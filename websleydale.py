#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import logging
import shutil
from abc import ABCMeta, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path
from shlex import quote
from subprocess import PIPE
from tempfile import mkdtemp, mkstemp
from typing import (
    Any,
    Awaitable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    cast,
)

import jinja2
import yaml
from mistletoe import Document, HTMLRenderer
from mistletoe.block_token import Heading
from slugify import slugify

__version__ = "3.0-dev"

logger = logging.getLogger(__name__)
jinjaenv = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=True,
)
tempdir: Optional[Path] = None
root = Path(".")


def outdir() -> Path:
    if tempdir is None:
        raise RuntimeError("outdir called while tempdir is None")
    return Path(mkdtemp(dir=tempdir))


def outfile() -> Path:
    if tempdir is None:
        raise RuntimeError("outdir called while tempdir is None")
    return Path(mkstemp(dir=tempdir)[1])


@dataclass
class Site:
    known_authors: Set[Author]
    name: str
    repo_name: str
    repo_url: str
    tree: Dict[str, FileProducer]
    generator: str = "websleydale"
    time: datetime = datetime.now()


@dataclass
class Info:
    path: str
    site: Site


def build(site: Site, *, dest: str) -> None:
    global tempdir

    destdir = Path(dest)
    if destdir.exists():
        logger.debug("Removing dest directory %s", destdir)
        shutil.rmtree(destdir)

    tempdir = Path(mkdtemp(prefix="websleydale-"))
    logger.debug("Using tempdir %s", tempdir)

    awaitables = []
    paths = []
    for pathstr, producer in site.tree.items():
        if pathstr.startswith("/"):
            raise ValueError(f"Invalid path {pathstr!r} (starts with '/')")
        if not isinstance(producer, FileProducer):
            raise TypeError(
                f"item for path {pathstr!r} has invalid type {type(producer)}"
            )
        destpath = destdir / pathstr
        info = Info(path=pathstr, site=site)
        awaitables.append(copy(destpath, producer, info))
        paths.append(pathstr)

    results = asyncio.run(gather(awaitables))
    successes = 0
    failures = 0
    for result, path in zip(results, paths):
        if isinstance(result, Exception):
            failures += 1
            logger.error(
                "[%s] %s: %s", path, result.__class__.__name__, result, exc_info=result
            )
        elif result is None:
            successes += 1
        else:
            failures += 1
            logger.error("[%s] got unexpected result %r", path, result)
    logger.info("%s SUCCESS / %s FAILURE", successes, failures)


async def copy(
    dest: Path, source_producer: FileProducer, info: Info, merge_dirs: bool = False
) -> None:
    source = await source_producer.run(info)
    if source.path.is_dir():
        logger.debug("Copying directory %s -> %s", source.path, dest)
        dest.parent.mkdir(exist_ok=True, parents=True)
        shutil.copytree(
            source.path,
            dest,
            copy_function=shutil.copy,  # ty: ignore[invalid-argument-type]
            dirs_exist_ok=merge_dirs,
        )
    else:
        if info.path.endswith("/"):
            dest = dest / "index.html"
        logger.debug("Copying file %s -> %s", source.path, dest)
        dest.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(source.path, dest)


async def gather(awaitables: Iterable[Awaitable[None]]) -> List[Optional[Exception]]:
    return cast(
        List[Optional[Exception]],
        await asyncio.gather(*awaitables, return_exceptions=True),
    )


@dataclass
class Result:
    sourceinfo: Optional[SourceInfo]


@dataclass
class FileResult(Result):
    path: Path


@dataclass
class TextResult(Result):
    content: str
    pageinfo: Dict[str, Any]


class FileProducer(metaclass=ABCMeta):
    @abstractmethod
    async def run(self, info: Info) -> FileResult: ...


class TextProducer(metaclass=ABCMeta):
    @abstractmethod
    async def run(self, info: Info) -> TextResult: ...


@dataclass(frozen=True)
class Author:
    display_name: str
    emails: Set[str] = field(hash=False)
    url: Optional[str]


@dataclass
class GitFileInfo:
    authors: List[Author]
    repo_name: Optional[str]
    repo_source_path: Optional[str]
    repo_url: Optional[str]
    updated_date: Optional[datetime]


@dataclass
class SourceInfo:
    authors: List[Author]
    is_committed: bool
    repo_name: Optional[str]
    repo_source_path: Optional[str]
    repo_url: Optional[str]
    updated_date: datetime


class file(FileProducer):
    def __init__(self, path: Path) -> None:
        self.path = path
        if not path.is_file():
            raise ValueError("not a file: %s", path)

    async def run(self, info: Info) -> FileResult:
        logger.debug("[%s] Loading Git info", self.path)
        gitinfo = await _git_file_info(self.path, info.site)
        sourceinfo = SourceInfo(
            authors=gitinfo.authors,
            is_committed=gitinfo.updated_date is not None,
            repo_name=gitinfo.repo_name,
            repo_source_path=gitinfo.repo_source_path,
            repo_url=gitinfo.repo_url,
            updated_date=gitinfo.updated_date or datetime.now(),
        )
        return FileResult(sourceinfo=sourceinfo, path=self.path)


class dir(FileProducer):
    def __init__(self, path: Path) -> None:
        self.path = path
        if not path.is_dir():
            raise ValueError("not a dir: %s", path)

    async def run(self, info: Info) -> FileResult:
        return FileResult(sourceinfo=None, path=self.path)


class merge(FileProducer):
    def __init__(self, *dirs: dir) -> None:
        self.dirs = dirs

    async def run(self, info: Info) -> FileResult:
        dest = outdir()
        for dir in self.dirs:
            await copy(dest, dir, info, merge_dirs=True)
        return FileResult(sourceinfo=None, path=dest)


async def _git_file_info(file: Path, site: Site) -> GitFileInfo:
    args = [
        "bash",
        "-c",
        f"cd {quote(str(file.parent))} && git ls-files --full-name {quote(str(file.name))}",
    ]
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=PIPE
    )  # ty: ignore[missing-argument]
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("git failed")

    lines = stdout.decode(errors="replace").splitlines()
    repo_source_path = lines[0] if lines else None

    args = ["bash", "-c", f"cd {quote(str(file.parent))} && git remote -v"]
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=PIPE
    )  # ty: ignore[missing-argument]
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("git failed")

    repo_name = None
    repo_url = None
    for line in stdout.decode(errors="replace").splitlines():
        remote_name, remote_url, _ = line.split(maxsplit=2)
        if remote_name == "origin":
            repo_url = remote_url
            break
    if repo_url is not None:
        if repo_url.endswith(".git"):
            repo_url = repo_url[: -len(".git")]
        if repo_url.startswith("git@github.com:"):
            repo_name = repo_url[len("git@github.com:") :]
            repo_url = f"https://github.com/{repo_name}"
    if repo_url and not repo_name:
        repo_name = "/".join(repo_url.split("/")[-2:])

    args = [
        "bash",
        "-c",
        f"cd {quote(str(file.parent))} && git log --format='%cI %ae %an' -- {quote(str(file.name))}",
    ]
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=PIPE
    )  # ty: ignore[missing-argument]
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("git failed")

    authors: Counter[Author] = Counter()
    date = None
    for line in stdout.decode(errors="replace").splitlines():
        datestr, email, name = line.split(maxsplit=2)
        if date is None:
            date = datetime.fromisoformat(datestr)
        author = next((a for a in site.known_authors if email in a.emails), None)
        if author is None:
            author = Author(display_name=name, emails={email}, url=None)
        authors[author] += 1

    return GitFileInfo(
        authors=[a for a, _ in authors.most_common()],
        repo_name=repo_name,
        repo_source_path=repo_source_path,
        repo_url=repo_url,
        updated_date=date,
    )


class markdown(TextProducer):
    def __init__(self, path: Path) -> None:
        self.source = file(path)

    async def run(self, info: Info) -> TextResult:
        source = await self.source.run(info)
        content = source.path.read_text()

        pageinfo: Dict[str, Any] = {}
        if content.startswith("---\n"):
            yamltext, content = content[4:].split("---\n", maxsplit=1)
            pageinfo.update(yaml.safe_load(yamltext))

        with WebsleydaleHTMLRenderer() as renderer:
            rendered = renderer.render(Document(content))

        return TextResult(
            sourceinfo=source.sourceinfo, content=rendered, pageinfo=pageinfo
        )


class fake(TextProducer):
    def __init__(self, pageinfo: Optional[Dict[str, Any]] = None) -> None:
        self.pageinfo = pageinfo if pageinfo is not None else {}

    async def run(self, info: Info) -> TextResult:
        sourceinfo = SourceInfo(
            authors=[],
            is_committed=False,
            repo_name=None,
            repo_source_path="",
            repo_url=None,
            updated_date=datetime.now(),
        )
        return TextResult(sourceinfo=sourceinfo, content="", pageinfo=self.pageinfo)


class string(TextProducer):
    def __init__(self, s: str, pageinfo: dict | None = None) -> None:
        self.s = s
        self.pageinfo = pageinfo

    async def run(self, info: Info) -> TextResult:
        sourceinfo = SourceInfo(
            authors=[],
            is_committed=False,
            repo_name=None,
            repo_source_path=None,
            repo_url=None,
            updated_date=datetime.now(),
        )
        return TextResult(
            sourceinfo=sourceinfo, content=self.s, pageinfo=self.pageinfo or {}
        )


class jinja(FileProducer):
    def __init__(
        self, source: TextProducer, template: str, title: str | None = None
    ) -> None:
        self.source = source
        self.template = jinjaenv.get_template(template)
        self.title = title

    async def run(self, info: Info) -> FileResult:
        source = await self.source.run(info)
        content = source.content
        pageinfo = source.pageinfo
        dest = outfile()

        pageinfo["content"] = content
        pageinfo["path"] = info.path
        if self.title is not None:
            pageinfo["title"] = self.title
        rendered = self.template.render(
            page=pageinfo, site=info.site, source=source.sourceinfo
        )
        dest.write_text(rendered)

        return FileResult(sourceinfo=source.sourceinfo, path=dest)


class sass(FileProducer):
    def __init__(self, path: Path) -> None:
        self.source = file(path)

    async def run(self, info: Info) -> FileResult:
        source = await self.source.run(info)
        dest = outfile()
        args = ["pysassc", "--style", "compressed", str(source.path), str(dest)]
        proc = await asyncio.create_subprocess_exec(
            *args
        )  # ty: ignore[missing-argument]
        exitcode = await proc.wait()
        if exitcode != 0:
            raise RuntimeError("pysassc failed")
        return FileResult(sourceinfo=source.sourceinfo, path=dest)


class IdGenerator:
    def __init__(self) -> None:
        self.used_ids: Counter[str] = Counter()

    def get_id(self, text: str) -> str:
        id_base = slugify(text, entities=False, decimal=False, hexadecimal=False)
        if id_base in self.used_ids:
            real_id = f"{id_base}-{self.used_ids[id_base]}"
        else:
            real_id = id_base
        self.used_ids[id_base] += 1
        return real_id


class WebsleydaleHTMLRenderer(HTMLRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.ids = IdGenerator()

    def render_heading(self, token: Heading) -> str:
        level = token.level
        inner = self.render_inner(token)
        if level > 1:
            identifier = self.ids.get_id(self.render_to_plain(token))
            return f'<a class=anchor href="#{identifier}"><h{level} id="{identifier}">{inner}</h{level}></a>'
        else:
            return f"<h{level}>{inner}</h{level}>"


def index_page(paths: list[str], *, title: str) -> jinja:
    items = [
        f'  <li><a href="{escape(path)}">{escape(path, quote=False)}</a></li>\n'
        for path in paths
    ]
    content = string(
        f"<ul class=index>\n{''.join(items)}</ul>", pageinfo={"title": title}
    )
    return jinja(content, template="page.html")


def index(tree: Dict[str, FileProducer], *dirs: str) -> Dict[str, FileProducer]:
    index_paths = {dir: [] for dir in dirs}
    for dest, source in tree.items():
        for dir, paths in index_paths.items():
            try:
                relpath = Path(dest).relative_to(dir)
            except ValueError:
                pass
            else:
                paths.append(str(relpath))
    return {
        **tree,
        **{
            f"{dir}/index.html": index_page(paths, title=dir.capitalize())
            for dir, paths in index_paths.items()
        },
    }

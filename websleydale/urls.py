from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Self


@dataclass(frozen=True, order=True)
class UrlfileEntry:
    path: str
    present: bool = True

    @classmethod
    def parse(cls, s: str) -> Self:
        if (path := s.removeprefix("MISSING: ")) != s:
            return cls(path, present=False)
        else:
            return cls(s)

    def __post_init__(self) -> None:
        if not self.path.startswith("/"):
            raise ValueError(f"path must be absolute: {self.path!r}")

    def __str__(self) -> str:
        if self.present:
            return self.path
        else:
            return f"MISSING: {self.path}"


@dataclass(frozen=True)
class Urlfile:
    entries: set[UrlfileEntry]

    FILE_HEADER: ClassVar[str] = "# websleydale URLs\n"

    @staticmethod
    def path(basedir: Path) -> Path:
        return basedir / "urls.txt"

    @classmethod
    def read(cls, basedir: Path) -> Self:
        path = cls.path(basedir)
        entries = set()
        with ExitStack() as stack:
            try:
                f = stack.enter_context(path.open())
            except FileNotFoundError:
                return cls(set())
            if next(f) != cls.FILE_HEADER:
                raise RuntimeError(f"{path} is not in the expected format")
            for line in f:
                entry = UrlfileEntry.parse(line.rstrip("\n"))
                if entry in entries:
                    raise RuntimeError(f"Duplicate entry in urls file: {entry!r}")
                entries.add(entry)
        return cls(entries)

    def urls(self) -> set[str]:
        return set(e.path for e in self.entries)

    def write(self, basedir: Path) -> None:
        dest = self.path(basedir)
        try:
            with dest.open() as f:
                line = f.readline()
            if line != self.FILE_HEADER:
                raise FileExistsError(f"Refusing to overwrite existing file {dest}")
        except FileNotFoundError:
            pass
        with dest.open("w") as f:
            f.write(self.FILE_HEADER)
            f.writelines(f"{e}\n" for e in sorted(self.entries))

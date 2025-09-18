from __future__ import annotations

import functools
import logging
import re
from contextlib import contextmanager
from copy import replace
from dataclasses import dataclass
from enum import Enum, auto
from types import FunctionType
from typing import Iterator, NamedTuple, Self, TypeVar

from .tokenizer import Tag, Token

logger = logging.getLogger(__name__)


class UnexpectedToken(RuntimeError):
    def __init__(self, message: str, start: int, stop: int) -> None:
        super().__init__(message)
        self.start = start
        self.stop = stop


T = TypeVar("T", bound=FunctionType)


def log_enter_exit(func: T) -> T:
    @functools.wraps(func)
    def _log_enter_exit_wrapper(self, *args, **kwargs):
        self.log_enter("%s", func.__name__)
        try:
            result = func(self, *args, **kwargs)
        except UnexpectedToken as e:
            self.log_exit("%s: %s", type(e).__name__, e)
            raise
        else:
            self.log_exit("%s", result)
            return result

    return _log_enter_exit_wrapper


RAW_TAGS = [t for t in Tag if t != Tag.eof]
INTRODUCER_TAGS = [
    Tag.dotdot,
    Tag.coloncolon,
    Tag.bangbang,
]
NAME_TAGS = [
    Tag.word,
    Tag.text,
    Tag.star,
    Tag.bar,
    Tag.underscore,
    Tag.backtick,
]
SPAN_TEXT_TAGS = [
    Tag.word,
    Tag.space,
    Tag.text,
    Tag.newline,
    Tag.comma,
    Tag.equals,
    Tag.colon,
    Tag.l_paren,
    Tag.r_paren,
]
SPAN_DELIMITER_TAGS = [
    Tag.star,
    Tag.starstar,
    Tag.bar,
    Tag.barbar,
    Tag.underscore,
    Tag.underscoreunderscore,
    Tag.backtick,
    Tag.backtickbacktick,
    Tag.l_brace,
]
assert len(set(SPAN_TEXT_TAGS) & set(SPAN_DELIMITER_TAGS)) == 0


BACKSLASH_REMOVER = re.compile(r"\\(.)")


class LineCol(NamedTuple):
    line: int
    col: int


class Parser:
    buffer: str
    tokens: list[Token]
    index: int
    depth: int
    iteration_limit: int | None

    def __init__(
        self, buffer: str, tokens: list[Token], *, iteration_limit: int | None = None
    ) -> None:
        self.buffer = buffer
        self.tokens = tokens
        self.index = 0
        self.depth = 0
        self.iteration_limit = iteration_limit

    def log(self, template: str, *args) -> None:
        prefix = "| " * self.depth
        logger.debug(prefix + template, *args)

    def log_enter(self, template: str, *args) -> None:
        if self.iteration_limit is not None:
            self.iteration_limit -= 1
            if self.iteration_limit == 0:
                raise RuntimeError("iteration_limit reached")
        self.log(template, *args)
        self.depth += 1

    def log_exit(self, template: str, *args) -> None:
        self.depth -= 1
        self.log("> " + template, *args)

    def find_position(self, pos: int) -> LineCol:
        line = self.buffer.count("\n", 0, pos) + 1
        col = pos - self.buffer.rfind("\n", 0, pos)
        return LineCol(line, col)

    def resolve_text(self, token: Token) -> str:
        slice = self.buffer[token.start : token.stop]
        return BACKSLASH_REMOVER.sub(r"\1", slice)

    @contextmanager
    def transaction(self) -> Iterator[None]:
        saved_index = self.index
        try:
            yield
        except UnexpectedToken:
            if self.index != saved_index:
                logger.debug(
                    "Transaction failed; rewinding index by %s tokens",
                    self.index - saved_index,
                )
                self.index = saved_index
            raise

    def try_consume(self, *tags: Tag) -> Token | None:
        assert Tag.eof not in tags
        token = self.tokens[self.index]
        if token.tag not in tags:
            return None
        self.index += 1
        self.log(
            "\x1b[32mconsume\x1b[39m(\x1b[34m%s\x1b[39m) %r",
            token.tag,
            self.buffer[token.start : token.stop],
        )
        return token

    def consume(self, *tags: Tag) -> Token:
        token = self.try_consume(*tags)
        if token is None:
            unexpected = self.tokens[self.index]
            raise UnexpectedToken(
                f"expected {tags}, found {unexpected.tag}",
                unexpected.start,
                unexpected.stop,
            )
        return token

    def next_is(self, *tags: Tag) -> bool:
        return self.tokens[self.index].tag in tags

    def skip(self, *tags: Tag) -> None:
        assert Tag.eof not in tags
        while True:
            token = self.tokens[self.index]
            if token.tag not in tags:
                break
            self.index += 1
            self.log("\x1b[32mskip\x1b[39m(\x1b[34m%s\x1b[39m)", token.tag)

    def parse_document(self) -> list[Node]:
        nodes = []
        while not self.next_is(Tag.eof) and (node := self.parse_any()) is not None:
            nodes.append(node)
        if not self.next_is(Tag.eof):
            token = self.tokens[self.index]
            raise UnexpectedToken(
                f"failed to parse; next token is {token}",
                start=token.start,
                stop=token.stop,
            )
        return nodes

    @log_enter_exit
    def parse_any(self) -> Node | None:
        self.skip(Tag.blank_line)
        if (node := self.parse_block()) is not None:
            return node
        elif (node := self.parse_raw()) is not None:
            return node
        elif (node := self.parse_toplevel_span()) is not None:
            return node
        return None

    @log_enter_exit
    def parse_block(self) -> Node | None:
        if self.try_consume(Tag.coloncolon) is None:
            return None

        try:
            name_token = self.consume(Tag.word)
        except UnexpectedToken as e:
            e.add_note("expected word to follow coloncolon")
            raise

        try:
            params = self.parse_parameters()
        except UnexpectedToken as e:
            e.add_note(f"while parsing the args for block {name_token}")
            raise

        self.skip(Tag.space, Tag.newline, Tag.blank_line)

        children: list[Node] = []
        if self.next_is(Tag.indent):
            self.consume(Tag.indent)
            while (node := self.parse_any()) is not None:
                children.append(node)
            self.consume(Tag.dedent)

        return Node(
            name=self.resolve_text(name_token),
            scope=Scope.block,
            params=params,
            data=children,
        )

    @log_enter_exit
    def parse_raw(self) -> Node | None:
        if self.try_consume(Tag.bangbang) is None:
            return None

        name_token = self.consume(Tag.word)
        params = self.parse_parameters()
        self.skip(Tag.space, Tag.newline)

        spans: list[Node] = []
        internal_indent = 0
        if self.try_consume(Tag.indent) is not None:
            while not self.next_is(Tag.dedent) or internal_indent > 0:
                if (token := self.try_consume(Tag.indent, Tag.dedent)) is not None:
                    internal_indent += token.indent
                elif (
                    span := self.parse_any_span(exclude=frozenset(), raw=True)
                ) is not None:
                    if internal_indent and not span.data.startswith("\n"):
                        spans.append(Node.string(" " * internal_indent))
                    spans.append(span)
                else:
                    token = self.consume(*RAW_TAGS)
                    raise UnexpectedToken(
                        f"Unhandled tag while parsing raw: {token.tag}",
                        token.start,
                        token.stop,
                    )
            assert internal_indent == 0
            self.consume(Tag.dedent)

        return Node(
            name=self.resolve_text(name_token),
            scope=Scope.block,
            params=params,
            data=collapse_inner_spans(strip_trailing_newlines(spans)),
        )

    @log_enter_exit
    def parse_toplevel_span(self) -> Node | None:
        if self.try_consume(Tag.dotdot) is not None:
            name_token = self.consume(*NAME_TAGS)
            name = self.resolve_text(name_token)
            params = self.parse_parameters()
            self.skip(Tag.space, Tag.newline)
        else:
            name = ""
            params = Parameters.empty()
        inner = self.parse_span_sequence(exclude=frozenset())
        if name == "" and inner is None:
            return None
        if inner is None:
            data = ""
        else:
            data = collapse_inner_spans(inner)
        return Node(
            name=name,
            scope=Scope.toplevel,
            params=params,
            data=data,
        )

    @log_enter_exit
    def parse_span_sequence(self, *, exclude: frozenset[Tag]) -> list[Node] | None:
        spans = []
        while (span := self.parse_any_span(exclude=exclude, raw=False)) is not None:
            spans.append(span)
        return spans or None

    @log_enter_exit
    def parse_any_span(self, *, exclude: frozenset[Tag], raw: bool) -> Node | None:
        if self.next_is(*exclude):
            return None
        if (span := self.parse_named_span(exclude=exclude, raw=raw)) is not None:
            return span
        elif (
            not raw
            and (span := self.parse_delimited_span(exclude=exclude, raw=raw))
            is not None
        ):
            return span
        elif (span := self.parse_text_span(exclude=exclude, raw=raw)) is not None:
            return span
        return None

    @log_enter_exit
    def parse_named_span(self, *, exclude: frozenset[Tag], raw: bool) -> Node | None:
        if not self.next_is(Tag.colon):
            return None
        try:
            with self.transaction():
                self.consume(Tag.colon)
                name_token = self.consume(Tag.word)
                params = self.parse_parameters()
                self.consume(Tag.colon)
                inner = self.parse_delimited_span(exclude=exclude, raw=raw)
                if inner is None:
                    raise UnexpectedToken(
                        "expected delimited span following named span introducer", 0, 0
                    )
        except UnexpectedToken:
            return None
        return Node(
            name=self.resolve_text(name_token),
            scope=Scope.inline,
            params=params,
            data=inner.data if inner is not None else "",
        )

    @log_enter_exit
    def parse_delimited_span(
        self, *, exclude: frozenset[Tag], raw: bool
    ) -> Node | None:
        if not self.next_is(*SPAN_DELIMITER_TAGS):
            return None
        open_delimiter_token = self.consume(*SPAN_DELIMITER_TAGS)
        open_delimiter_tag = open_delimiter_token.tag
        if open_delimiter_tag == Tag.l_brace:
            close_delimiter_tag = Tag.r_brace
        else:
            close_delimiter_tag = open_delimiter_tag
        inner = self.parse_span_sequence(exclude={close_delimiter_tag} | exclude)
        if inner is None:
            data = ""
        else:
            data = collapse_inner_spans(inner)
        try:
            self.consume(close_delimiter_tag)
        except UnexpectedToken as e:
            tag = open_delimiter_token.tag
            line, col = self.find_position(open_delimiter_token.start)
            e.add_note(
                f"While parsing a span started by the {tag} at line {line} col {col}"
            )
            raise
        return Node(
            name=open_delimiter_tag.name,
            scope=Scope.inline,
            params=Parameters.empty(),
            data=data,
        )

    @log_enter_exit
    def parse_text_span(self, *, exclude: frozenset[Tag], raw: bool) -> Node | None:
        text_tags = (
            SPAN_TEXT_TAGS
            + [
                Tag.blank_line,
                Tag.dotdot,
                Tag.coloncolon,
                Tag.bangbang,
                Tag.l_brace,
                Tag.r_brace,
            ]
            + SPAN_DELIMITER_TAGS
            if raw
            else SPAN_TEXT_TAGS
        )
        if not self.next_is(*text_tags):
            return None
        parts = []
        while (token := self.try_consume(*text_tags)) is not None:
            if token.tag == Tag.newline:
                if raw or self.next_is(*text_tags):
                    parts.append("\n" if raw else " ")
            elif token.tag == Tag.blank_line:
                parts.append("\n")
            else:
                parts.append(self.resolve_text(token))
            if self.next_is(Tag.colon):
                break
        if not parts:
            return None
        full_text = "".join(parts)
        return Node(
            name="",
            scope=Scope.inline,
            params=Parameters.empty(),
            data=full_text,
        )

    @log_enter_exit
    def parse_parameters(self) -> Parameters:
        if self.try_consume(Tag.l_paren) is None:
            return Parameters([], {})

        self.skip(Tag.space)

        args = []
        kwargs = {}
        while not self.next_is(Tag.r_paren):
            key_token = self.consume(Tag.word, Tag.text)
            if self.try_consume(Tag.equals) is not None:
                value_token = self.consume(Tag.word, Tag.text)
                kwargs[self.resolve_text(key_token)] = self.resolve_text(value_token)
            else:
                args.append(self.resolve_text(key_token))
            self.skip(Tag.comma, Tag.space)

        self.consume(Tag.r_paren)
        return Parameters(args, kwargs)


def collapse_inner_spans(spans: list[Node]) -> list[Node] | str:
    match spans:
        case []:
            return ""
        case [span]:
            if span.name == "":
                return span.data
            else:
                return [span]
        case [first, *rest]:
            logger.debug("simplifying %s items", len(rest) + 1)
            simplified = [first]
            for span in rest:
                if span.name == "" and (prev := simplified[-1]).name == "":
                    logger.debug("replacing")
                    simplified[-1] = replace(prev, data=prev.data + span.data)
                else:
                    logger.debug("appending")
                    simplified.append(span)
            return simplified
        case _:
            raise TypeError(
                f"unhandled value passed to collapse_inner_spans: {spans!r}"
            )


@dataclass(frozen=True)
class Parameters:
    args: list[str]
    kwargs: dict[str, str]

    @classmethod
    def empty(cls) -> Self:
        return cls([], {})


class Scope(Enum):
    inline = auto()
    toplevel = auto()
    block = auto()


@dataclass(frozen=True)
class Node:
    name: str
    scope: Scope
    params: Parameters
    data: str | list[Node]

    def __post_init__(self) -> None:
        if not isinstance(self.data, (str, list)):
            raise TypeError(
                f"Node() data must be str or list; got {type(self.data).__name__}"
            )

    def __repr__(self) -> str:
        if isinstance(self.data, list):
            if len(self.data) < 8:
                data = ", ".join(map(str, self.data))
            else:
                data = f"<{len(self.data)} nodes>"
        else:
            data = repr(abbreviate(self.data))
        return f"Node({self.name!r}, data={data})"

    @classmethod
    def string(cls, s: str) -> Self:
        return cls(
            name="",
            scope=Scope.inline,
            params=Parameters.empty(),
            data=s,
        )


def format_tree(nodes: list[Node], depth: int = 0) -> Iterator[str]:
    for node in nodes:
        if isinstance(node.data, str):
            yield f"{'  ' * depth}<{node.name}> {node.data!r}"
        else:
            yield f"{'  ' * depth}<{node.name}>:"
            yield from format_tree(node.data, depth + 1)


def abbreviate(s: str) -> str:
    if len(s) > 25:
        return s[:24] + "…"
    return s


def strip_trailing_newlines(spans: list[Node]) -> list[Node]:
    if (
        spans
        and (final_span := spans[-1]).name == ""
        and isinstance(final_span.data, str)
        and final_span.data.endswith("\n")
    ):
        stripped = final_span.data.rstrip("\n")
        if stripped:
            return spans[:-1] + [replace(final_span, data=stripped)]
        else:
            return spans[:-1]
    else:
        return spans

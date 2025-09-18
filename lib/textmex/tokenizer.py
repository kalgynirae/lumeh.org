from __future__ import annotations

import logging
import string
from dataclasses import dataclass
from enum import Enum, auto

logger = logging.getLogger(__name__)


class Tag(Enum):
    invalid = auto()
    eof = auto()
    blank_line = auto()
    indent = auto()
    dedent = auto()
    word = auto()
    space = auto()
    text = auto()
    newline = auto()
    comma = auto()
    equals = auto()
    dotdot = auto()
    coloncolon = auto()
    bangbang = auto()
    colon = auto()
    star = auto()
    starstar = auto()
    bar = auto()
    barbar = auto()
    underscore = auto()
    underscoreunderscore = auto()
    backtick = auto()
    backtickbacktick = auto()
    l_paren = auto()
    r_paren = auto()
    l_brace = auto()
    r_brace = auto()

    def __repr__(self) -> str:
        return f".{self.name}"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass(frozen=True)
class Token:
    tag: Tag
    start: int
    stop: int
    indent: int | None

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.tag}, {self.start}:{self.stop})"


DELIMITER_CHARS = {*"*|_`"}
WORD_CHARS = {*string.ascii_letters, *string.digits, "-"}
HANDLED_CHARS = DELIMITER_CHARS | WORD_CHARS | {*' \n=(){}"\\', None}


def delimiter_char_to_single_tag(s: str) -> Tag:
    if s == "*":
        return Tag.star
    elif s == "|":
        return Tag.bar
    elif s == "_":
        return Tag.underscore
    elif s == "`":
        return Tag.backtick
    else:
        assert False, (
            f"{delimiter_char_to_single_tag.__name__}() called with invalid character {s!r}"
        )


def delimiter_char_to_double_tag(s: str) -> Tag:
    if s == "*":
        return Tag.starstar
    elif s == "|":
        return Tag.barbar
    elif s == "_":
        return Tag.underscoreunderscore
    elif s == "`":
        return Tag.backtickbacktick
    else:
        assert False, (
            f"{delimiter_char_to_double_tag.__name__}() called with invalid character {s!r}"
        )


class State(Enum):
    eof = auto()
    indentation = auto()
    post_indentation = auto()
    default = auto()
    word = auto()
    whitespace = auto()
    delimiter = auto()
    quoted_string = auto()
    backslash = auto()
    text = auto()


class Tokenizer:
    buffer: str
    index: int
    next_state: State
    indents: list[int]

    def __init__(self, buffer: str) -> None:
        self.buffer = buffer
        self.index = 0
        self.next_state = State.indentation
        self.indents = [0]

    def advance(self) -> None:
        self.index += 1
        assert self.index <= len(self.buffer), (
            "advance() called while already at end of buffer"
        )

    def char(self, index: int | None = None) -> str | None:
        try:
            return self.buffer[index if index is not None else self.index]
        except IndexError:
            return None

    def next(self) -> Token:
        token_tag: Tag | None = None
        token_start: int = self.index
        token_stop: int | None = None
        token_indent: int | None = None

        state = self.next_state
        while True:
            if state == State.eof:
                assert self.index == len(self.buffer), (
                    f"reached {State.eof} while not at end of buffer"
                )
                if len(self.indents) > 1:
                    current_indent = self.indents.pop()
                    previous_indent = self.indents[-1]
                    logger.debug(
                        "dedent %s -> %s (EOF)", current_indent, previous_indent
                    )
                    token_tag = Tag.dedent
                    token_indent = previous_indent - current_indent
                else:
                    token_tag = Tag.eof
                self.next_state = State.eof

            elif state == State.indentation:
                if self.index == len(self.buffer):
                    state = State.eof
                    continue
                temp_index = self.index
                found_newline = False
                while True:
                    char = self.char(temp_index)
                    if char == " " or char == "\t":
                        temp_index += 1
                        continue
                    elif char == "\n":
                        temp_index += 1
                        found_newline = True
                    break
                last_indent = self.indents[-1]
                new_indent = temp_index - self.index
                if found_newline:
                    # Skip over the indent and yield a blank line
                    self.index = temp_index
                    token_tag = Tag.blank_line
                    token_start = self.index
                elif new_indent == last_indent:
                    # Skip over the indent without yielding a token
                    self.index = temp_index
                    token_start = temp_index
                    self.next_state = State.post_indentation
                    state = State.post_indentation
                    continue
                elif new_indent > last_indent:
                    logger.debug("indent %s -> %s", last_indent, new_indent)
                    self.indents.append(new_indent)
                    self.index = temp_index
                    token_tag = Tag.indent
                    token_start = self.index
                    token_stop = self.index
                    token_indent = new_indent - last_indent
                    self.next_state = State.post_indentation
                else:
                    _ = self.indents.pop()
                    previous_indent = self.indents[-1]
                    logger.debug(
                        "dedent %s -> %s (target %s)",
                        last_indent,
                        previous_indent,
                        new_indent,
                    )
                    token_tag = Tag.dedent
                    token_start = temp_index
                    token_stop = temp_index
                    token_indent = previous_indent - last_indent
                    if previous_indent == new_indent:
                        self.index = temp_index
                        self.next_state = State.post_indentation

            elif state == State.post_indentation:
                char = self.char()
                nextchar = self.char(self.index + 1)
                if char == "." == nextchar:
                    self.advance()
                    self.advance()
                    token_tag = Tag.dotdot
                elif char == ":" == nextchar:
                    self.advance()
                    self.advance()
                    token_tag = Tag.coloncolon
                elif char == "!" == nextchar:
                    self.advance()
                    self.advance()
                    token_tag = Tag.bangbang
                else:
                    self.next_state = State.default
                    state = State.default
                    continue

            elif state == State.default:
                char = self.char()
                if char is None:
                    if self.indents[-1] == 0:
                        state = State.eof
                        continue
                    else:
                        token_tag = Tag.newline
                        self.next_state = State.eof
                elif char == "\n":
                    self.advance()
                    self.next_state = State.indentation
                    token_tag = Tag.newline
                elif char == ":":
                    self.advance()
                    token_tag = Tag.colon
                elif char == ",":
                    self.advance()
                    token_tag = Tag.comma
                elif char == "=":
                    self.advance()
                    token_tag = Tag.equals
                elif char == "(":
                    self.advance()
                    token_tag = Tag.l_paren
                elif char == ")":
                    self.advance()
                    token_tag = Tag.r_paren
                elif char == "{":
                    self.advance()
                    token_tag = Tag.l_brace
                elif char == "}":
                    self.advance()
                    token_tag = Tag.r_brace
                elif char == " ":
                    state = State.whitespace
                    continue
                elif char == '"':
                    token_start = self.index + 1
                    state = State.quoted_string
                    continue
                elif char == "\\":
                    state = State.backslash
                    continue
                elif char in DELIMITER_CHARS:
                    state = State.delimiter
                    continue
                elif char in WORD_CHARS:
                    state = State.word
                    continue
                else:
                    state = State.text
                    continue

            elif state == State.word:
                self.advance()
                if self.char() in WORD_CHARS:
                    continue
                else:
                    token_tag = Tag.word

            elif state == State.whitespace:
                self.advance()
                if self.char() == " ":
                    continue
                else:
                    token_tag = Tag.space

            elif state == State.delimiter:
                first_char = self.char()
                self.advance()
                if self.char() == first_char:
                    self.advance()
                    token_tag = delimiter_char_to_double_tag(first_char)
                else:
                    token_tag = delimiter_char_to_single_tag(first_char)

            elif state == State.quoted_string:
                self.advance()
                char = self.char()
                if char == '"':
                    self.advance()
                    token_tag = Tag.text
                    token_stop = self.index - 1
                elif char == "\\":
                    self.advance()
                    if self.char() == "\n":
                        token_tag = Tag.invalid
                    else:
                        continue
                else:
                    continue

            elif state == State.backslash:
                self.advance()
                char = self.char()
                if char == "\n":
                    token_tag = Tag.invalid
                else:
                    state = State.text
                    continue

            elif state == State.text:
                self.advance()
                char = self.char()
                if char == "\\":
                    state = State.backslash
                    continue
                elif self.char() in HANDLED_CHARS:
                    token_tag = Tag.text
                else:
                    continue

            break

        assert token_tag is not None
        if token_tag == Tag.indent or token_tag == Tag.dedent:
            assert token_indent is not None
        token = Token(
            tag=token_tag,
            start=token_start,
            stop=token_stop if token_stop is not None else self.index,
            indent=token_indent,
        )
        logger.debug("TOKEN %s(%r)", token, self.buffer[token.start : token.stop])
        return token

import logging
from textwrap import dedent

from textmex.tokenizer import Tag, Tokenizer


def test_simple(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    input = "..foo"
    tokenizer = Tokenizer(input)
    assert tokenizer.next().tag == Tag.dotdot
    assert tokenizer.next().tag == Tag.word
    assert tokenizer.next().tag == Tag.eof


def test_params(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    input = r"""..foo(a, b=5, c="#|\":)\\str")"""
    tokenizer = Tokenizer(input)
    expected_tags = [
        Tag.dotdot,
        Tag.word,
        Tag.l_paren,
        Tag.word,
        Tag.comma,
        Tag.space,
        Tag.word,
        Tag.equals,
        Tag.word,
        Tag.comma,
        Tag.space,
        Tag.word,
        Tag.equals,
        Tag.text,
        Tag.r_paren,
        Tag.eof,
    ]
    for tag in expected_tags:
        assert tokenizer.next().tag == tag


def test_indentation(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        not indented
          indented a bit
            indented even more
        fully dedented
            again indented
          unexpectedly indented
        end
        """
    )
    tokenizer = Tokenizer(input)
    expected_tags = iter(
        [
            Tag.indent,
            Tag.indent,
            Tag.dedent,
            Tag.dedent,
            Tag.indent,
            Tag.dedent,
            Tag.indent,
            Tag.dedent,
        ]
    )
    token = tokenizer.next()
    while token.tag != Tag.eof:
        if token.tag == Tag.indent or token.tag == Tag.dedent:
            assert token.tag == next(expected_tags)
        token = tokenizer.next()


def test_dedent_at_eof(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        a
          b
            c
        """
    )
    tokenizer = Tokenizer(input)
    expected_tags = iter(
        [
            Tag.word,
            Tag.newline,
            Tag.indent,
            Tag.word,
            Tag.newline,
            Tag.indent,
            Tag.word,
            Tag.newline,
            Tag.dedent,
            Tag.dedent,
            Tag.eof,
        ]
    )
    for tag in expected_tags:
        assert tokenizer.next().tag == tag


def test_dedent_at_eof_no_newline(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        a
          b
            c"""
    )
    tokenizer = Tokenizer(input)
    expected_tags = iter(
        [
            Tag.word,
            Tag.newline,
            Tag.indent,
            Tag.word,
            Tag.newline,
            Tag.indent,
            Tag.word,
            Tag.newline,
            Tag.dedent,
            Tag.dedent,
            Tag.eof,
        ]
    )
    for tag in expected_tags:
        assert tokenizer.next().tag == tag


def test_full(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """
        ..foo(test, cool-name="That's wild", type=15) Here's some
        stuff:*cool* :what:{bea|n|s}

        ::test
          this is indented

          so is this

        this is not
        !what!{bea|n|s}
        """
    )
    tokenizer = Tokenizer(input)
    for _ in range(1000):
        if tokenizer.next().tag == Tag.eof:
            break
    else:
        assert False, "didn't see EOF in 1000 tokens (probably stuck in a loop)"


def test_introducer_tokens(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        ..span
        ::block
        !!raw
        foo..::!!
        """
    )
    tokenizer = Tokenizer(input)
    expected_tags = iter(
        [
            Tag.dotdot,
            Tag.word,
            Tag.newline,
            Tag.coloncolon,
            Tag.word,
            Tag.newline,
            Tag.bangbang,
            Tag.word,
            Tag.newline,
            Tag.word,
            Tag.text,
        ]
    )
    for tag in expected_tags:
        assert tokenizer.next().tag == tag


def test_backslashes(caplog):
    caplog.set_level(logging.DEBUG)
    input = r"\a\*\||a|"
    tokenizer = Tokenizer(input)
    expected_tags = iter(
        [
            Tag.text,
            Tag.bar,
            Tag.word,
            Tag.bar,
            Tag.eof,
        ]
    )
    for tag in expected_tags:
        assert tokenizer.next().tag == tag


def test_backslashes_2(caplog):
    caplog.set_level(logging.DEBUG)
    input = r"\*a\|\|\\"
    tokenizer = Tokenizer(input)
    expected_tags = iter(
        [
            Tag.text,
            Tag.word,
            Tag.text,
            Tag.eof,
        ]
    )
    for tag in expected_tags:
        assert tokenizer.next().tag == tag

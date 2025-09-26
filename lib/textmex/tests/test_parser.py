import logging
from textwrap import dedent

from textmex import parse
from textmex.parser import Parameters


def test_full(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        foo

        ::bar(a, b=5, c, d="x y z")
            test
            test2 **test3** |foo *bar*|
        """
    )
    parse(input)


def test_spans(caplog):
    caplog.set_level(logging.DEBUG)
    input = "a *b* c"
    nodes = parse(input)
    assert len(nodes) == 1
    (parent,) = nodes
    assert len(parent.data) == 3
    assert isinstance(parent.data, list)
    text1, inner, text2 = parent.data
    assert text1.data == "a "
    assert inner.name == "star"
    assert inner.data == "b"
    assert text2.data == " c"


def test_span_params(caplog):
    caplog.set_level(logging.DEBUG)
    input = "a :john:{b} :karl(p):{c}"
    nodes = parse(input)
    assert len(nodes) == 1
    (parent,) = nodes
    assert len(parent.data) == 4
    assert isinstance(parent.data, list)
    text, john, space, karl = parent.data
    assert text.data == "a "
    assert john.name == "john"
    assert john.data == "b"
    assert space.data == " "
    assert karl.name == "karl"
    assert karl.params == Parameters(["p"], {})
    assert karl.data == "c"


def test_escaped_delimiters(caplog):
    caplog.set_level(logging.DEBUG)
    input = r"\*a\|\|\*"
    (n,) = parse(input)
    assert n.data == "*a||*"


def test_toplevel_spans(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        a

        ..a(b) c
        d e
        """
    )
    nodes = parse(input)
    assert len(nodes) == 2
    (simple, complex) = nodes
    assert simple.name == ""
    assert simple.params == Parameters([], {})
    assert simple.data == "a"
    assert complex.name == "a"
    assert complex.params == Parameters(["b"], {})
    assert complex.data == "c d e"


def test_compact_toplevel_spans(caplog):
    caplog.set_level(logging.DEBUG)
    input = "..a foo\n..b bar\n"
    nodes = parse(input)
    assert len(nodes) == 2
    (a, b) = nodes
    assert a.name == "a"
    assert a.data == "foo"
    assert b.name == "b"
    assert b.data == "bar"


def test_compact_blocks(caplog):
    caplog.set_level(logging.DEBUG)
    input = "::a\n::b\n"
    nodes = parse(input)
    assert len(nodes) == 2
    (a, b) = nodes
    assert a.name == "a"
    assert a.data == []
    assert b.name == "b"
    assert b.data == []


def test_empty_spans_in_block(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        ::block
          ..span
          ..span
        """
    )
    nodes = parse(input)
    assert len(nodes) == 1


def test_empty_line_starting_block(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """\
        ::block

          test
        """
    )
    nodes = parse(input, iteration_limit=30)
    assert len(nodes) == 1


def test_named_span(caplog):
    caplog.set_level(logging.DEBUG)
    input = ":foo(bar):{test}"
    nodes = parse(input)
    assert len(nodes) == 1
    (node,) = nodes
    assert isinstance(node.data, list)
    assert len(node.data) == 1
    (inner,) = node.data
    assert inner.name == "foo"


def test_named_span_nospace(caplog):
    caplog.set_level(logging.DEBUG)
    input = "a:foo:{b}"
    (node,) = parse(input)
    assert isinstance(node.data, list)
    assert len(node.data) == 2
    a, b = node.data
    assert a.data == "a"
    assert b.name == "foo"
    assert b.data == "b"


def test_empty_named_span(caplog):
    caplog.set_level(logging.DEBUG)
    input = ":foo:{}"
    (node,) = parse(input)
    assert isinstance(node.data, list)
    (named,) = node.data
    assert named.name == "foo"
    assert named.data == ""


def test_timestamp_is_not_named_span(caplog):
    caplog.set_level(logging.DEBUG)
    input = "05:07:13"
    (node,) = parse(input)
    assert isinstance(node.data, list)
    assert "".join(child.data for child in node.data) == "05:07:13"


def test_raw(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        """
        !!code
            a

              *b*
            c

        foo
        """
    )
    nodes = parse(input, iteration_limit=60)
    assert len(nodes) == 2
    (code, _) = nodes
    assert isinstance(code.data, list)
    reconstructed_string = ""
    for node in code.data:
        assert isinstance(node.data, str)
        reconstructed_string += node.data
    assert reconstructed_string == "a\n\n  *b*\nc"


def test_raw_with_introducers(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        r"""
        !!code
            ..d
            ::c
            !!e
        """
    )
    nodes = parse(input, iteration_limit=60)
    assert len(nodes) == 1
    (code,) = nodes
    assert code.data == "..d\n::c\n!!e"


def test_raw_with_named_spans(caplog):
    caplog.set_level(logging.DEBUG)
    input = dedent(
        r"""
        !!code
            \:foo:{a}:foo:{b}
        """
    )
    (code,) = parse(input, iteration_limit=60)
    assert isinstance(code.data, list)
    assert len(code.data) == 2
    (text, foo) = code.data
    assert text.data == ":foo:{a}"
    assert foo.name == "foo"
    assert foo.data == "b"

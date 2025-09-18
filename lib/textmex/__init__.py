import sys

from .html_renderer import HtmlRenderer, RendererConfig
from .htmlgen import Html
from .parser import Node, Parser, UnexpectedToken
from .tokenizer import Tag, Token, Tokenizer

__all__ = [Node, RendererConfig, "parse", "render", "tokenize"]


def tokenize(buffer: str) -> list[Token]:
    tokenizer = Tokenizer(buffer)
    tokens = []
    while True:
        token = tokenizer.next()
        tokens.append(token)
        if token.tag == Tag.eof:
            break
    assert len(tokens) > 0, "tokenizer produced no tokens (should be EOF at least)"
    return tokens


def parse(
    buffer: str,
    *,
    recursion_limit: int | None = None,
    iteration_limit: int | None = None,
) -> list[Node]:
    if recursion_limit is not None:
        sys.setrecursionlimit(recursion_limit)
    tokens = tokenize(buffer)
    parser = Parser(buffer, tokens, iteration_limit=iteration_limit)
    try:
        return parser.parse_document()
    except UnexpectedToken as e:
        unexpected_str = buffer[e.start : e.stop]
        line, col = parser.find_position(e.start)
        e.add_note(f"Unexpected token was {unexpected_str!r} at line {line} col {col}")
        raise


def render(nodes: list[Node], config: RendererConfig) -> Html:
    renderer = HtmlRenderer(config.renderers)
    return renderer.render(nodes)

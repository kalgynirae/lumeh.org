import logging
import sys

from htmlgen import Html

from .html_renderer import HtmlRenderer, RenderConfig
from .parser import Node, Parser, Scope, UnexpectedToken
from .processor import ProcessConfig, SurroundWithConfig, process_children
from .tokenizer import Tag, Token, Tokenizer

__all__ = [Node, RenderConfig, Scope, SurroundWithConfig, "parse", "render", "tokenize"]

logger = logging.getLogger(__name__)


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
    line_number_start: int = 1,
    recursion_limit: int | None = None,
    iteration_limit: int | None = None,
) -> list[Node]:
    if recursion_limit is not None:
        sys.setrecursionlimit(recursion_limit)
    tokens = tokenize(buffer)
    parser = Parser(
        buffer,
        tokens,
        iteration_limit=iteration_limit,
        line_number_start=line_number_start,
    )
    try:
        return parser.parse_document()
    except UnexpectedToken as e:
        unexpected_str = buffer[e.start : e.stop]
        line, col = parser.find_position(e.start)
        e.add_note(f"Unexpected token was {unexpected_str!r} at line {line} col {col}")
        raise


def process(nodes: list[Node], config: ProcessConfig) -> list[Node]:
    return process_children(None, nodes, config)


def render(nodes: list[Node], config: RenderConfig) -> Html:
    renderer = HtmlRenderer(config.render_funcs)
    return Html.joinlines(*renderer.render(nodes))

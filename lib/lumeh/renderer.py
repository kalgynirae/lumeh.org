import re

from htmlgen import Html, html
from textmex import Node, ProcessConfig, RenderConfig, Scope, SurroundWithConfig

process_config = ProcessConfig(
    rename={
        "*": "ingredient",
        "backtick": "amount",
    },
    surround_with={
        "ingredient": SurroundWithConfig(name="ingredient-list", scope=Scope.toplevel),
    },
)
render_config = RenderConfig()


rc = render_config


FRACTION_RE = re.compile(r"\d+(?: \d+)?/\d+")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


@rc.register("amount")
def amount(data: str) -> Html:
    data = data.replace("/", "\N{FRACTION SLASH}")
    return html(t"<span class=amount>{data}</span>")


@rc.register("ingredient")
def ingredient(node: Node, contents: Html) -> Html:
    return html(t"<li>{contents}</li>")


@rc.register("ingredient-list")
def ingredient_list(node: Node, contents: Html) -> Html:
    return html(t"<ul class=ingredients>{contents}</ul>")

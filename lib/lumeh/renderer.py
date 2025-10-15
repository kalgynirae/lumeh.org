import re
from typing import Any

from htmlgen import Html, html, htmlstr
from textmex import Node, ProcessConfig, RenderConfig, Scope

process_config = ProcessConfig(
    rename={
        "*": "ingredient",
        "#": "step",
        "backtick": "amount",
    },
)
process_config.surround(
    ["ingredient"],
    "ingredient-list",
    scope=Scope.toplevel,
)
process_config.surround(
    ["step"],
    "step-list",
    scope=Scope.toplevel,
)
process_config.surround(
    ["author", "time", "yield"],
    "metadata",
    scope=Scope.toplevel,
)

render_config = RenderConfig()
register = render_config.register


@register("bar")
def link(data: str, contents: list[Html], metadata: dict[str, Any]) -> Html:
    url = metadata["links"][data]
    return html(t"<a href={url}>{contents}</a>")


@register("metadata")
def metadata(contents: list[Html]) -> Html:
    return html(t"<div class=recipe-metadata>{Html.joinlines(*contents)}</div>")


@register("author")
def author(data: str) -> Html:
    return html(
        t"<p><span>Author<span class=hidden-text>:</span></span> <span>{data}</span></p>"
    )


@register("time")
def time(data: str) -> Html:
    return html(
        t"<p><span>Time<span class=hidden-text>:</span></span> <span>{data}</span></p>"
    )


@register("yield")
def serves(data: str) -> Html:
    return html(
        t"<p><span>Yield<span class=hidden-text>:</span></span> <span>{data}</span></p>"
    )


@register("recipe-part")
def part(data: str) -> Html:
    return html(t"<h2 class=recipe-part>{data}</h2>")


AMOUNT_RE = re.compile(
    """
        (:?
            (?P<mixednumber>
                \\d+\\ \\d+[/\N{FRACTION SLASH}]\\d+
            ) | (?P<number>
                \\d+(:?[\\./\N{FRACTION SLASH}]\\d+)?
            )
        )
        (
            \\s+
            (?P<unit> [\\w\\s]+ )
        )?
        (:?
            \\s+
            \\((?P<alternates> .* )\\)
        )?
    """,
    re.VERBOSE,
)


@register("amount")
def amount(data: str) -> Html:
    if m := AMOUNT_RE.fullmatch(data):
        parts = []

        if (text := m["mixednumber"]) is not None:
            text = text.replace("/", "\N{FRACTION SLASH}")
            parts.append(html(t"<span class=mixed-number>{text}</span>"))
        else:
            text = m["number"].replace("/", "\N{FRACTION SLASH}")
            parts.append(htmlstr(text))

        parts.append(html(t"<span class=unit>{m['unit']}</span>"))

        if (text := m["alternates"]) is not None:
            text = text.replace("/", "\N{FRACTION SLASH}")
            parts.append(html(t"<span class=alternates>({text})</span>"))

        return Html.join(*parts, sep=htmlstr(" "))
    raise ValueError(f"Failed to parse amount text: {data!r}")


@register("substitutions")
def substitutions(data: str) -> Html:
    return html(
        t"<details class=substitutions><summary><l-icon name=caret-down class=mini></l-icon></summary><p><strong>Substitutions:</strong> {data}</p></details>"
    )


@register("recipe")
def recipe(contents: list[Html]) -> Html:
    return html(t"<div class=hyperchef-recipe>\n{Html.joinlines(*contents)}\n</div>")


@register("inline-tip")
def inline_tip(data: str) -> Html:
    return html(
        t"<details class=inline-tip><summary><l-icon name=info></l-icon></summary><p>{data}</p></details>"
    )


@register("ingredient-list")
def ingredient_list(node: Node, contents: list[Html]) -> Html:
    return html(t"<ul class=ingredient-list>\n{Html.joinlines(*contents)}\n</ul>")


@register("ingredient")
def ingredient(node: Node, contents: list[Html]) -> Html:
    return html(t"<li class=ingredient>{Html.join(*contents)}</li>")


@register("step-list")
def step_list(node: Node, contents: list[Html], *, start: str | None = None) -> Html:
    attrs = {}
    if start:
        attrs["start"] = start
    return html(t"<ol class=step-list{attrs}>\n{Html.joinlines(*contents)}\n</ol>")


@register("step")
def step(node: Node, contents: list[Html], *, start: str | None = None) -> Html:
    return html(t"<li>{Html.join(*contents)}</li>")

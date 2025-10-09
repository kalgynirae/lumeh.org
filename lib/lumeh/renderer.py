from htmlgen import Html, html, htmlstr
from textmex import Node, ProcessConfig, RenderConfig, Scope

process_config = ProcessConfig(
    rename={
        "*": "ingredient",
        "backtick": "amount",
    },
)
process_config.surround(
    ["ingredient"],
    "ingredient-list",
    scope=Scope.toplevel,
)
process_config.surround(
    ["author", "time", "yield"],
    "metadata",
    scope=Scope.toplevel,
)

render_config = RenderConfig()
register = render_config.register


@register("metadata")
def metadata(contents: list[Html]) -> Html:
    inner = Html.join(*contents, sep=html(t"<br>"))
    return html(t"<p class=recipe-metadata>{inner}</p>")


@register("author")
def author(data: str) -> Html:
    return html(
        t"<span><span>Author<span class=hidden-text>:</span></span> <span>{data}</span></span>"
    )


@register("time")
def time(data: str) -> Html:
    return html(
        t"<span><span>Time<span class=hidden-text>:</span></span> <span>{data}</span></span>"
    )


@register("yield")
def serves(data: str) -> Html:
    return html(
        t"<span><span>Yield<span class=hidden-text>:</span></span> <span>{data}</span></span>"
    )


@register("amount")
def amount(data: str) -> Html:
    data = data.replace("/", "\N{FRACTION SLASH}")
    return htmlstr(data)


@register("ingredient")
def ingredient(node: Node, contents: list[Html]) -> Html:
    return html(t"<li>{Html.join(*contents)}</li>")


@register("ingredient-list")
def ingredient_list(node: Node, contents: list[Html]) -> Html:
    return html(t"<ul class=ingredients>\n{Html.joinlines(*contents)}\n</ul>")

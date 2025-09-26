from htmlgen import Html, html, htmlstr
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


register = render_config.register


@register("time")
def time(data: str) -> Html:
    return html(t"<p>Time: {data}</p>")


@register("serves")
def serves(data: str) -> Html:
    return html(t"<p>Serves: {data}</p>")


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

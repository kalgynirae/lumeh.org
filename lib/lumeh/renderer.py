from textmex import RendererConfig, Node
from htmlgen import Html, html

renderer_config = RendererConfig()
rc = renderer_config


@rc.register("foo")
def foo(node: Node) -> Html:
    return html(t"foo")

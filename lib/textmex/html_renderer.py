import functools
import inspect
import logging
from dataclasses import dataclass, field
from types import FunctionType
from typing import Any, Callable, Protocol, TypeVar, cast

from htmlgen import Html, htmlstr, html

from .parser import Node, Scope

type RendererRender = Callable[[list[Node]], Html]
type RenderFunc = Callable[[Node, RendererRender], Html]

Tfunc = TypeVar("Tfunc", bound=FunctionType)


logger = logging.getLogger(__name__)


class BaseRenderFunc(Protocol):
    __name__: str

    def __call__(self, *args, **kwargs) -> Html: ...


def wrap_render_func(func: BaseRenderFunc) -> RenderFunc:
    sig = inspect.signature(func)
    pass_node = False
    pass_data = False
    pass_contents = False
    pass_metadata = False
    required_data_type = None
    for param in sig.parameters.values():
        if param.name == "node":
            pass_node = True
        elif param.name == "data":
            pass_data = True
            if param.annotation is str:
                required_data_type = str
            elif param.annotation == list[Node]:
                required_data_type = list
            else:
                raise TypeError(
                    f"unsupported type annotation for 'data' parameter: {param.annotation}"
                )
        elif param.name == "contents":
            pass_contents = True
        elif param.name == "metadata":
            pass_metadata = True

    @functools.wraps(func)
    def _render_wrapper(
        node: Node, metadata: dict[str, Any], renderer_render: Callable
    ) -> Html:
        if required_data_type is not None:
            if not isinstance(node.data, required_data_type):
                raise TypeError(
                    f"renderer func {func.__name__} expected a node with {required_data_type} data; got {type(node.data)}"
                )
        kwargs = cast(dict[str, Any], node.params.kwargs).copy()
        if pass_node:
            if "node" in kwargs:
                raise RuntimeError("key 'node' already present in kwargs")
            kwargs["node"] = node
        if pass_data:
            if "data" in kwargs:
                raise RuntimeError("key 'data' already present in kwargs")
            kwargs["data"] = node.data
        if pass_contents:
            if "contents" in kwargs:
                raise RuntimeError("key 'contents' already present in kwargs")
            if isinstance(node.data, str):
                contents = [htmlstr(node.data)]
            else:
                contents = renderer_render(node.data, metadata)
            kwargs["contents"] = contents
        if pass_metadata:
            kwargs["metadata"] = metadata
        return func(*node.params.args, **kwargs)

    return _render_wrapper


@wrap_render_func
def render_default(node: Node, contents: list[Html], **kwargs: str) -> Html:
    attrs = {**kwargs}
    if node.name and "class" not in attrs and node.name not in ALL_ELEMENTS:
        attrs["class"] = node.name
    if node.name in VOID_ELEMENTS:
        if str(Html.join(*contents)) != "":
            raise TypeError(
                f"Node name is a void element ({node.name}) but node has contents ({contents})"
            )
        return html(t"<{node.name}{attrs}>")
    elif node.name in NONVOID_ELEMENTS:
        return html(t"<{node.name}{attrs}>{contents}</{node.name}>")
    else:
        if node.name != "":
            logger.warning("No renderer defined for non-element name %r", node.name)
        match node.scope:
            case Scope.inline:
                if attrs:
                    return html(t"<span{attrs}>{contents}</span>")
                else:
                    return Html.join(*contents)
            case Scope.toplevel:
                return html(t"<p{attrs}>{Html.join(*contents)}</p>")
            case Scope.block:
                return html(t"<div{attrs}>{Html.joinlines(*contents)}</div>")
            case _:
                raise TypeError(f"unhandled node.scope value: {node.scope!r}")


@dataclass
class RenderConfig:
    render_funcs: dict[str, RenderFunc] = field(default_factory=dict)

    def register(self, node_name: str) -> Callable[[Tfunc], Tfunc]:
        def _register_renderer(func: Tfunc) -> Tfunc:
            self.render_funcs[node_name] = wrap_render_func(func)
            return func

        return _register_renderer


class HtmlRenderer:
    render_funcs: dict[str, RenderFunc]

    def __init__(self, render_funcs: dict[str, RenderFunc]) -> None:
        self.render_funcs = render_funcs

    def render(self, nodes: list[Node], metadata: dict[str, Any]) -> list[Html]:
        htmls = []
        for node in nodes:
            try:
                render_func = self.render_funcs.get(node.name, render_default)
            except KeyError:
                render_func = self.render_funcs[""]
            htmls.append(render_func(node, metadata, self.render))
        return htmls


VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}

NONVOID_ELEMENTS = {
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "bdi",
    "bdo",
    "blockquote",
    "br",
    "button",
    "canvas",
    "cite",
    "code",
    "data",
    "datalist",
    "del",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "em",
    "embed",
    "fieldset",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hgroup",
    "hr",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "math",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "output",
    "p",
    "picture",
    "pre",
    "progress",
    "q",
    "ruby",
    "s",
    "samp",
    "script",
    "search",
    "section",
    "select",
    "slot",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "svg",
    "table",
    "template",
    "textarea",
    "time",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
}

ALL_ELEMENTS = VOID_ELEMENTS | NONVOID_ELEMENTS

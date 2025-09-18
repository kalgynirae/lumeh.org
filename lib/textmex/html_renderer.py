import functools
import inspect
import logging
from dataclasses import dataclass, field
from types import FunctionType
from typing import Any, Callable, TypeVar, cast

from .htmlgen import Html, htmlstr
from .parser import Node

type RendererFunc = Callable[..., Html]

Tfunc = TypeVar("Tfunc", bound=FunctionType)


logger = logging.getLogger(__name__)


@dataclass
class RendererConfig:
    renderers: dict[str, RendererFunc] = field(default_factory=dict)


class HtmlRenderer:
    renderers: dict[str, RendererFunc]

    def __init__(self, renderers: dict[str, RendererFunc]) -> None:
        self.renderers = renderers

    def register(self, node_name: str) -> Callable[[Tfunc], Tfunc]:
        def _register_renderer(func: Tfunc) -> Tfunc:
            sig = inspect.signature(func)
            pass_node = False
            pass_data = False
            pass_contents = False
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

            @functools.wraps(func)
            def _render_wrapper(node: Node) -> Html:
                if required_data_type is not None:
                    if not isinstance(node.data, required_data_type):
                        raise TypeError(
                            f"renderer for {node_name!r} expected a node with {required_data_type} data; got {type(node.data)}"
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
                        contents = htmlstr(node.data)
                    else:
                        contents = self.render(node.data)
                    kwargs["contents"] = contents
                return func(*node.params.args, **kwargs)

            self.renderers[node_name] = _render_wrapper
            return func

        return _register_renderer

    def render(self, nodes: list[Node]) -> Html:
        htmls = []
        for node in nodes:
            try:
                renderer = self.renderers[node.name]
            except KeyError:
                logger.warning("No renderer registered for node name %r", node.name)
                renderer = self.renderers[""]
            htmls.append(renderer(node))
        return Html.join(*htmls)

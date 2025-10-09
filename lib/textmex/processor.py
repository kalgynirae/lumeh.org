from __future__ import annotations

import logging
from dataclasses import dataclass, field, replace

from .parser import Node, Scope

logger = logging.getLogger(__name__)


@dataclass
class ProcessConfig:
    rename: dict[str, str] = field(default_factory=dict)
    surround_with: dict[str, SurroundWithConfig] = field(default_factory=dict)

    def surround(self, names: list[str], new_parent_name: str, *, scope: Scope) -> None:
        swc = SurroundWithConfig(frozenset(names), new_parent_name, scope)
        for name in names:
            if name in self.surround_with:
                logger.warning(
                    "Overwriting existing surround_with entry for %r (%r) with new entry %r",
                    name,
                    self.surround_with[name],
                    swc,
                )
            self.surround_with[name] = swc


@dataclass
class SurroundWithConfig:
    names: frozenset[str]
    new_parent_name: str
    scope: Scope


def process_node(node: Node, config: ProcessConfig) -> Node:
    node = replace(node, name=config.rename.get(node.name, node.name))
    if isinstance(node.data, list):
        node = replace(node, data=process_children(node, node.data, config))
    return node


def process_children(parent: Node | None, nodes: list[Node], config: ProcessConfig):
    nodes = [process_node(n, config) for n in nodes]
    out = []
    i = 0
    while i < len(nodes):
        node_name = nodes[i].name
        if (surround := config.surround_with.get(node_name)) is not None and (
            (parent.name if parent is not None else "") != surround.new_parent_name
        ):
            collected_nodes = []
            while i < len(nodes) and nodes[i].name in surround.names:
                collected_nodes.append(nodes[i])
                i += 1
            assert len(collected_nodes) > 0
            surround_node = Node(
                name=surround.new_parent_name,
                scope=surround.scope,
                params=collected_nodes[0].params,
                data=collected_nodes,
            )
            out.append(surround_node)
        else:
            out.append(nodes[i])
            i += 1
    return out

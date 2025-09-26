from dataclasses import dataclass, replace
from .parser import Scope, Node


@dataclass
class ProcessConfig:
    rename: dict[str, str]
    surround_with: dict[str, SurroundWithConfig]


@dataclass
class SurroundWithConfig:
    name: str
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
            (parent.name if parent is not None else "") != surround.name
        ):
            collected_nodes = []
            while i < len(nodes) and nodes[i].name == node_name:
                collected_nodes.append(nodes[i])
                i += 1
            assert len(collected_nodes) > 0
            surround_node = Node(
                name=surround.name,
                scope=surround.scope,
                params=collected_nodes[0].params,
                data=collected_nodes,
            )
            out.append(surround_node)
        else:
            out.append(nodes[i])
            i += 1
    return out

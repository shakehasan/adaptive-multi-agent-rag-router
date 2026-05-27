"""Simple task graph representation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphNode:
    """One node in the agent graph."""

    name: str
    depends_on: list[str] = field(default_factory=list)


class AgentGraph:
    """Static graph used for docs, tests, and trace display."""

    def __init__(self) -> None:
        self.nodes = [
            GraphNode("supervisor"),
            GraphNode("planner", ["supervisor"]),
            GraphNode("retrieval", ["planner"]),
            GraphNode("researcher", ["retrieval"]),
            GraphNode("coder", ["planner"]),
            GraphNode("critic", ["researcher", "coder"]),
            GraphNode("verifier", ["critic"]),
            GraphNode("synthesizer", ["verifier"]),
        ]

    def edges(self) -> list[tuple[str, str]]:
        """Return graph edges."""
        result: list[tuple[str, str]] = []
        for node in self.nodes:
            for parent in node.depends_on:
                result.append((parent, node.name))
        return result

    def names(self) -> list[str]:
        """Return node names in declared order."""
        return [node.name for node in self.nodes]

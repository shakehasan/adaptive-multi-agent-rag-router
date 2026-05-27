"""Coding agent for implementation-oriented requests."""

from __future__ import annotations

from .base import BaseAgent
from .state import TaskState


class CodingAgent(BaseAgent):
    """Provide code inspection guidance from local evidence."""

    def __init__(self) -> None:
        super().__init__("coder")

    def run(self, state: TaskState) -> TaskState:
        """Add code-specific findings when needed."""
        lowered = state.query.lower()
        if any(term in lowered for term in ("code", "debug", "function", "class", "test")):
            state.findings.append("Code work should keep typed boundaries, deterministic tests, and explicit local state.")
            state.add_message(self.name, "critic", "code_note", state.findings[-1])
        return state

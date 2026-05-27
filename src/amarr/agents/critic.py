"""Critique agent."""

from __future__ import annotations

from .base import BaseAgent
from .state import TaskState


class CriticAgent(BaseAgent):
    """Identify missing context and weak evidence."""

    def __init__(self) -> None:
        super().__init__("critic")

    def run(self, state: TaskState) -> TaskState:
        """Review evidence and plan quality."""
        if len(state.evidence) < 2:
            state.warnings.append("retrieval returned fewer than two evidence chunks")
        if not state.plan:
            state.warnings.append("plan was missing before critique")
        if not state.warnings:
            state.warnings.append("no critical evidence gaps found")
        state.add_message(self.name, "verifier", "critique", "; ".join(state.warnings))
        return state

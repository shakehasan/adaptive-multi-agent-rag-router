"""Fallback agent for recoverable failures."""

from __future__ import annotations

from amarr.core.types import WorkflowAnswer

from .base import BaseAgent
from .state import TaskState


class FallbackAgent(BaseAgent):
    """Create a safe fallback response when a workflow fails."""

    def __init__(self) -> None:
        super().__init__("fallback")

    def run(self, state: TaskState) -> TaskState:
        """Attach a fallback answer."""
        state.answer = WorkflowAnswer(
            final_answer="The local workflow could not gather enough evidence. Run ingestion and retry the query.",
            citations=[],
            confidence=0.25,
            selected_route=state.route.selected_alias if state.route else "fast_small",
            active_agents=["supervisor", "fallback"],
            verification_notes=["fallback used because the standard workflow did not complete"],
        )
        state.add_message(self.name, "supervisor", "fallback", state.answer.final_answer)
        return state

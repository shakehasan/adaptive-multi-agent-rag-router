"""Planning agent."""

from __future__ import annotations

from .base import BaseAgent
from .state import TaskState


class PlannerAgent(BaseAgent):
    """Decompose a query into workflow steps."""

    def __init__(self) -> None:
        super().__init__("planner")

    def run(self, state: TaskState) -> TaskState:
        """Create a concise plan."""
        state.plan = [
            "classify intent and route task",
            "retrieve local evidence",
            "summarize evidence themes",
            "critique missing context",
            "verify grounding and citations",
            "synthesize final cited answer",
        ]
        if any(term in state.query.lower() for term in ("code", "debug", "function", "class")):
            state.plan.insert(2, "inspect code-specific context")
        state.add_message(self.name, "supervisor", "plan", "\n".join(state.plan))
        return state

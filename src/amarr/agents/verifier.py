"""Verification agent."""

from __future__ import annotations

from amarr.rag.grounding import grounding_score

from .base import BaseAgent
from .state import TaskState


class VerificationAgent(BaseAgent):
    """Check grounding and citation adequacy."""

    def __init__(self) -> None:
        super().__init__("verifier")

    def run(self, state: TaskState) -> TaskState:
        """Verify current findings against evidence."""
        draft = " ".join(state.findings) if state.findings else state.query
        result = grounding_score(draft, state.evidence)
        state.metadata["grounding_score"] = result.score
        state.verification_notes = result.notes + state.warnings
        if result.unsupported_claims:
            state.metadata["unsupported_claims"] = result.unsupported_claims
        state.add_message(self.name, "synthesizer", "verification", "; ".join(state.verification_notes))
        return state

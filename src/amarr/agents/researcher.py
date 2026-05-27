"""Research agent."""

from __future__ import annotations

from amarr.rag.normalization import sentence_split

from .base import BaseAgent
from .state import TaskState


class ResearchAgent(BaseAgent):
    """Summarize retrieved evidence into findings."""

    def __init__(self) -> None:
        super().__init__("researcher")

    def run(self, state: TaskState) -> TaskState:
        """Create evidence-backed findings."""
        findings: list[str] = []
        for item in state.evidence[:5]:
            sentence = sentence_split(item.text)[0] if sentence_split(item.text) else item.preview()
            findings.append(f"{sentence} [{item.chunk_id}]")
        state.findings = findings
        state.add_message(self.name, "critic", "findings", "\n".join(findings))
        return state

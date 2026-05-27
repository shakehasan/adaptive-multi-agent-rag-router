"""Synthesis agent."""

from __future__ import annotations

from amarr.core.types import WorkflowAnswer
from amarr.rag.citations import citations_from_evidence

from .base import BaseAgent
from .state import TaskState


class SynthesisAgent(BaseAgent):
    """Create final cited answers."""

    def __init__(self) -> None:
        super().__init__("synthesizer")

    def run(self, state: TaskState) -> TaskState:
        """Write a grounded response with metadata."""
        citations = citations_from_evidence(state.evidence[:5])
        themes = _derive_themes(state.findings)
        if themes:
            final = (
                "The knowledge base recommends reliable local AI systems that "
                + ", ".join(themes[:5])
                + ". These principles are supported by the cited local evidence."
            )
        else:
            final = (
                "The available local evidence supports using explicit routing, "
                "deterministic fallback, grounded retrieval, verification, and local traces."
            )
        grounding = float(state.metadata.get("grounding_score", 0.7))
        evidence_factor = min(1.0, len(citations) / 5)
        confidence = round(0.55 * grounding + 0.35 * evidence_factor + 0.10, 2)
        selected = state.route.selected_alias if state.route else "fast_small"
        active_agents = ["supervisor", "planner", "retrieval", "researcher", "critic", "verifier", "synthesizer"]
        state.answer = WorkflowAnswer(
            final_answer=final,
            citations=citations,
            confidence=confidence,
            selected_route=selected,
            active_agents=active_agents,
            verification_notes=state.verification_notes,
            metadata={"plan": state.plan, "warnings": state.warnings},
        )
        state.add_message(self.name, "supervisor", "answer", final)
        return state


def _derive_themes(findings: list[str]) -> list[str]:
    """Extract compact design themes from findings."""
    text = " ".join(findings).lower()
    themes: list[str] = []
    if "local" in text:
        themes.append("keep documents, memory, traces, and indexes local")
    if "deterministic" in text or "mock" in text:
        themes.append("use deterministic fallbacks for testing and demos")
    if "routing" in text:
        themes.append("make routing decisions explicit and traceable")
    if "evidence" in text or "cited" in text:
        themes.append("ground answers in cited evidence")
    if "failure" in text or "fallback" in text:
        themes.append("record retries, fallback, and recovery behavior")
    return themes

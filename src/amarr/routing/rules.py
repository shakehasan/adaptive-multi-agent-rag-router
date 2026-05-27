"""Rule-based task classification for routing."""

from __future__ import annotations

from dataclasses import dataclass, field

from amarr.core.types import Capability, TaskKind


@dataclass(slots=True)
class TaskProfile:
    """Router input derived from task text."""

    kind: TaskKind
    complexity: float
    required_capabilities: list[Capability] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


CODING_TERMS = {"code", "function", "class", "debug", "bug", "test", "repository", "module", "script"}
RESEARCH_TERMS = {"design", "architecture", "principles", "recommend", "compare", "evidence", "research"}
VERIFY_TERMS = {"verify", "ground", "cite", "citation", "faithful", "confidence"}


def classify_task(text: str) -> TaskProfile:
    """Classify a task with transparent local rules."""
    lowered = text.lower()
    tokens = set(lowered.replace("?", " ").replace(".", " ").split())
    reasons: list[str] = []
    if tokens & CODING_TERMS:
        reasons.append("code-oriented terms found")
        return TaskProfile(
            kind=TaskKind.CODING,
            complexity=_complexity(text, base=0.55),
            required_capabilities=[Capability.CODE, Capability.DEBUGGING],
            reasons=reasons,
        )
    if tokens & VERIFY_TERMS:
        reasons.append("verification terms found")
        return TaskProfile(
            kind=TaskKind.VERIFICATION,
            complexity=_complexity(text, base=0.6),
            required_capabilities=[Capability.VERIFICATION, Capability.SYNTHESIS],
            reasons=reasons,
        )
    if tokens & RESEARCH_TERMS or len(tokens) > 10:
        reasons.append("research or architecture terms found")
        return TaskProfile(
            kind=TaskKind.RESEARCH,
            complexity=_complexity(text, base=0.7),
            required_capabilities=[Capability.PLANNING, Capability.SYNTHESIS, Capability.VERIFICATION],
            reasons=reasons,
        )
    reasons.append("short utility task")
    return TaskProfile(
        kind=TaskKind.CLASSIFICATION,
        complexity=_complexity(text, base=0.25),
        required_capabilities=[Capability.CLASSIFICATION, Capability.ROUTING],
        reasons=reasons,
    )


def _complexity(text: str, *, base: float) -> float:
    """Estimate complexity from length and structure."""
    words = len(text.split())
    punctuation = sum(1 for ch in text if ch in "?:;")
    score = base + min(0.25, words / 160.0) + min(0.1, punctuation * 0.02)
    return min(1.0, score)

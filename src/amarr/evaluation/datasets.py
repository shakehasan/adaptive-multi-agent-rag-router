"""Evaluation dataset models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EvalItem:
    """One local evaluation item."""

    query: str
    expected_terms: list[str]
    expected_route: str
    metadata: dict[str, str] = field(default_factory=dict)


def default_dataset() -> list[EvalItem]:
    """Return deterministic local eval cases."""
    return [
        EvalItem(
            "What principles guide reliable local AI systems?",
            ["local", "deterministic", "routing", "evidence"],
            "reasoning_large",
        ),
        EvalItem(
            "How should routing fallback be handled?",
            ["fallback", "retries", "circuit", "trace"],
            "reasoning_large",
        ),
        EvalItem(
            "Debug a code path that fails retrieval tests",
            ["test", "debug", "retrieval"],
            "coding_large",
        ),
    ]

"""Evaluation metrics."""

from __future__ import annotations

from amarr.core.types import Evidence, WorkflowAnswer
from amarr.rag.normalization import tokenize


def retrieval_recall(evidence: list[Evidence], expected_terms: list[str]) -> float:
    """Compute expected term recall over retrieved evidence."""
    found = set(tokenize(" ".join(item.text for item in evidence)))
    expected = {term.lower() for term in expected_terms}
    return len(found & expected) / max(1, len(expected))


def citation_precision(answer: WorkflowAnswer) -> float:
    """Estimate citation precision from non-empty citations."""
    if not answer.citations:
        return 0.0
    useful = sum(1 for citation in answer.citations if citation.preview and citation.score > 0)
    return useful / len(answer.citations)


def route_accuracy(selected: str, expected: str) -> float:
    """Return 1 when selected route matches expected."""
    return 1.0 if selected == expected else 0.0


def workflow_success(answer: WorkflowAnswer | None) -> float:
    """Return success score for completed workflows."""
    if answer is None:
        return 0.0
    return 1.0 if answer.final_answer and answer.confidence > 0 else 0.0

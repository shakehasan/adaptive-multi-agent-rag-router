"""RAG evaluation runner."""

from __future__ import annotations

from amarr.core.types import EvaluationSummary
from amarr.rag.retrieval import RetrievalPipeline

from .datasets import EvalItem
from .metrics import retrieval_recall


def evaluate_retrieval(pipeline: RetrievalPipeline, dataset: list[EvalItem]) -> EvaluationSummary:
    """Evaluate retrieval recall."""
    scores: list[float] = []
    notes: list[str] = []
    for item in dataset:
        evidence = pipeline.retrieve(item.query)
        score = retrieval_recall(evidence, item.expected_terms)
        scores.append(score)
        notes.append(f"{item.query}: {score:.2f}")
    average = sum(scores) / max(1, len(scores))
    return EvaluationSummary("rag", {"retrieval_recall": average}, average >= 0.5, notes)

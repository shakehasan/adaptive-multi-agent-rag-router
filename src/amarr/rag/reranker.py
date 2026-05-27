"""Local reranking interface and deterministic fallback."""

from __future__ import annotations

from amarr.core.types import Evidence
from amarr.models.registry import ModelRegistry


def rerank_evidence(query: str, evidence: list[Evidence], registry: ModelRegistry, *, top_k: int) -> list[Evidence]:
    """Rerank evidence using the registered local reranker."""
    if not evidence:
        return []
    scores = registry.rerank(query, [item.text for item in evidence])
    reranked: list[Evidence] = []
    for item, score in zip(evidence, scores):
        reranked.append(Evidence(item.chunk_id, item.source_id, item.text, 0.7 * item.score + 0.3 * score, item.metadata))
    reranked.sort(key=lambda item: item.score, reverse=True)
    return reranked[:top_k]

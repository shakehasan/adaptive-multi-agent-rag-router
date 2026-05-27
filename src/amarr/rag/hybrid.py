"""Hybrid retrieval with reciprocal rank fusion."""

from __future__ import annotations

from amarr.core.types import Evidence
from amarr.models.registry import ModelRegistry

from .keyword_index import KeywordIndex
from .vector_store import VectorStore


def reciprocal_rank_fusion(rankings: list[list[tuple[str, float]]], *, k: int = 60) -> dict[str, float]:
    """Fuse ranked ids with reciprocal rank fusion."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item_id, _score) in enumerate(ranking, start=1):
            fused[item_id] = fused.get(item_id, 0.0) + 1.0 / (k + rank)
    return fused


class HybridRetriever:
    """Combine vector and keyword retrieval."""

    def __init__(self, vector_store: VectorStore, keyword_index: KeywordIndex, registry: ModelRegistry) -> None:
        self.vector_store = vector_store
        self.keyword_index = keyword_index
        self.registry = registry

    def retrieve(self, query: str, *, top_k: int = 8, rerank_top_k: int = 5) -> list[Evidence]:
        """Retrieve fused evidence."""
        query_vector = self.registry.embed([query])[0]
        vector_hits = self.vector_store.search(query_vector, top_k=top_k)
        keyword_hits = self.keyword_index.search(query, top_k=top_k)
        rankings = [
            [(chunk.chunk_id, score) for chunk, score in vector_hits],
            [(chunk.chunk_id, score) for chunk, score in keyword_hits],
        ]
        fused = reciprocal_rank_fusion(rankings)
        chunk_by_id = {chunk.chunk_id: chunk for chunk, _ in vector_hits + keyword_hits}
        evidence = [
            Evidence(
                chunk_id=chunk_id,
                source_id=chunk_by_id[chunk_id].source_id,
                text=chunk_by_id[chunk_id].text,
                score=score,
                metadata=chunk_by_id[chunk_id].metadata,
            )
            for chunk_id, score in fused.items()
            if chunk_id in chunk_by_id
        ]
        evidence.sort(key=lambda item: item.score, reverse=True)
        from .reranker import rerank_evidence

        return rerank_evidence(query, evidence[:top_k], self.registry, top_k=rerank_top_k)

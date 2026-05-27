"""Deterministic mock adapters for tests, demo, and evaluation."""

from __future__ import annotations

import hashlib

from amarr.core.clocks import Stopwatch
from amarr.core.types import HealthStatus
from amarr.rag.embeddings import DeterministicEmbedder

from .base import EmbeddingRequest, EmbeddingResponse, ModelRequest, ModelResponse
from .streaming import chunk_text


class DeterministicMockChatAdapter:
    """Predictable chat adapter that needs no external model."""

    def __init__(self, alias: str) -> None:
        self.alias = alias

    def health(self) -> HealthStatus:
        """Return healthy status."""
        return HealthStatus(name=self.alias, ok=True, detail="mock")

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Return a stable response based on the prompt hash."""
        watch = Stopwatch.start()
        text = request.prompt.joined().lower()
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
        if "plan" in text or "design" in text:
            body = "Plan: classify intent, retrieve local evidence, critique gaps, verify grounding, synthesize cited answer."
        elif "code" in text or "debug" in text:
            body = "Code review: inspect boundaries, validate inputs, test deterministic behavior, keep local state explicit."
        elif "verify" in text:
            body = "Verification: cited evidence supports the main claims with no critical gaps."
        else:
            body = "Local answer: use explicit routing, deterministic fallback, grounded retrieval, and local traces."
        return ModelResponse(
            text=f"{body} [{self.alias}:{digest}]",
            alias=self.alias,
            latency_ms=watch.elapsed_ms(),
            tokens_in=len(text.split()),
            tokens_out=len(body.split()),
        )

    def stream(self, request: ModelRequest):
        """Yield deterministic response chunks."""
        yield from chunk_text(self.complete(request).text)


class MockEmbeddingAdapter:
    """Deterministic embedding adapter."""

    def __init__(self, dimensions: int = 64) -> None:
        self.alias = "retrieval_embedder"
        self.embedder = DeterministicEmbedder(dimensions=dimensions)

    def health(self) -> HealthStatus:
        """Return healthy status."""
        return HealthStatus(self.alias, True, "mock")

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Return deterministic embeddings."""
        watch = Stopwatch.start()
        return EmbeddingResponse(self.embedder.embed_many(request.texts), self.alias, watch.elapsed_ms())


class MockRerankAdapter:
    """Lexical reranker for deterministic local ranking."""

    def __init__(self) -> None:
        self.alias = "rerank_local"

    def health(self) -> HealthStatus:
        """Return healthy status."""
        return HealthStatus(self.alias, True, "mock")

    def rerank(self, query: str, documents: list[str]) -> list[float]:
        """Score documents by query token overlap."""
        terms = {term for term in query.lower().split() if len(term) > 2}
        scores: list[float] = []
        for document in documents:
            tokens = set(document.lower().split())
            overlap = len(terms & tokens)
            scores.append(overlap / max(1, len(terms)))
        return scores

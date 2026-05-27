"""Generic local embedding adapter with deterministic fallback."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

from amarr.core.clocks import Stopwatch
from amarr.core.errors import ModelError
from amarr.core.types import HealthStatus
from amarr.rag.embeddings import DeterministicEmbedder

from .base import EmbeddingRequest, EmbeddingResponse


class GenericLocalEmbeddingAdapter:
    """Adapter for local embeddings with a deterministic fallback."""

    def __init__(self, endpoint: str = "", *, enabled: bool = False, dimensions: int = 64) -> None:
        self.alias = "retrieval_embedder"
        self.endpoint = endpoint.rstrip("/")
        self.enabled = enabled
        self.fallback = DeterministicEmbedder(dimensions=dimensions)

    def health(self) -> HealthStatus:
        """Return health for local mode or fallback mode."""
        if not self.enabled:
            return HealthStatus(self.alias, True, "deterministic fallback")
        parsed = urllib.parse.urlparse(self.endpoint)
        if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            return HealthStatus(self.alias, False, "endpoint is not local")
        return HealthStatus(self.alias, True, "configured")

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Embed text with local endpoint when enabled, otherwise fallback."""
        watch = Stopwatch.start()
        if not self.enabled:
            return EmbeddingResponse(self.fallback.embed_many(request.texts), self.alias, watch.elapsed_ms())
        parsed = urllib.parse.urlparse(self.endpoint)
        if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ModelError("embedding endpoint must be local")
        payload = json.dumps({"texts": request.texts}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.endpoint}/embed",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return EmbeddingResponse(vectors=list(data.get("vectors", [])), alias=self.alias, latency_ms=watch.elapsed_ms())

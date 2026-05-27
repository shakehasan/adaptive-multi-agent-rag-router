"""Base model adapter contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol

from amarr.core.types import HealthStatus

from .messages import ChatPrompt


@dataclass(slots=True)
class ModelRequest:
    """Input for chat or completion adapters."""

    prompt: ChatPrompt
    alias: str
    timeout_seconds: int = 30
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ModelResponse:
    """Output from a model adapter."""

    text: str
    alias: str
    latency_ms: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingRequest:
    """Input for embedding adapters."""

    texts: list[str]
    alias: str = "retrieval_embedder"


@dataclass(slots=True)
class EmbeddingResponse:
    """Output from embedding adapters."""

    vectors: list[list[float]]
    alias: str
    latency_ms: float = 0.0


class ChatAdapter(Protocol):
    """Protocol for chat adapters."""

    alias: str

    def health(self) -> HealthStatus:
        """Return adapter health."""

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Return a non-streaming model response."""

    def stream(self, request: ModelRequest) -> Iterable[str]:
        """Yield response chunks."""


class EmbeddingAdapter(Protocol):
    """Protocol for embedding adapters."""

    alias: str

    def health(self) -> HealthStatus:
        """Return adapter health."""

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Return embeddings."""


class RerankAdapter(Protocol):
    """Protocol for reranking adapters."""

    alias: str

    def health(self) -> HealthStatus:
        """Return adapter health."""

    def rerank(self, query: str, documents: list[str]) -> list[float]:
        """Return one score per document."""

"""Model registry that binds aliases to local adapters."""

from __future__ import annotations

from dataclasses import dataclass, field

from amarr.core.config import AppConfig
from amarr.core.errors import ModelError
from amarr.core.types import HealthStatus, MODEL_ALIASES

from .base import ChatAdapter, EmbeddingAdapter, EmbeddingRequest, RerankAdapter
from .local_chat import GenericLocalChatAdapter
from .local_embedding import GenericLocalEmbeddingAdapter
from .mock import DeterministicMockChatAdapter, MockEmbeddingAdapter, MockRerankAdapter


@dataclass(slots=True)
class ModelRegistry:
    """Registry for chat, embedding, and reranking adapters."""

    chat_adapters: dict[str, ChatAdapter] = field(default_factory=dict)
    embedding_adapter: EmbeddingAdapter | None = None
    rerank_adapter: RerankAdapter | None = None

    @classmethod
    def from_config(cls, config: AppConfig, *, mock: bool = True) -> "ModelRegistry":
        """Create a registry from app configuration."""
        registry = cls()
        for alias in ("reasoning_large", "coding_large", "fast_small"):
            model = config.models[alias]
            if mock or model.type == "mock":
                registry.chat_adapters[alias] = DeterministicMockChatAdapter(alias)
            else:
                registry.chat_adapters[alias] = GenericLocalChatAdapter(
                    alias, model.endpoint, enabled=config.enable_network
                )
        if mock:
            registry.embedding_adapter = MockEmbeddingAdapter()
            registry.rerank_adapter = MockRerankAdapter()
        else:
            registry.embedding_adapter = GenericLocalEmbeddingAdapter(
                config.models["retrieval_embedder"].endpoint,
                enabled=config.enable_network,
            )
            registry.rerank_adapter = MockRerankAdapter()
        return registry

    def register_chat(self, alias: str, adapter: ChatAdapter) -> None:
        """Register a chat adapter."""
        if alias not in MODEL_ALIASES:
            raise ModelError(f"unknown alias: {alias}")
        self.chat_adapters[alias] = adapter

    def chat(self, alias: str) -> ChatAdapter:
        """Return a chat adapter by alias."""
        if alias not in self.chat_adapters:
            raise ModelError(f"chat adapter not registered: {alias}")
        return self.chat_adapters[alias]

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts using the registered embedding adapter."""
        if self.embedding_adapter is None:
            raise ModelError("embedding adapter not registered")
        return self.embedding_adapter.embed(EmbeddingRequest(texts=texts)).vectors

    def rerank(self, query: str, documents: list[str]) -> list[float]:
        """Score documents using the registered rerank adapter."""
        if self.rerank_adapter is None:
            raise ModelError("rerank adapter not registered")
        return self.rerank_adapter.rerank(query, documents)

    def health(self) -> list[HealthStatus]:
        """Return health for all registered adapters."""
        statuses = [adapter.health() for adapter in self.chat_adapters.values()]
        if self.embedding_adapter is not None:
            statuses.append(self.embedding_adapter.health())
        if self.rerank_adapter is not None:
            statuses.append(self.rerank_adapter.health())
        return statuses

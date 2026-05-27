"""High-level retrieval pipeline."""

from __future__ import annotations

from pathlib import Path

from amarr.core.config import AppConfig
from amarr.core.errors import RetrievalError
from amarr.core.types import Evidence
from amarr.models.registry import ModelRegistry

from .hybrid import HybridRetriever
from .keyword_index import KeywordIndex
from .vector_store import VectorStore


class RetrievalPipeline:
    """Load local indexes and retrieve evidence."""

    def __init__(self, config: AppConfig, registry: ModelRegistry) -> None:
        self.config = config
        self.registry = registry
        self.vector_path = Path(config.vector_dir) / "vectors.json"
        self.keyword_path = Path(config.vector_dir) / "keywords.json"

    def ready(self) -> bool:
        """Return whether persisted indexes exist."""
        return self.vector_path.exists() and self.keyword_path.exists()

    def retrieve(self, query: str) -> list[Evidence]:
        """Retrieve evidence for a query."""
        if not self.ready():
            raise RetrievalError("local indexes are missing; run ingest first")
        vector_store = VectorStore.load(self.vector_path)
        keyword_index = KeywordIndex.load(self.keyword_path)
        retriever = HybridRetriever(vector_store, keyword_index, self.registry)
        return retriever.retrieve(
            query,
            top_k=self.config.rag.top_k,
            rerank_top_k=self.config.rag.rerank_top_k,
        )

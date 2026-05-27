"""Document ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry

from .chunking import Chunker
from .keyword_index import KeywordIndex
from .loaders import load_documents
from .vector_store import VectorStore


@dataclass(slots=True)
class IngestionStats:
    """Summary of ingestion work."""

    documents: int
    chunks: int
    vector_path: str
    keyword_path: str


class IngestionPipeline:
    """Load, chunk, embed, and persist local indexes."""

    def __init__(self, config: AppConfig, registry: ModelRegistry) -> None:
        self.config = config
        self.registry = registry
        self.vector_dir = Path(config.vector_dir)
        self.vector_path = self.vector_dir / "vectors.json"
        self.keyword_path = self.vector_dir / "keywords.json"

    def ingest(self, path: str | Path) -> IngestionStats:
        """Ingest documents from a local path."""
        documents = load_documents(path)
        chunker = Chunker(self.config.rag.chunk_size, self.config.rag.chunk_overlap)
        chunks = chunker.split_many(documents)
        vectors = self.registry.embed([chunk.text for chunk in chunks]) if chunks else []
        vector_store = VectorStore()
        vector_store.extend(chunks, vectors)
        keyword_index = KeywordIndex()
        keyword_index.extend(chunks)
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        vector_store.save(self.vector_path)
        keyword_index.save(self.keyword_path)
        return IngestionStats(len(documents), len(chunks), str(self.vector_path), str(self.keyword_path))

"""Simple local vector store backed by JSON."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amarr.core.serialization import dump_json, load_json

from .documents import Chunk
from .embeddings import cosine_similarity


@dataclass(slots=True)
class VectorRecord:
    """Stored vector with chunk payload."""

    chunk: Chunk
    vector: list[float]

    def to_record(self) -> dict[str, Any]:
        """Return JSON-compatible data."""
        return {"chunk": self.chunk.to_record(), "vector": self.vector}

    @classmethod
    def from_record(cls, data: dict[str, Any]) -> "VectorRecord":
        """Create a vector record from JSON data."""
        return cls(Chunk.from_record(data["chunk"]), list(data["vector"]))


class VectorStore:
    """In-memory vector index with JSON persistence."""

    def __init__(self) -> None:
        self.records: list[VectorRecord] = []

    def add(self, chunk: Chunk, vector: list[float]) -> None:
        """Add a vector for a chunk."""
        self.records.append(VectorRecord(chunk=chunk, vector=vector))

    def extend(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Add many chunk vectors."""
        for chunk, vector in zip(chunks, vectors):
            self.add(chunk, vector)

    def search(self, query_vector: list[float], *, top_k: int = 8) -> list[tuple[Chunk, float]]:
        """Return nearest chunks by cosine similarity."""
        scored = [(record.chunk, cosine_similarity(query_vector, record.vector)) for record in self.records]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def save(self, path: Path) -> None:
        """Persist the store to JSON."""
        dump_json(path, [record.to_record() for record in self.records])

    @classmethod
    def load(cls, path: Path) -> "VectorStore":
        """Load a vector store from JSON."""
        store = cls()
        data = load_json(path, []) or []
        store.records = [VectorRecord.from_record(item) for item in data]
        return store

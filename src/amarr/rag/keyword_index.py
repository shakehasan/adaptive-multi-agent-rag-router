"""Keyword index for exact local retrieval."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from amarr.core.serialization import dump_json, load_json

from .documents import Chunk
from .normalization import tokenize


class KeywordIndex:
    """Small BM25-like keyword index."""

    def __init__(self) -> None:
        self.chunks: dict[str, Chunk] = {}
        self.term_freqs: dict[str, Counter[str]] = {}
        self.doc_freqs: Counter[str] = Counter()
        self.lengths: dict[str, int] = {}

    def add(self, chunk: Chunk) -> None:
        """Index one chunk."""
        tokens = tokenize(chunk.text)
        counts = Counter(tokens)
        self.chunks[chunk.chunk_id] = chunk
        self.term_freqs[chunk.chunk_id] = counts
        self.lengths[chunk.chunk_id] = max(1, len(tokens))
        for term in counts:
            self.doc_freqs[term] += 1

    def extend(self, chunks: list[Chunk]) -> None:
        """Index many chunks."""
        for chunk in chunks:
            self.add(chunk)

    def search(self, query: str, *, top_k: int = 8) -> list[tuple[Chunk, float]]:
        """Search by query terms."""
        terms = tokenize(query)
        if not terms:
            return []
        total_docs = max(1, len(self.chunks))
        avg_len = sum(self.lengths.values()) / max(1, len(self.lengths))
        scores: dict[str, float] = defaultdict(float)
        for term in terms:
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                continue
            idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
            for chunk_id, counts in self.term_freqs.items():
                tf = counts.get(term, 0)
                if tf == 0:
                    continue
                length = self.lengths[chunk_id]
                denom = tf + 1.5 * (0.25 + 0.75 * length / max(1.0, avg_len))
                scores[chunk_id] += idf * (tf * 2.5 / denom)
        ranked = [(self.chunks[chunk_id], score) for chunk_id, score in scores.items()]
        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked[:top_k]

    def save(self, path: Path) -> None:
        """Persist indexed chunks."""
        dump_json(path, [chunk.to_record() for chunk in self.chunks.values()])

    @classmethod
    def load(cls, path: Path) -> "KeywordIndex":
        """Load index chunks and rebuild statistics."""
        index = cls()
        data = load_json(path, []) or []
        index.extend([Chunk.from_record(item) for item in data])
        return index

    def stats(self) -> dict[str, Any]:
        """Return index statistics."""
        return {"chunks": len(self.chunks), "terms": len(self.doc_freqs)}

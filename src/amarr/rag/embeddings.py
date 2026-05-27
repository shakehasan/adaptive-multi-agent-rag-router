"""Deterministic local embeddings for offline retrieval."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass

from .normalization import tokenize


@dataclass(slots=True)
class DeterministicEmbedder:
    """Hashing embedder that is stable and free to run locally."""

    dimensions: int = 64

    def embed(self, text: str) -> list[float]:
        """Embed text into a normalized dense vector."""
        vector = [0.0 for _ in range(self.dimensions)]
        for token in tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign * (1.0 + min(len(token), 12) / 12.0)
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Embed many texts."""
        return [self.embed(text) for text in texts]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Compute cosine similarity for normalized vectors."""
    if not left or not right:
        return 0.0
    size = min(len(left), len(right))
    return sum(left[i] * right[i] for i in range(size))

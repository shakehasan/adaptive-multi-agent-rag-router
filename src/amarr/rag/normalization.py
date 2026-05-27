"""Text normalization for reproducible ingestion."""

from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph boundaries."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase alphanumeric terms."""
    return re.findall(r"[a-z0-9_]+", text.lower())


def sentence_split(text: str) -> list[str]:
    """Split text into simple sentence-like units."""
    pieces = re.split(r"(?<=[.!?])\s+", normalize_text(text))
    return [piece.strip() for piece in pieces if piece.strip()]

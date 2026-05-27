"""Streaming helpers used by adapters and tests."""

from __future__ import annotations

from collections.abc import Iterable


def chunk_text(text: str, *, size: int = 48) -> Iterable[str]:
    """Yield text chunks with stable boundaries."""
    for index in range(0, len(text), size):
        yield text[index : index + size]


def collect_stream(chunks: Iterable[str]) -> str:
    """Collect a stream of chunks into a string."""
    return "".join(chunks)

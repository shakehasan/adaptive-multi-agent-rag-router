"""Memory summarization helpers."""

from __future__ import annotations

from amarr.rag.normalization import sentence_split


def summarize_texts(texts: list[str], *, max_sentences: int = 5) -> str:
    """Create a compact extractive summary."""
    sentences: list[str] = []
    for text in texts:
        sentences.extend(sentence_split(text))
    unique: list[str] = []
    seen: set[str] = set()
    for sentence in sentences:
        key = sentence.lower()
        if key not in seen:
            unique.append(sentence)
            seen.add(key)
        if len(unique) >= max_sentences:
            break
    return " ".join(unique)

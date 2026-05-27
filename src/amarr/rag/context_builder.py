"""Build bounded context blocks from retrieved evidence."""

from __future__ import annotations

from amarr.core.types import Evidence


def build_context(evidence: list[Evidence], *, max_chars: int = 3200) -> str:
    """Build a context string with chunk ids and source ids."""
    parts: list[str] = []
    used = 0
    for item in evidence:
        block = f"[{item.chunk_id}] {item.text.strip()}"
        if used + len(block) > max_chars:
            break
        parts.append(block)
        used += len(block)
    return "\n\n".join(parts)


def evidence_table(evidence: list[Evidence]) -> list[dict[str, object]]:
    """Return evidence display rows for the API and demo."""
    return [
        {
            "chunk_id": item.chunk_id,
            "source_id": item.source_id,
            "score": round(item.score, 4),
            "preview": item.preview(),
        }
        for item in evidence
    ]

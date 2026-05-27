"""Citation formatting and source attribution."""

from __future__ import annotations

from amarr.core.types import Citation, Evidence


def citations_from_evidence(evidence: list[Evidence]) -> list[Citation]:
    """Create citations from retrieved evidence."""
    citations: list[Citation] = []
    seen: set[str] = set()
    for item in evidence:
        key = item.chunk_id
        if key in seen:
            continue
        seen.add(key)
        citations.append(Citation(item.source_id, item.chunk_id, item.score, item.preview()))
    return citations


def inline_citation_list(citations: list[Citation]) -> str:
    """Return a compact inline citation list."""
    if not citations:
        return "no citations"
    return ", ".join(citation.chunk_id for citation in citations)

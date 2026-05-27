"""Retrieval quality diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field

from amarr.core.types import Evidence

from .normalization import tokenize


@dataclass(slots=True)
class RetrievalQuality:
    """Diagnostic quality scores for a retrieval result."""

    diversity: float
    average_score: float
    term_coverage: float
    source_count: int
    notes: list[str] = field(default_factory=list)

    def overall(self) -> float:
        """Combine quality dimensions."""
        return round(0.30 * self.diversity + 0.35 * self.average_score + 0.35 * self.term_coverage, 3)


def source_diversity(evidence: list[Evidence]) -> float:
    """Measure how many distinct sources are represented."""
    if not evidence:
        return 0.0
    return len({item.source_id for item in evidence}) / len(evidence)


def average_score(evidence: list[Evidence]) -> float:
    """Return average normalized evidence score."""
    if not evidence:
        return 0.0
    top = max(item.score for item in evidence) or 1.0
    return sum(item.score / top for item in evidence) / len(evidence)


def query_term_coverage(query: str, evidence: list[Evidence]) -> float:
    """Measure query term coverage in evidence."""
    query_terms = {term for term in tokenize(query) if len(term) > 3}
    if not query_terms:
        return 1.0
    evidence_terms = set(tokenize(" ".join(item.text for item in evidence)))
    return len(query_terms & evidence_terms) / len(query_terms)


def diagnose_retrieval(query: str, evidence: list[Evidence]) -> RetrievalQuality:
    """Create a retrieval quality report."""
    quality = RetrievalQuality(
        diversity=source_diversity(evidence),
        average_score=average_score(evidence),
        term_coverage=query_term_coverage(query, evidence),
        source_count=len({item.source_id for item in evidence}),
    )
    if not evidence:
        quality.notes.append("no evidence returned")
    if quality.diversity < 0.3 and len(evidence) > 2:
        quality.notes.append("evidence is concentrated in a small number of sources")
    if quality.term_coverage < 0.4:
        quality.notes.append("query terms are weakly covered")
    if not quality.notes:
        quality.notes.append("retrieval quality is acceptable")
    return quality


def quality_markdown(query: str, evidence: list[Evidence]) -> str:
    """Render retrieval quality diagnostics."""
    quality = diagnose_retrieval(query, evidence)
    lines = [
        "### Retrieval Quality",
        "",
        f"- diversity: {quality.diversity:.2f}",
        f"- average_score: {quality.average_score:.2f}",
        f"- term_coverage: {quality.term_coverage:.2f}",
        f"- source_count: {quality.source_count}",
        f"- overall: {quality.overall():.2f}",
        "",
    ]
    lines.extend(f"- {note}" for note in quality.notes)
    return "\n".join(lines)

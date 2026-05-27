"""Grounding and faithfulness checks."""

from __future__ import annotations

from dataclasses import dataclass, field

from amarr.core.types import Evidence

from .normalization import sentence_split, tokenize


@dataclass(slots=True)
class GroundingResult:
    """Result of checking answer support against evidence."""

    score: float
    notes: list[str] = field(default_factory=list)
    unsupported_claims: list[str] = field(default_factory=list)


def grounding_score(answer: str, evidence: list[Evidence]) -> GroundingResult:
    """Estimate whether answer claims are supported by evidence."""
    evidence_terms = set(tokenize(" ".join(item.text for item in evidence)))
    sentences = sentence_split(answer)
    if not sentences:
        return GroundingResult(0.0, ["empty answer"], [])
    supported = 0
    unsupported: list[str] = []
    for sentence in sentences:
        terms = [term for term in tokenize(sentence) if len(term) > 3]
        if not terms:
            supported += 1
            continue
        overlap = sum(1 for term in terms if term in evidence_terms)
        ratio = overlap / max(1, len(terms))
        if ratio >= 0.25:
            supported += 1
        else:
            unsupported.append(sentence)
    score = supported / max(1, len(sentences))
    notes = ["all major claims are supported by cited evidence"] if score >= 0.75 else ["some claims need stronger evidence"]
    return GroundingResult(score=score, notes=notes, unsupported_claims=unsupported)

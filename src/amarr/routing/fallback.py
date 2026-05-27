"""Fallback route selection."""

from __future__ import annotations

from .circuit_breaker import CircuitBreaker
from .decisions import RouteCandidate


def choose_fallback(candidates: list[RouteCandidate], breaker: CircuitBreaker, preferred: str) -> RouteCandidate:
    """Choose the next healthy candidate."""
    ordered = sorted(candidates, key=lambda item: (item.alias != preferred, -item.total_score))
    for candidate in ordered:
        if candidate.stability_score > 0 and breaker.allow(candidate.alias):
            return candidate
    for candidate in candidates:
        if breaker.allow(candidate.alias):
            return candidate
    raise ValueError("no fallback route available")

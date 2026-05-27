"""Routing policies that select from scored candidates."""

from __future__ import annotations

from .decisions import RouteCandidate


def apply_policy(candidates: list[RouteCandidate], policy: str) -> RouteCandidate:
    """Return the selected candidate for a policy."""
    if not candidates:
        raise ValueError("no route candidates")
    if policy == "quality":
        return max(candidates, key=lambda item: (item.capability_score, item.stability_score, item.total_score))
    if policy == "economy":
        viable = [item for item in candidates if item.capability_score >= 0.5 and item.stability_score > 0]
        if viable:
            return max(viable, key=lambda item: (item.speed_score, item.total_score))
    return max(candidates, key=lambda item: item.total_score)


def policy_reason(candidate: RouteCandidate, policy: str) -> str:
    """Return a human-readable policy reason."""
    return (
        f"{policy} policy selected {candidate.alias} with score "
        f"{candidate.total_score:.2f} ({', '.join(candidate.reasons)})"
    )

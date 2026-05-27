"""Route explanation utilities."""

from __future__ import annotations

from .decisions import RouteCandidate, RouteDecision


def explain_candidate(candidate: RouteCandidate) -> str:
    """Explain a candidate score."""
    return (
        f"{candidate.alias}: total={candidate.total_score:.3f}, "
        f"capability={candidate.capability_score:.3f}, "
        f"speed={candidate.speed_score:.3f}, stability={candidate.stability_score:.3f}"
    )


def explain_decision(decision: RouteDecision) -> str:
    """Render a route decision explanation."""
    lines = [
        f"decision: {decision.decision_id}",
        f"task: {decision.task_kind}",
        f"selected: {decision.selected_alias}",
        f"policy: {decision.policy}",
        f"fallback: {decision.fallback_used}",
        f"reason: {decision.reason}",
        "",
        "candidates:",
    ]
    lines.extend(f"- {explain_candidate(candidate)}" for candidate in decision.candidates)
    return "\n".join(lines)


def route_confidence(decision: RouteDecision) -> float:
    """Estimate route confidence from margin and fallback state."""
    if not decision.candidates:
        return 0.0
    ordered = sorted(decision.candidates, key=lambda item: item.total_score, reverse=True)
    best = ordered[0].total_score
    second = ordered[1].total_score if len(ordered) > 1 else 0.0
    margin = max(0.0, best - second)
    fallback_penalty = 0.2 if decision.fallback_used else 0.0
    return max(0.0, min(1.0, 0.55 + margin - fallback_penalty))


def route_table(decisions: list[RouteDecision]) -> str:
    """Render decisions as a Markdown table."""
    lines = ["| task | selected | policy | confidence |", "| --- | --- | --- | ---: |"]
    for decision in decisions:
        lines.append(
            f"| {decision.task_kind} | {decision.selected_alias} | "
            f"{decision.policy} | {route_confidence(decision):.2f} |"
        )
    return "\n".join(lines)

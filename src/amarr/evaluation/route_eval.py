"""Route evaluation runner."""

from __future__ import annotations

from amarr.core.types import EvaluationSummary
from amarr.routing.router import Router

from .datasets import EvalItem
from .metrics import route_accuracy


def evaluate_routes(router: Router, dataset: list[EvalItem]) -> EvaluationSummary:
    """Evaluate route choices."""
    scores: list[float] = []
    notes: list[str] = []
    for item in dataset:
        selected = router.route(item.query).selected_alias
        score = route_accuracy(selected, item.expected_route)
        scores.append(score)
        notes.append(f"{selected} expected {item.expected_route}: {score:.2f}")
    average = sum(scores) / max(1, len(scores))
    return EvaluationSummary("routing", {"route_accuracy": average}, average >= 0.66, notes)

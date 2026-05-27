"""Agent workflow evaluation."""

from __future__ import annotations

from amarr.agents.executor import run_query
from amarr.core.config import AppConfig
from amarr.core.types import EvaluationSummary
from amarr.models.registry import ModelRegistry

from .datasets import EvalItem
from .metrics import citation_precision, workflow_success


def evaluate_agent_workflow(config: AppConfig, registry: ModelRegistry, dataset: list[EvalItem]) -> EvaluationSummary:
    """Evaluate end-to-end agent workflow."""
    successes: list[float] = []
    citation_scores: list[float] = []
    notes: list[str] = []
    for item in dataset:
        state = run_query(item.query, config, registry)
        successes.append(workflow_success(state.answer))
        citation_scores.append(citation_precision(state.answer) if state.answer else 0.0)
        notes.append(f"{item.query}: agents={len(state.messages)} confidence={state.answer.confidence if state.answer else 0:.2f}")
    return EvaluationSummary(
        "agents",
        {
            "workflow_success": sum(successes) / max(1, len(successes)),
            "citation_precision": sum(citation_scores) / max(1, len(citation_scores)),
        },
        bool(successes) and min(successes) >= 1.0,
        notes,
    )

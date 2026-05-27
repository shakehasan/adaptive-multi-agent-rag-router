"""Main model router."""

from __future__ import annotations

from pathlib import Path

from amarr.core.config import AppConfig
from amarr.core.errors import RoutingError
from amarr.models.registry import ModelRegistry

from .circuit_breaker import CircuitBreaker
from .decisions import RouteDecision
from .fallback import choose_fallback
from .policies import apply_policy, policy_reason
from .rules import classify_task
from .scoring import score_candidates
from .telemetry import RouteTelemetry


class Router:
    """Route tasks to neutral local aliases."""

    def __init__(self, config: AppConfig, registry: ModelRegistry) -> None:
        self.config = config
        self.registry = registry
        self.breaker = CircuitBreaker()
        self.telemetry = RouteTelemetry(Path(config.storage_dir) / "routes.json")

    def route(self, text: str, *, policy: str | None = None) -> RouteDecision:
        """Return a route decision for task text."""
        profile = classify_task(text)
        candidates = score_candidates(profile, self.registry)
        if not candidates:
            raise RoutingError("no route candidates")
        active_policy = policy or self.config.routing.default_policy
        selected = apply_policy(candidates, active_policy)
        fallback_used = False
        if selected.stability_score <= 0 or not self.breaker.allow(selected.alias):
            selected = choose_fallback(candidates, self.breaker, self.config.routing.fallback_model)
            fallback_used = True
        decision = RouteDecision(
            task_kind=profile.kind.value,
            selected_alias=selected.alias,
            policy=active_policy,
            reason=policy_reason(selected, active_policy),
            candidates=candidates,
            fallback_used=fallback_used,
            metadata={"complexity": profile.complexity, "profile_reasons": profile.reasons},
        )
        self.telemetry.record(decision)
        return decision

    def record_success(self, alias: str) -> None:
        """Record successful use of an alias."""
        self.breaker.record_success(alias)

    def record_failure(self, alias: str) -> None:
        """Record failed use of an alias."""
        self.breaker.record_failure(alias)

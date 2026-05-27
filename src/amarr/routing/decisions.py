"""Route decision value objects."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from amarr.core.clocks import utc_ms
from amarr.core.ids import new_id


@dataclass(slots=True)
class RouteCandidate:
    """One model alias candidate."""

    alias: str
    capability_score: float
    speed_score: float
    stability_score: float
    total_score: float
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RouteDecision:
    """Structured route decision log."""

    task_kind: str
    selected_alias: str
    policy: str
    reason: str
    candidates: list[RouteCandidate]
    fallback_used: bool = False
    attempts: int = 1
    decision_id: str = field(default_factory=lambda: new_id("route"))
    timestamp_ms: int = field(default_factory=utc_ms)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        """Return a JSON-compatible record."""
        return {
            "decision_id": self.decision_id,
            "task_kind": self.task_kind,
            "selected_alias": self.selected_alias,
            "policy": self.policy,
            "reason": self.reason,
            "fallback_used": self.fallback_used,
            "attempts": self.attempts,
            "timestamp_ms": self.timestamp_ms,
                "candidates": [asdict(candidate) for candidate in self.candidates],
            "metadata": self.metadata,
        }

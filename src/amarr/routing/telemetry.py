"""Local route decision telemetry."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from amarr.core.serialization import dump_json, load_json

from .decisions import RouteDecision


@dataclass(slots=True)
class RouteTelemetry:
    """Append route decisions to local state."""

    path: Path
    decisions: list[RouteDecision] = field(default_factory=list)

    def record(self, decision: RouteDecision) -> None:
        """Record a decision in memory and on disk."""
        self.decisions.append(decision)
        existing = load_json(self.path, []) or []
        existing.append(decision.to_record())
        dump_json(self.path, existing)

    def latest(self) -> RouteDecision | None:
        """Return latest in-memory decision."""
        return self.decisions[-1] if self.decisions else None

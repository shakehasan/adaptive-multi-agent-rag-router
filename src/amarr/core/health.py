"""Local health aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .types import HealthStatus


@dataclass(slots=True)
class HealthReport:
    """Aggregate health report for local components."""

    statuses: list[HealthStatus] = field(default_factory=list)

    def ok(self) -> bool:
        """Return true when all statuses are healthy."""
        return all(status.ok for status in self.statuses)

    def add(self, status: HealthStatus) -> None:
        """Append a status."""
        self.statuses.append(status)

    def summary(self) -> dict[str, object]:
        """Return JSON-compatible summary."""
        return {
            "ok": self.ok(),
            "total": len(self.statuses),
            "healthy": sum(1 for status in self.statuses if status.ok),
            "unhealthy": [status.name for status in self.statuses if not status.ok],
        }


def storage_health(storage_dir: Path, vector_dir: Path, trace_dir: Path) -> list[HealthStatus]:
    """Return health statuses for local storage directories."""
    statuses: list[HealthStatus] = []
    for name, path in [("storage", storage_dir), ("vector", vector_dir), ("traces", trace_dir)]:
        try:
            path.mkdir(parents=True, exist_ok=True)
            statuses.append(HealthStatus(name, path.exists() and path.is_dir(), str(path)))
        except OSError as exc:
            statuses.append(HealthStatus(name, False, str(exc)))
    return statuses


def render_health_table(report: HealthReport) -> str:
    """Render health statuses as a compact text table."""
    rows = ["component | ok | detail", "--- | --- | ---"]
    for status in report.statuses:
        rows.append(f"{status.name} | {status.ok} | {status.detail}")
    return "\n".join(rows)

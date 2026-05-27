"""Latency metric helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LatencyStats:
    """Latency summary values."""

    minimum_ms: float
    p50_ms: float
    p90_ms: float
    maximum_ms: float
    count: int

    def to_metrics(self) -> dict[str, float]:
        """Return metrics dictionary."""
        return {
            "latency_min_ms": self.minimum_ms,
            "latency_p50_ms": self.p50_ms,
            "latency_p90_ms": self.p90_ms,
            "latency_max_ms": self.maximum_ms,
            "latency_count": float(self.count),
        }


def percentile(values: list[float], pct: float) -> float:
    """Compute a simple percentile."""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100.0) * (len(ordered) - 1))))
    return ordered[index]


def latency_stats(values: list[float]) -> LatencyStats:
    """Compute latency stats."""
    if not values:
        return LatencyStats(0.0, 0.0, 0.0, 0.0, 0)
    return LatencyStats(
        minimum_ms=min(values),
        p50_ms=percentile(values, 50),
        p90_ms=percentile(values, 90),
        maximum_ms=max(values),
        count=len(values),
    )

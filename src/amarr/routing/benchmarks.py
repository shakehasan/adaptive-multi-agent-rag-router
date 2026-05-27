"""Local routing benchmark scenarios."""

from __future__ import annotations

from dataclasses import dataclass

from .router import Router


@dataclass(slots=True)
class RoutingBenchmarkResult:
    """Result for one benchmark case."""

    query: str
    expected: str
    selected: str
    passed: bool


CASES: list[tuple[str, str]] = [
    ("Summarize this short note", "fast_small"),
    ("Debug this function and explain the failing test", "coding_large"),
    ("What design principles guide reliable local AI systems?", "reasoning_large"),
    ("Verify whether these claims are supported by the citations", "reasoning_large"),
]


def run_routing_benchmark(router: Router) -> list[RoutingBenchmarkResult]:
    """Run deterministic route benchmark cases."""
    results: list[RoutingBenchmarkResult] = []
    for query, expected in CASES:
        selected = router.route(query).selected_alias
        results.append(RoutingBenchmarkResult(query, expected, selected, selected == expected))
    return results

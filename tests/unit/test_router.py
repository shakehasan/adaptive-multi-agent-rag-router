"""Router unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.routing.benchmarks import run_routing_benchmark
from amarr.routing.circuit_breaker import CircuitBreaker
from amarr.routing.router import Router
from amarr.routing.rules import classify_task


class RouterTests(unittest.TestCase):
    """Validate routing decisions and fallback behavior."""

    def make_router(self) -> Router:
        self.tmp = tempfile.TemporaryDirectory()
        config = AppConfig.defaults()
        config.storage_dir = str(Path(self.tmp.name) / "state")
        config.vector_dir = str(Path(self.tmp.name) / "state" / "vector")
        registry = ModelRegistry.from_config(config, mock=True)
        return Router(config, registry)

    def tearDown(self) -> None:
        if hasattr(self, "tmp"):
            self.tmp.cleanup()

    def test_research_routes_to_reasoning_alias(self) -> None:
        router = self.make_router()
        decision = router.route("What design principles guide reliable local AI systems?")
        self.assertEqual(decision.selected_alias, "reasoning_large")
        self.assertFalse(decision.fallback_used)
        self.assertGreater(decision.candidates[0].total_score, 0.0)

    def test_coding_routes_to_coding_alias(self) -> None:
        router = self.make_router()
        decision = router.route("Debug this code path and inspect the failing test")
        self.assertEqual(decision.selected_alias, "coding_large")

    def test_short_task_routes_to_fast_alias(self) -> None:
        router = self.make_router()
        decision = router.route("Summarize note")
        self.assertEqual(decision.selected_alias, "fast_small")

    def test_profile_contains_reasons(self) -> None:
        profile = classify_task("Verify the citation grounding and confidence")
        self.assertEqual(profile.kind.value, "verification")
        self.assertTrue(profile.reasons)

    def test_circuit_breaker_opens(self) -> None:
        breaker = CircuitBreaker(failure_threshold=2, recovery_seconds=100)
        self.assertTrue(breaker.allow("fast_small"))
        breaker.record_failure("fast_small")
        self.assertTrue(breaker.allow("fast_small"))
        breaker.record_failure("fast_small")
        self.assertFalse(breaker.allow("fast_small"))

    def test_benchmark_passes_core_cases(self) -> None:
        router = self.make_router()
        results = run_routing_benchmark(router)
        self.assertGreaterEqual(sum(1 for item in results if item.passed), 3)


if __name__ == "__main__":
    unittest.main()

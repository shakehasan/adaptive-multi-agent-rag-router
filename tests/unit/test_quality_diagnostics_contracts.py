"""Quality, diagnostics, and contract tests."""

from __future__ import annotations

import unittest

from amarr.agents.recovery import plan_recovery
from amarr.core.types import Evidence
from amarr.evaluation.diagnostics import diagnose_metrics, interpret_metric
from amarr.evaluation.latency import latency_stats, percentile
from amarr.models.contracts import CHAT_CONTRACT, all_contracts
from amarr.observability.audit import AuditRecord, summarize_audit
from amarr.rag.metadata import extract_front_matter, extract_headings, infer_tags
from amarr.rag.quality import diagnose_retrieval, quality_markdown
from amarr.routing.explain import explain_decision, route_confidence
from amarr.routing.router import Router
from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry


class QualityDiagnosticsContractsTests(unittest.TestCase):
    """Validate expanded architecture utilities."""

    def test_endpoint_contracts_validate_shape(self) -> None:
        issues = CHAT_CONTRACT.validate_request({"messages": [], "temperature": 0, "max_tokens": 10})
        self.assertEqual(issues, [])
        self.assertTrue(all_contracts())
        self.assertIn("local_chat", CHAT_CONTRACT.markdown())

    def test_metadata_extraction(self) -> None:
        text = "---\ntag: local\n---\n# Title\n\nRouting evidence and fallback."
        self.assertEqual(extract_front_matter(text)["tag"], "local")
        self.assertEqual(extract_headings(text), ["Title"])
        self.assertIn("routing", infer_tags(text))

    def test_retrieval_quality(self) -> None:
        evidence = [
            Evidence("a", "s1", "local routing evidence citation", 0.9),
            Evidence("b", "s2", "verification confidence evidence", 0.7),
        ]
        quality = diagnose_retrieval("local routing confidence", evidence)
        self.assertGreater(quality.overall(), 0.0)
        self.assertIn("Retrieval Quality", quality_markdown("local routing confidence", evidence))

    def test_recovery_plan(self) -> None:
        plan = plan_recovery("missing index and route alias timeout")
        actions = [step.action for step in plan.steps]
        self.assertIn("rebuild local indexes", actions)
        self.assertIn("select fallback alias", actions)
        self.assertTrue(plan.retryable_steps())

    def test_metric_diagnostics(self) -> None:
        band = interpret_metric(0.92)
        self.assertEqual(band.name, "excellent")
        report = diagnose_metrics({"retrieval_recall": 0.4, "route_accuracy": 0.95})
        self.assertTrue(report.action_items)
        self.assertIn("retrieval_recall", report.markdown())

    def test_latency_stats(self) -> None:
        self.assertEqual(percentile([1, 2, 3], 50), 2)
        stats = latency_stats([10, 20, 30, 40])
        self.assertEqual(stats.count, 4)
        self.assertIn("latency_p50_ms", stats.to_metrics())

    def test_audit_records(self) -> None:
        record = AuditRecord("planner", "prompt 1234567890123", "response", "fast_small", ["plan"])
        redacted = record.redacted()
        self.assertIn("[redacted-number]", redacted.prompt)
        summary = summarize_audit([record])
        self.assertEqual(summary["by_route"]["fast_small"], 1)

    def test_route_explanation(self) -> None:
        config = AppConfig.defaults()
        registry = ModelRegistry.from_config(config, mock=True)
        router = Router(config, registry)
        decision = router.route("What design principles guide reliable local AI systems?")
        self.assertIn(decision.selected_alias, explain_decision(decision))
        self.assertGreater(route_confidence(decision), 0.0)


if __name__ == "__main__":
    unittest.main()

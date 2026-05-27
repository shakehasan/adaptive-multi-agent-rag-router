"""Evaluation unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.core.config import AppConfig
from amarr.core.types import Citation, Evidence, WorkflowAnswer
from amarr.evaluation.datasets import default_dataset
from amarr.evaluation.metrics import citation_precision, retrieval_recall, route_accuracy, workflow_success
from amarr.evaluation.reports import write_reports


class EvaluationTests(unittest.TestCase):
    """Validate local metrics and reports."""

    def test_metrics(self) -> None:
        evidence = [Evidence("c1", "s1", "local deterministic routing evidence", 1.0)]
        self.assertEqual(retrieval_recall(evidence, ["local", "routing"]), 1.0)
        answer = WorkflowAnswer("answer", [Citation("s1", "c1", 1.0, "preview")], 0.8, "reasoning_large", [], [])
        self.assertEqual(citation_precision(answer), 1.0)
        self.assertEqual(route_accuracy("fast_small", "fast_small"), 1.0)
        self.assertEqual(workflow_success(answer), 1.0)

    def test_default_dataset(self) -> None:
        dataset = default_dataset()
        self.assertGreaterEqual(len(dataset), 3)
        self.assertTrue(dataset[0].expected_terms)

    def test_report_writing(self) -> None:
        from amarr.core.types import EvaluationSummary

        with tempfile.TemporaryDirectory() as tmp:
            json_path, md_path = write_reports([EvaluationSummary("x", {"score": 1.0}, True)], Path(tmp))
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())


if __name__ == "__main__":
    unittest.main()

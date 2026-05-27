"""Observability unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.observability.local_viewer import render_trace_html
from amarr.observability.redaction import redact_text
from amarr.observability.timeline import spans_to_timeline
from amarr.observability.traces import TraceStore


class ObservabilityTests(unittest.TestCase):
    """Validate traces, redaction, and viewer output."""

    def test_trace_store_writes_latest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = TraceStore(Path(tmp))
            with store.span("query", "workflow", "detail"):
                pass
            path = store.write()
            self.assertTrue(path.exists())
            latest = store.latest()
            self.assertIsNotNone(latest)

    def test_redaction(self) -> None:
        redacted = redact_text("number 1234567890123 and term alpha", ["alpha"])
        self.assertIn("[redacted-number]", redacted)
        self.assertIn("[redacted-term]", redacted)

    def test_timeline_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = TraceStore(Path(tmp))
            with store.span("route", "routing", "ok"):
                pass
            rows = spans_to_timeline(store.spans)
            self.assertEqual(rows[0]["name"], "route")
            html = render_trace_html({"spans": rows})
            self.assertIn("Local Trace", html)


if __name__ == "__main__":
    unittest.main()

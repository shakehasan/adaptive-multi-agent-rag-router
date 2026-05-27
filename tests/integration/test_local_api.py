"""Local API integration test."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from amarr.app.dependencies import AppContext
from amarr.app.server import make_handler
from amarr.core.config import AppConfig

class LocalApiTests(unittest.TestCase):
    def test_context_query_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "a.md").write_text("# A\n\nLocal API queries return answers with route and evidence metadata.", encoding="utf-8")
            config = AppConfig.defaults()
            config.storage_dir = str(root / "state")
            config.vector_dir = str(root / "state" / "vector")
            config.observability.trace_dir = str(root / "state" / "traces")
            context = AppContext(config, mock=True)
            context.ingest(str(docs))
            result = context.query("What does the local API return?")
            self.assertIn("answer", result)
            self.assertIn("route", result)
            self.assertIn("trace_events", result)

    def test_handler_factory(self) -> None:
        config = AppConfig.defaults()
        context = AppContext(config, mock=True)
        handler = make_handler(context)
        self.assertTrue(handler.__name__.endswith("Handler"))

if __name__ == "__main__":
    unittest.main()

"""CLI command tests."""

from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from amarr.cli.main import build_parser, main
from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.ingestion import IngestionPipeline
from amarr.routing.benchmarks import CASES


class CliCommandTests(unittest.TestCase):
    """Validate CLI parser and command-level behavior."""

    def test_parser_contains_expected_commands(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertIn("ingest", help_text)
        self.assertIn("benchmark-routing", help_text)
        self.assertIn("serve", help_text)

    def test_inspect_config_command(self) -> None:
        with redirect_stdout(StringIO()):
            code = main(["inspect", "config"])
        self.assertEqual(code, 0)

    def test_benchmark_cases_are_present(self) -> None:
        self.assertGreaterEqual(len(CASES), 4)
        self.assertIn("fast_small", {expected for _query, expected in CASES})

    def test_ingest_command_with_temp_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "a.md").write_text("# A\n\nlocal routing evidence", encoding="utf-8")
            config = AppConfig.defaults()
            config.storage_dir = str(root / "state")
            config.vector_dir = str(root / "state" / "vector")
            registry = ModelRegistry.from_config(config, mock=True)
            stats = IngestionPipeline(config, registry).ingest(docs)
            self.assertEqual(stats.documents, 1)


if __name__ == "__main__":
    unittest.main()

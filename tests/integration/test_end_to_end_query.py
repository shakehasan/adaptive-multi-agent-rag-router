"""End-to-end query test."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from amarr.agents.executor import run_query
from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.ingestion import IngestionPipeline

class EndToEndQueryTests(unittest.TestCase):
    def test_sample_flow_returns_cited_answer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "kb.md").write_text("# KB\n\nReliable local systems use explicit routing, deterministic fallback, cited evidence, and verification.", encoding="utf-8")
            config = AppConfig.defaults()
            config.storage_dir = str(root / "state")
            config.vector_dir = str(root / "state" / "vector")
            registry = ModelRegistry.from_config(config, mock=True)
            IngestionPipeline(config, registry).ingest(docs)
            state = run_query("What design principles does this knowledge base recommend for building reliable local AI systems?", config, registry)
            self.assertIsNotNone(state.answer)
            self.assertTrue(state.answer.citations)
            self.assertEqual(state.answer.selected_route, "reasoning_large")

if __name__ == "__main__":
    unittest.main()

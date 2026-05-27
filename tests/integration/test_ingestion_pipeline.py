"""Ingestion pipeline integration test."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.ingestion import IngestionPipeline
from amarr.rag.retrieval import RetrievalPipeline

class IngestionPipelineTests(unittest.TestCase):
    def test_ingest_then_retrieve(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "a.md").write_text("# A\n\nHybrid retrieval combines keyword and vector search for local evidence.", encoding="utf-8")
            config = AppConfig.defaults()
            config.storage_dir = str(root / "state")
            config.vector_dir = str(root / "state" / "vector")
            registry = ModelRegistry.from_config(config, mock=True)
            stats = IngestionPipeline(config, registry).ingest(docs)
            self.assertEqual(stats.documents, 1)
            evidence = RetrievalPipeline(config, registry).retrieve("keyword vector evidence")
            self.assertTrue(evidence)

if __name__ == "__main__":
    unittest.main()

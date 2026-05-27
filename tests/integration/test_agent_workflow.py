"""Agent workflow integration test."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from amarr.agents.executor import run_query
from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.ingestion import IngestionPipeline

class AgentWorkflowTests(unittest.TestCase):
    def test_workflow_records_agent_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "a.md").write_text("# A\n\nThe supervisor coordinates planner retrieval critic verifier and synthesis agents.", encoding="utf-8")
            config = AppConfig.defaults()
            config.storage_dir = str(root / "state")
            config.vector_dir = str(root / "state" / "vector")
            registry = ModelRegistry.from_config(config, mock=True)
            IngestionPipeline(config, registry).ingest(docs)
            state = run_query("Explain the agent workflow design principles", config, registry)
            senders = {message.sender for message in state.messages}
            self.assertIn("planner", senders)
            self.assertIn("verifier", senders)

if __name__ == "__main__":
    unittest.main()

"""Agent unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.agents.executor import run_query
from amarr.agents.graph import AgentGraph
from amarr.agents.planner import PlannerAgent
from amarr.agents.state import TaskState
from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.ingestion import IngestionPipeline


class AgentTests(unittest.TestCase):
    """Validate agent state transitions."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.docs = self.root / "docs"
        self.docs.mkdir()
        (self.docs / "notes.md").write_text(
            "# Notes\n\nLocal AI systems should use explicit routing, deterministic tests, citations, and verification.",
            encoding="utf-8",
        )
        self.config = AppConfig.defaults()
        self.config.storage_dir = str(self.root / "state")
        self.config.vector_dir = str(self.root / "state" / "vector")
        self.registry = ModelRegistry.from_config(self.config, mock=True)
        IngestionPipeline(self.config, self.registry).ingest(self.docs)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_planner_adds_plan_and_message(self) -> None:
        state = PlannerAgent().run(TaskState(query="plan local system"))
        self.assertTrue(state.plan)
        self.assertEqual(state.messages[-1].sender, "planner")

    def test_agent_graph_edges(self) -> None:
        graph = AgentGraph()
        self.assertIn(("verifier", "synthesizer"), graph.edges())
        self.assertIn("supervisor", graph.names())

    def test_supervisor_workflow_completes(self) -> None:
        state = run_query("What principles guide reliable local AI systems?", self.config, self.registry)
        self.assertIsNotNone(state.answer)
        self.assertGreater(state.answer.confidence, 0.0)
        self.assertGreaterEqual(len(state.messages), 6)
        self.assertTrue(state.evidence)


if __name__ == "__main__":
    unittest.main()

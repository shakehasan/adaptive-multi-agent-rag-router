"""Retrieval agent."""

from __future__ import annotations

from amarr.rag.retrieval import RetrievalPipeline

from .base import BaseAgent
from .state import TaskState


class RetrievalAgent(BaseAgent):
    """Gather evidence from local retrieval indexes."""

    def __init__(self, pipeline: RetrievalPipeline) -> None:
        super().__init__("retrieval")
        self.pipeline = pipeline

    def run(self, state: TaskState) -> TaskState:
        """Retrieve evidence and store it in task state."""
        state.evidence = self.pipeline.retrieve(state.query)
        state.add_message(self.name, "researcher", "evidence", f"retrieved {len(state.evidence)} chunks")
        return state

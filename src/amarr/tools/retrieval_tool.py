"""Tool wrapper for retrieval."""

from __future__ import annotations

from typing import Any

from amarr.rag.retrieval import RetrievalPipeline

from .base import BaseTool, ToolResult


class RetrievalTool(BaseTool):
    """Expose retrieval to agents."""

    name = "retrieval"

    def __init__(self, pipeline: RetrievalPipeline) -> None:
        self.pipeline = pipeline

    def run(self, **kwargs: Any) -> ToolResult:
        """Retrieve evidence for a query."""
        query = str(kwargs.get("query", ""))
        evidence = self.pipeline.retrieve(query)
        return ToolResult(True, f"retrieved {len(evidence)} chunks", {"evidence": evidence})

"""Rule-based planning tool."""

from __future__ import annotations

from typing import Any

from .base import BaseTool, ToolResult


class PlannerTool(BaseTool):
    """Create a small task plan."""

    name = "planner"

    def run(self, **kwargs: Any) -> ToolResult:
        """Return a generic plan."""
        query = str(kwargs.get("query", ""))
        steps = ["route task", "retrieve evidence", "verify support", "synthesize answer"]
        if "code" in query.lower():
            steps.insert(2, "inspect code context")
        return ToolResult(True, "\n".join(steps), {"steps": steps})

"""Local safety and intent classifier."""

from __future__ import annotations

from typing import Any

from .base import BaseTool, ToolResult

BLOCKED_TERMS = {"credential", "secret", "token dump", "private key"}


class SafetyTool(BaseTool):
    """Classify whether a request is allowed for local demo execution."""

    name = "safety"

    def run(self, **kwargs: Any) -> ToolResult:
        """Return local safety classification."""
        query = str(kwargs.get("query", ""))
        lowered = query.lower()
        blocked = [term for term in BLOCKED_TERMS if term in lowered]
        if blocked:
            return ToolResult(False, "request rejected by local safety policy", {"blocked": blocked})
        intent = "coding" if "code" in lowered or "debug" in lowered else "research"
        return ToolResult(True, intent, {"intent": intent})

"""Safe local file reader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from amarr.core.errors import ToolError

from .base import BaseTool, ToolResult


class FileReaderTool(BaseTool):
    """Read files beneath an allowed root."""

    name = "file_reader"

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def run(self, **kwargs: Any) -> ToolResult:
        """Read a local text file."""
        requested = Path(str(kwargs.get("path", ""))).resolve()
        if not requested.is_relative_to(self.root):
            raise ToolError("file access outside allowed root")
        text = requested.read_text(encoding="utf-8")
        return ToolResult(True, text, {"path": str(requested), "chars": len(text)})

"""Local code inspection tool."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from .base import BaseTool, ToolResult


class CodeInspectorTool(BaseTool):
    """Inspect Python files without executing them."""

    name = "code_inspector"

    def run(self, **kwargs: Any) -> ToolResult:
        """Return simple structural metrics."""
        path = Path(str(kwargs.get("path", "")))
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        output = f"{len(classes)} classes, {len(functions)} functions"
        return ToolResult(True, output, {"classes": classes, "functions": functions})

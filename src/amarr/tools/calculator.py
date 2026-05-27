"""Safe arithmetic calculator tool."""

from __future__ import annotations

import ast
import operator
from typing import Any

from amarr.core.errors import ToolError

from .base import BaseTool, ToolResult

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


class CalculatorTool(BaseTool):
    """Evaluate simple arithmetic expressions."""

    name = "calculator"

    def run(self, **kwargs: Any) -> ToolResult:
        """Evaluate the expression argument."""
        expression = str(kwargs.get("expression", ""))
        value = _eval(ast.parse(expression, mode="eval").body)
        return ToolResult(True, str(value), {"value": value})


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return float(OPS[type(node.op)](_eval(node.left), _eval(node.right)))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return float(OPS[type(node.op)](_eval(node.operand)))
    raise ToolError("unsupported calculator expression")

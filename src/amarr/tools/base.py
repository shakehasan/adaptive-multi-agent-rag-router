"""Base local tool contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolResult:
    """Tool execution result."""

    ok: bool
    output: str
    data: dict[str, Any] = field(default_factory=dict)


class BaseTool(ABC):
    """Base class for local tools."""

    name: str

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        """Run the tool."""

"""Base agent contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .state import TaskState


class BaseAgent(ABC):
    """Base class for all local agents."""

    name: str

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.__class__.__name__.replace("Agent", "").lower()

    @abstractmethod
    def run(self, state: TaskState) -> TaskState:
        """Run the agent and return updated state."""

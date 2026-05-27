"""Shared task state for agent workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amarr.core.types import Evidence, WorkflowAnswer
from amarr.routing.decisions import RouteDecision

from .messages import AgentMessage


@dataclass(slots=True)
class TaskState:
    """Mutable state passed through an agent graph."""

    query: str
    route: RouteDecision | None = None
    plan: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    verification_notes: list[str] = field(default_factory=list)
    answer: WorkflowAnswer | None = None
    messages: list[AgentMessage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_message(self, sender: str, recipient: str, kind: str, content: str, **data: Any) -> AgentMessage:
        """Append a typed message to state."""
        message = AgentMessage(sender=sender, recipient=recipient, kind=kind, content=content, data=data)
        self.messages.append(message)
        return message

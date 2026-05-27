"""Typed model messages."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Message:
    """One message in a chat-style exchange."""

    role: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ChatPrompt:
    """A model prompt with optional system context."""

    messages: list[Message]
    temperature: float = 0.0
    max_tokens: int = 700

    @classmethod
    def from_user(cls, content: str, system: str = "") -> "ChatPrompt":
        """Create a prompt from user text and optional system guidance."""
        messages = []
        if system:
            messages.append(Message(role="system", content=system))
        messages.append(Message(role="user", content=content))
        return cls(messages=messages)

    def joined(self) -> str:
        """Return a deterministic plain text representation."""
        return "\n".join(f"{msg.role}: {msg.content}" for msg in self.messages)

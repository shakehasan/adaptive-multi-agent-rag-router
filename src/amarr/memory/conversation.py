"""Conversation memory helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from amarr.core.clocks import utc_ms

from .store import JsonMemoryStore


@dataclass(slots=True)
class ConversationTurn:
    """One conversation turn."""

    role: str
    content: str
    timestamp_ms: int = field(default_factory=utc_ms)


class ConversationMemory:
    """Persist conversation history locally."""

    def __init__(self, store: JsonMemoryStore) -> None:
        self.store = store

    def append(self, conversation_id: str, role: str, content: str) -> None:
        """Append a turn."""
        turns = self.store.get("conversation", conversation_id, []) or []
        turns.append(asdict(ConversationTurn(role, content)))
        self.store.put("conversation", conversation_id, turns)

    def load(self, conversation_id: str) -> list[ConversationTurn]:
        """Load turns."""
        return [ConversationTurn(**item) for item in self.store.get("conversation", conversation_id, []) or []]

    def recent_text(self, conversation_id: str, limit: int = 6) -> str:
        """Return recent history as text."""
        turns = self.load(conversation_id)[-limit:]
        return "\n".join(f"{turn.role}: {turn.content}" for turn in turns)

"""Long-term local memory."""

from __future__ import annotations

from amarr.core.ids import stable_id

from .store import JsonMemoryStore


class LongTermMemory:
    """Store durable local facts and summaries."""

    def __init__(self, store: JsonMemoryStore) -> None:
        self.store = store

    def remember(self, text: str, *, tags: list[str] | None = None) -> str:
        """Persist a memory and return its key."""
        key = stable_id("mem", text)
        self.store.put("long_term", key, {"text": text, "tags": tags or []})
        return key

    def search(self, term: str) -> list[dict[str, object]]:
        """Search memories by simple term containment."""
        results: list[dict[str, object]] = []
        for record in self.store.list_namespace("long_term"):
            text = str(record.value.get("text", ""))
            tags = [str(tag) for tag in record.value.get("tags", [])]
            if term.lower() in text.lower() or term.lower() in " ".join(tags).lower():
                results.append({"key": record.key, **record.value})
        return results

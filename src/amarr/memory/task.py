"""Short-term task memory."""

from __future__ import annotations

from .store import JsonMemoryStore


class TaskMemory:
    """Store task-local intermediate artifacts."""

    def __init__(self, store: JsonMemoryStore) -> None:
        self.store = store

    def save_plan(self, task_id: str, plan: list[str]) -> None:
        """Persist a task plan."""
        self.store.put("task", f"{task_id}:plan", {"steps": plan})

    def load_plan(self, task_id: str) -> list[str]:
        """Load a task plan."""
        data = self.store.get("task", f"{task_id}:plan", {}) or {}
        return list(data.get("steps", []))

    def save_note(self, task_id: str, key: str, value: str) -> None:
        """Persist a task note."""
        self.store.put("task", f"{task_id}:{key}", {"value": value})

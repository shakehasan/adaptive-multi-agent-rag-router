"""Memory pruning policies."""

from __future__ import annotations

from .store import JsonMemoryStore


def prune_namespace(store: JsonMemoryStore, namespace: str, *, keep_last: int) -> int:
    """Keep only the last N records in insertion order."""
    records = store.records.get(namespace, {})
    keys = list(records.keys())
    removed = 0
    for key in keys[:-keep_last]:
        records.pop(key, None)
        removed += 1
    store.put(namespace, "__prune_marker__", {"removed": removed})
    store.delete(namespace, "__prune_marker__")
    return removed

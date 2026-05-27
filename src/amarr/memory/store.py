"""Local JSON memory store."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from amarr.core.serialization import dump_json, load_json


@dataclass(slots=True)
class MemoryRecord:
    """One memory record."""

    key: str
    value: dict[str, Any]
    namespace: str = "default"


class JsonMemoryStore:
    """Small local key-value store backed by JSON."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.records: dict[str, dict[str, Any]] = load_json(path, {}) or {}

    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        """Write a record."""
        bucket = self.records.setdefault(namespace, {})
        bucket[key] = value
        dump_json(self.path, self.records)

    def get(self, namespace: str, key: str, default: Any | None = None) -> Any:
        """Read a record."""
        return self.records.get(namespace, {}).get(key, default)

    def list_namespace(self, namespace: str) -> list[MemoryRecord]:
        """List records in a namespace."""
        return [
            MemoryRecord(key=key, value=value, namespace=namespace)
            for key, value in self.records.get(namespace, {}).items()
        ]

    def delete(self, namespace: str, key: str) -> bool:
        """Delete a record if present."""
        bucket = self.records.get(namespace, {})
        existed = key in bucket
        bucket.pop(key, None)
        dump_json(self.path, self.records)
        return existed

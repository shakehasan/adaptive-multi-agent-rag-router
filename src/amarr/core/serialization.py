"""JSON serialization helpers for dataclasses and enums."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any


def to_plain(value: Any) -> Any:
    """Convert common Python objects into JSON-compatible data."""
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_plain(item) for item in value]
    return value


def dumps(value: Any, *, indent: int = 2) -> str:
    """Serialize a value as formatted JSON."""
    return json.dumps(to_plain(value), indent=indent, sort_keys=True)


def dump_json(path: Path, value: Any) -> None:
    """Write JSON to disk, creating the parent directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(value), encoding="utf-8")


def load_json(path: Path, default: Any | None = None) -> Any:
    """Load JSON from disk or return a default."""
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

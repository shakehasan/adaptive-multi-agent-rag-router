"""Structured local logging without external telemetry."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .clocks import utc_ms
from .serialization import dumps


class LocalJsonLogger:
    """Append-only JSON line logger."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, level: str, event: str, **data: Any) -> None:
        """Write one structured line."""
        payload = {"level": level, "event": event, "timestamp_ms": utc_ms(), **data}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(dumps(payload, indent=None) + "\n")

    def info(self, event: str, **data: Any) -> None:
        """Write an info event."""
        self.log("info", event, **data)

    def warning(self, event: str, **data: Any) -> None:
        """Write a warning event."""
        self.log("warning", event, **data)

    def error(self, event: str, **data: Any) -> None:
        """Write an error event."""
        self.log("error", event, **data)


def get_logger(storage_dir: Path, name: str = "amarr") -> LocalJsonLogger:
    """Return a logger under the local storage directory."""
    return LocalJsonLogger(storage_dir / "logs" / f"{name}.jsonl")

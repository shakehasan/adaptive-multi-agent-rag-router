"""Local trace storage."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from amarr.core.ids import time_ordered_id
from amarr.core.serialization import dump_json, load_json, to_plain

from .spans import Span


class TraceStore:
    """Write and read local trace files."""

    def __init__(self, trace_dir: Path) -> None:
        self.trace_dir = trace_dir
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.trace_id = time_ordered_id("trace")
        self.spans: list[Span] = []

    @contextmanager
    def span(self, name: str, kind: str, detail: str = "") -> Iterator[Span]:
        """Context manager for a trace span."""
        span = Span(name=name, kind=kind, detail=detail)
        self.spans.append(span)
        try:
            yield span
        finally:
            span.finish()

    def write(self) -> Path:
        """Persist the current trace."""
        path = self.trace_dir / f"{self.trace_id}.json"
        dump_json(path, {"trace_id": self.trace_id, "spans": [to_plain(span) for span in self.spans]})
        return path

    def list_traces(self) -> list[Path]:
        """List trace files."""
        return sorted(self.trace_dir.glob("trace_*.json"))

    def latest(self) -> dict[str, object] | None:
        """Return latest trace data."""
        traces = self.list_traces()
        if not traces:
            return None
        return load_json(traces[-1], {})

    def read(self, trace_id: str) -> dict[str, object] | None:
        """Read one trace by id."""
        path = self.trace_dir / f"{trace_id}.json"
        return load_json(path, None)

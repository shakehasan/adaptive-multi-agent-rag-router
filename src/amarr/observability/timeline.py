"""Timeline export helpers."""

from __future__ import annotations

from .spans import Span


def spans_to_timeline(spans: list[Span]) -> list[dict[str, object]]:
    """Convert spans to timeline rows."""
    return [
        {
            "name": span.name,
            "kind": span.kind,
            "duration_ms": span.duration_ms,
            "detail": span.detail,
            "data": span.data,
        }
        for span in spans
    ]

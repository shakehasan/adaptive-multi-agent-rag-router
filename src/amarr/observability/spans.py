"""Trace span value objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amarr.core.clocks import utc_ms
from amarr.core.ids import new_id


@dataclass(slots=True)
class Span:
    """One trace span."""

    name: str
    kind: str
    start_ms: int = field(default_factory=utc_ms)
    end_ms: int | None = None
    span_id: str = field(default_factory=lambda: new_id("span"))
    parent_id: str | None = None
    detail: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def finish(self) -> "Span":
        """Mark the span finished."""
        self.end_ms = utc_ms()
        return self

    @property
    def duration_ms(self) -> int:
        """Return span duration."""
        end = self.end_ms or utc_ms()
        return max(0, end - self.start_ms)

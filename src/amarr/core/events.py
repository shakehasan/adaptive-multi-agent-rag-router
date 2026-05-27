"""Typed local event system used by agents, routing, and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .clocks import utc_ms
from .ids import new_id


@dataclass(slots=True)
class Event:
    """A structured local event."""

    kind: str
    name: str
    detail: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: new_id("evt"))
    timestamp_ms: int = field(default_factory=utc_ms)


EventHandler = Callable[[Event], None]


class EventBus:
    """In-process event bus that keeps a local history."""

    def __init__(self) -> None:
        self._handlers: list[EventHandler] = []
        self.history: list[Event] = []

    def subscribe(self, handler: EventHandler) -> None:
        """Register a handler for future events."""
        self._handlers.append(handler)

    def publish(self, event: Event) -> Event:
        """Record and dispatch an event."""
        self.history.append(event)
        for handler in list(self._handlers):
            handler(event)
        return event

    def emit(self, kind: str, name: str, detail: str = "", **data: Any) -> Event:
        """Create and publish an event."""
        return self.publish(Event(kind=kind, name=name, detail=detail, data=data))

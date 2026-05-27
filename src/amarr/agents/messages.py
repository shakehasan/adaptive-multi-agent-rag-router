"""Typed messages exchanged by agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amarr.core.clocks import utc_ms
from amarr.core.ids import new_id


@dataclass(slots=True)
class AgentMessage:
    """Agent-to-agent message."""

    sender: str
    recipient: str
    kind: str
    content: str
    data: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: new_id("msg"))
    timestamp_ms: int = field(default_factory=utc_ms)

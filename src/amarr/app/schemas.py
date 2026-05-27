"""API schema helpers using dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class QueryRequest:
    """Local API query request."""

    query: str
    mock: bool = True
    conversation_id: str = "default"


@dataclass(slots=True)
class IngestRequest:
    """Local API ingest request."""

    path: str


@dataclass(slots=True)
class ApiResponse:
    """Generic API response."""

    ok: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str = ""

"""Shared typed value objects used across the project."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

MODEL_ALIASES: tuple[str, ...] = (
    "reasoning_large",
    "coding_large",
    "fast_small",
    "retrieval_embedder",
    "rerank_local",
)


class TaskKind(str, Enum):
    """Supported high-level task classes."""

    CLASSIFICATION = "classification"
    ROUTING = "routing"
    PLANNING = "planning"
    RETRIEVAL = "retrieval"
    RESEARCH = "research"
    CODING = "coding"
    CRITIQUE = "critique"
    VERIFICATION = "verification"
    SYNTHESIS = "synthesis"
    EVALUATION = "evaluation"
    UNKNOWN = "unknown"


class Capability(str, Enum):
    """Model capability labels understood by the router."""

    CLASSIFICATION = "classification"
    ROUTING = "routing"
    SUMMARIZATION = "summarization"
    PLANNING = "planning"
    SYNTHESIS = "synthesis"
    VERIFICATION = "verification"
    CODE = "code"
    DEBUGGING = "debugging"
    ARCHITECTURE = "architecture"
    EMBEDDING = "embedding"
    RERANKING = "reranking"


@dataclass(slots=True)
class Evidence:
    """A retrieved text span with score and source metadata."""

    chunk_id: str
    source_id: str
    text: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def preview(self, limit: int = 220) -> str:
        """Return a compact display string."""
        text = " ".join(self.text.split())
        return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


@dataclass(slots=True)
class Citation:
    """A source citation included in an answer."""

    source_id: str
    chunk_id: str
    score: float
    preview: str


@dataclass(slots=True)
class WorkflowAnswer:
    """Final user-facing answer with audit metadata."""

    final_answer: str
    citations: list[Citation]
    confidence: float
    selected_route: str
    active_agents: list[str]
    verification_notes: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QueryEnvelope:
    """Incoming query payload used by CLI and API."""

    query: str
    conversation_id: str = "default"
    mock: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HealthStatus:
    """Health result for a local component."""

    name: str
    ok: bool
    detail: str = ""
    latency_ms: float = 0.0


@dataclass(slots=True)
class EvaluationSummary:
    """Aggregate result produced by evaluation runners."""

    name: str
    metrics: dict[str, float]
    passed: bool
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TimedResult:
    """Generic container for values measured with duration."""

    value: Any
    elapsed_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)

"""Replay adapter for deterministic evaluation fixtures."""

from __future__ import annotations

from pathlib import Path

from amarr.core.serialization import load_json
from amarr.core.types import HealthStatus

from .base import ModelRequest, ModelResponse
from .streaming import chunk_text


class ReplayChatAdapter:
    """Return recorded responses keyed by normalized prompt text."""

    def __init__(self, alias: str, fixture_path: Path) -> None:
        self.alias = alias
        self.fixture_path = fixture_path
        self.fixtures: dict[str, str] = load_json(fixture_path, {}) or {}

    def health(self) -> HealthStatus:
        """Return health based on fixture availability."""
        return HealthStatus(self.alias, self.fixture_path.exists(), str(self.fixture_path))

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Return a replayed response or a deterministic miss message."""
        key = " ".join(request.prompt.joined().lower().split())
        text = self.fixtures.get(key, "Replay miss: no fixture was recorded for this prompt.")
        return ModelResponse(text=text, alias=self.alias, metadata={"replay_key": key})

    def stream(self, request: ModelRequest):
        """Yield replayed chunks."""
        yield from chunk_text(self.complete(request).text)

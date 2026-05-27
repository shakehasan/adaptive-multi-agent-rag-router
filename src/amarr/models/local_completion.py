"""Generic local completion endpoint adapter."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

from amarr.core.clocks import Stopwatch
from amarr.core.errors import ModelError
from amarr.core.types import HealthStatus

from .base import ModelRequest, ModelResponse
from .streaming import chunk_text


class GenericLocalCompletionAdapter:
    """Adapter for simple local completion endpoints."""

    def __init__(self, alias: str, endpoint: str, *, enabled: bool = False) -> None:
        self.alias = alias
        self.endpoint = endpoint.rstrip("/")
        self.enabled = enabled

    def _validate(self) -> None:
        parsed = urllib.parse.urlparse(self.endpoint)
        if not self.enabled:
            raise ModelError("local network mode is disabled")
        if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ModelError("completion endpoint must be local")

    def health(self) -> HealthStatus:
        """Return configuration health."""
        try:
            self._validate()
        except ModelError as exc:
            return HealthStatus(self.alias, False, str(exc))
        return HealthStatus(self.alias, True, "configured")

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Send a prompt to a local completion endpoint."""
        self._validate()
        watch = Stopwatch.start()
        payload = json.dumps({"prompt": request.prompt.joined()}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.endpoint}/complete",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=request.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
        return ModelResponse(text=str(data.get("text", "")), alias=self.alias, latency_ms=watch.elapsed_ms())

    def stream(self, request: ModelRequest):
        """Yield chunks from the completion output."""
        yield from chunk_text(self.complete(request).text)

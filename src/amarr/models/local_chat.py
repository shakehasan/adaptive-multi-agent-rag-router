"""Generic local chat endpoint adapter."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

from amarr.core.clocks import Stopwatch
from amarr.core.errors import ModelError
from amarr.core.types import HealthStatus

from .base import ModelRequest, ModelResponse
from .streaming import chunk_text


def _is_local_url(endpoint: str) -> bool:
    parsed = urllib.parse.urlparse(endpoint)
    return parsed.hostname in {"localhost", "127.0.0.1", "::1"}


class GenericLocalChatAdapter:
    """Adapter for simple local HTTP chat endpoints."""

    def __init__(self, alias: str, endpoint: str, *, enabled: bool = False) -> None:
        self.alias = alias
        self.endpoint = endpoint.rstrip("/")
        self.enabled = enabled

    def health(self) -> HealthStatus:
        """Return adapter health without contacting non-local endpoints."""
        if not self.enabled:
            return HealthStatus(name=self.alias, ok=False, detail="network disabled")
        if not _is_local_url(self.endpoint):
            return HealthStatus(name=self.alias, ok=False, detail="endpoint is not local")
        try:
            with urllib.request.urlopen(f"{self.endpoint}/health", timeout=2) as response:
                return HealthStatus(name=self.alias, ok=response.status < 500, detail=str(response.status))
        except Exception as exc:
            return HealthStatus(name=self.alias, ok=False, detail=str(exc))

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Send a request to a local chat endpoint."""
        if not self.enabled:
            raise ModelError("local network mode is disabled")
        if not _is_local_url(self.endpoint):
            raise ModelError("endpoint must be local")
        watch = Stopwatch.start()
        payload = json.dumps({
                "messages": [
                    {"role": msg.role, "content": msg.content, "metadata": msg.metadata}
                    for msg in request.prompt.messages
                ],
            "temperature": request.prompt.temperature,
            "max_tokens": request.prompt.max_tokens,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.endpoint}/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=request.timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise ModelError(f"local chat endpoint failed: {exc}") from exc
        text = str(data.get("text", ""))
        return ModelResponse(text=text, alias=self.alias, latency_ms=watch.elapsed_ms())

    def stream(self, request: ModelRequest):
        """Stream chunks from a non-streaming response for portability."""
        yield from chunk_text(self.complete(request).text)

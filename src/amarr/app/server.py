"""Local HTTP API server and static demo host."""

from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from amarr.core.serialization import load_json

from .dependencies import AppContext, build_context


def run_server(host: str = "127.0.0.1", port: int = 8765, *, mock: bool = True) -> None:
    """Run the local API and demo server."""
    context = build_context(mock=mock)
    handler = make_handler(context)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"serving local demo at http://{host}:{port}")
    server.serve_forever()


def make_handler(context: AppContext):
    """Create a request handler bound to an application context."""

    class Handler(BaseHTTPRequestHandler):
        server_version = "amarr-local"

        def do_GET(self) -> None:
            """Handle GET requests."""
            path = urlparse(self.path).path
            if path == "/health":
                self._json({"ok": True, "status": "healthy"})
            elif path == "/config":
                self._json(context.config_view())
            elif path == "/traces":
                self._json({"traces": [item.name for item in context.trace_store.list_traces()]})
            elif path.startswith("/traces/"):
                trace_id = path.rsplit("/", 1)[-1].removesuffix(".json")
                self._json(context.trace_store.read(trace_id) or {})
            elif path == "/" or path.startswith("/static/"):
                self._static(path)
            else:
                self._json({"error": "not found"}, status=404)

        def do_POST(self) -> None:
            """Handle POST requests."""
            path = urlparse(self.path).path
            try:
                payload = self._read_json()
                if path == "/ingest":
                    self._json(context.ingest(str(payload.get("path", "examples/documents"))))
                elif path == "/query":
                    self._json(context.query(str(payload.get("query", ""))))
                elif path == "/evaluate":
                    self._json(context.evaluate())
                else:
                    self._json({"error": "not found"}, status=404)
            except Exception as exc:
                self._json({"error": str(exc)}, status=500)

        def log_message(self, format: str, *args: Any) -> None:
            """Keep the demo quiet by default."""
            return None

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                return {}
            return json.loads(self.rfile.read(length).decode("utf-8"))

        def _json(self, payload: dict[str, Any], *, status: int = 200) -> None:
            body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _static(self, request_path: str) -> None:
            base = Path(__file__).resolve().parents[1] / "demo" / "static"
            target = base / "index.html" if request_path == "/" else base / request_path.removeprefix("/static/")
            if not target.exists() or not target.resolve().is_relative_to(base.resolve()):
                self._json({"error": "not found"}, status=404)
                return
            body = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler

"""Render local trace HTML."""

from __future__ import annotations

import html


def render_trace_html(trace: dict[str, object]) -> str:
    """Render a trace as standalone HTML."""
    spans = trace.get("spans", []) if isinstance(trace, dict) else []
    rows = []
    for span in spans:
        if isinstance(span, dict):
            rows.append(
                "<tr>"
                f"<td>{html.escape(str(span.get('name', '')))}</td>"
                f"<td>{html.escape(str(span.get('kind', '')))}</td>"
                f"<td>{html.escape(str(span.get('duration_ms', '')))}</td>"
                f"<td>{html.escape(str(span.get('detail', '')))}</td>"
                "</tr>"
            )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Trace</title>"
        "<style>body{font-family:sans-serif;margin:24px}td,th{border:1px solid #ccc;padding:6px}</style>"
        "</head><body><h1>Local Trace</h1><table><tr><th>Name</th><th>Kind</th><th>ms</th><th>Detail</th></tr>"
        + "".join(rows)
        + "</table></body></html>"
    )

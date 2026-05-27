"""Ingest bundled example documents."""
from __future__ import annotations
from amarr.app.dependencies import build_context
if __name__ == "__main__":
    print(build_context(mock=True).ingest("examples/documents"))

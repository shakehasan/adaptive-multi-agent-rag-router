"""CLI ingest command."""
from __future__ import annotations
from amarr.app.dependencies import build_context

def run(args) -> int:
    context = build_context(mock=args.mock)
    stats = context.ingest(args.path)
    print(f"ingested {stats['documents']} documents into {stats['chunks']} chunks")
    print(f"vector index: {stats['vector_path']}")
    return 0

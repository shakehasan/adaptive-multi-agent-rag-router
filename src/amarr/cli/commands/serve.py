"""CLI serve command."""
from __future__ import annotations
from amarr.app.server import run_server

def run(args) -> int:
    run_server(host=args.host, port=args.port, mock=args.mock)
    return 0

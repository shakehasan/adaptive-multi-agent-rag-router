"""Command line interface for the local multi-agent RAG router."""

from __future__ import annotations

import argparse

from .commands import ask, benchmark, evaluate, ingest, inspect, serve, trace


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(prog="amarr", description="Local-first multi-agent RAG router")
    parser.add_argument("--mock", action=argparse.BooleanOptionalAction, default=True, help="use deterministic mock adapters")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="ingest local documents")
    ingest_parser.add_argument("path")
    ingest_parser.set_defaults(func=ingest.run)

    ask_parser = sub.add_parser("ask", help="ask a question")
    ask_parser.add_argument("query")
    ask_parser.set_defaults(func=ask.run)

    evaluate_parser = sub.add_parser("evaluate", help="run local evaluations")
    evaluate_parser.set_defaults(func=evaluate.run)

    trace_parser = sub.add_parser("trace", help="inspect local traces")
    trace_parser.add_argument("which", default="latest", nargs="?")
    trace_parser.set_defaults(func=trace.run)

    benchmark_parser = sub.add_parser("benchmark-routing", help="benchmark route decisions")
    benchmark_parser.set_defaults(func=benchmark.run)

    serve_parser = sub.add_parser("serve", help="run local API and browser demo")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.set_defaults(func=serve.run)

    inspect_parser = sub.add_parser("inspect", help="inspect config or index state")
    inspect_parser.add_argument("target", choices=["config", "index"])
    inspect_parser.set_defaults(func=inspect.run)
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

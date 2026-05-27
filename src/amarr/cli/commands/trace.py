"""CLI trace command."""
from __future__ import annotations
from pathlib import Path
from amarr.core.config import load_config
from amarr.core.serialization import dumps, load_json

def run(args) -> int:
    config = load_config()
    trace_dir = Path(config.observability.trace_dir)
    traces = sorted(trace_dir.glob("trace_*.json"))
    if args.which == "latest":
        if not traces:
            print("no traces found")
            return 0
        print(dumps(load_json(traces[-1], {})))
        return 0
    target = trace_dir / f"{args.which}.json"
    print(dumps(load_json(target, {})))
    return 0

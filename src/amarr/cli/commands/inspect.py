"""CLI inspect command."""
from __future__ import annotations
from pathlib import Path
from amarr.core.config import load_config
from amarr.core.serialization import dumps, load_json

def run(args) -> int:
    config = load_config()
    if args.target == "config":
        print(dumps(config))
    elif args.target == "index":
        vector_path = Path(config.vector_dir) / "vectors.json"
        data = load_json(vector_path, []) or []
        print(dumps({"vector_records": len(data), "path": str(vector_path)}))
    else:
        print("unknown inspect target")
    return 0

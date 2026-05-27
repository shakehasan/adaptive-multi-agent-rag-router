"""Export a sample local demo payload for review."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amarr.app.dependencies import build_context


def main() -> int:
    """Run the sample flow and save its payload."""
    context = build_context(mock=True)
    if not (ROOT / ".amarr" / "vector" / "vectors.json").exists():
        context.ingest("examples/documents")
    result = context.query("What principles guide reliable local AI systems?")
    output = ROOT / ".amarr" / "demo_payload.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

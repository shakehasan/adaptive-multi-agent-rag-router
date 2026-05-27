"""Asset generation placeholder for local diagrams."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    """Verify that required SVG assets exist."""
    root = Path(__file__).resolve().parents[1]
    required = ["architecture.svg", "routing-flow.svg", "rag-flow.svg", "agent-graph.svg", "evaluation-dashboard.svg"]
    missing = [name for name in required if not (root / "assets" / name).exists()]
    if missing:
        print("missing assets: " + ", ".join(missing))
        return 1
    print("assets present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

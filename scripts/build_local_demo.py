"""Check local demo files."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    """Validate local demo static files."""
    root = Path(__file__).resolve().parents[1]
    static = root / "src" / "amarr" / "demo" / "static"
    for name in ["index.html", "styles.css", "app.js"]:
        path = static / name
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            print(f"missing demo file: {name}")
            return 1
    print("local demo files ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

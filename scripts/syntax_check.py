"""Parse Python files without writing bytecode caches."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ["src", "tests", "scripts", "examples"]


def main() -> int:
    """Parse all Python files."""
    failures: list[str] = []
    for folder in FOLDERS:
        for path in (ROOT / folder).rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if failures:
        print("\n".join(failures))
        return 1
    print("syntax check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

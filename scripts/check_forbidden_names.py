"""Scan the repository for disallowed literal names without storing them in clear text."""

from __future__ import annotations

import base64
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".amarr", "__pycache__", ".venv", "venv", "build", "dist"}
TEXT_EXTENSIONS = {".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".html", ".css", ".js", ".svg", ".example", ""}
ENCODED_DEFAULTS = [
    "T3BlbkFJ", "QW50aHJvcGlj", "R29vZ2xl", "TWljcm9zb2Z0", "QW1hem9u",
    "QXp1cmU=", "Q29oZXJl", "TWlzdHJhbA==", "Q2xhdWRl", "R1BU", "Q2hhdEdQVA==",
        "QkVSTFJPQ0s=", "VmVydGV4", "TGFtYQ==", "RmFjZWJvb2s=",
]


def default_terms() -> list[str]:
    """Decode built-in terms at runtime so literals stay out of the tree."""
    return [base64.b64decode(item).decode("utf-8") for item in ENCODED_DEFAULTS]


def configured_terms() -> list[str]:
    """Load optional configured terms."""
    terms = default_terms()
    env_terms = os.getenv("AMARR_FORBIDDEN_TERMS", "")
    terms.extend(term.strip() for term in env_terms.split(",") if term.strip())
    term_file = ROOT / "forbidden_terms.txt"
    if term_file.exists():
        terms.extend(line.strip() for line in term_file.read_text(encoding="utf-8").splitlines() if line.strip())
    return sorted(set(terms), key=str.lower)


def iter_text_files() -> list[Path]:
    """Return text files to scan."""
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in TEXT_EXTENSIONS or path.name in {"Makefile", ".env.example", ".gitignore"}:
            files.append(path)
    return files


def main() -> int:
    """Run the scan."""
    terms = configured_terms()
    pattern = re.compile(r"\b(?:" + "|".join(re.escape(term) for term in terms) + r")\b", re.IGNORECASE)
    hits: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            hits.append(f"{path.relative_to(ROOT)}: {match.group(0)}")
    if hits:
        print("forbidden names detected")
        for hit in hits:
            print(hit)
        return 1
    print("forbidden name scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

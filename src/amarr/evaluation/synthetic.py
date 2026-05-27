"""Synthetic local dataset generation."""

from __future__ import annotations

from pathlib import Path

from .datasets import EvalItem


def generate_from_documents(path: str | Path) -> list[EvalItem]:
    """Create simple eval items from local document filenames."""
    root = Path(path)
    items: list[EvalItem] = []
    for file_path in sorted(root.glob("*.md")):
        text = file_path.read_text(encoding="utf-8").lower()
        terms = [term for term in ["local", "routing", "evidence", "verification", "fallback"] if term in text]
        if terms:
            items.append(EvalItem(f"What does {file_path.stem} say about local system design?", terms, "reasoning_large"))
    return items

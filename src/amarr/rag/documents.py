"""Document and chunk models."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def checksum(text: str) -> str:
    """Return a stable checksum for text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class Document:
    """Loaded local document."""

    source_id: str
    path: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_path(cls, path: Path, root: Path | None = None) -> "Document":
        """Load a document from disk."""
        base = root or path.parent
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(base)) if path.is_relative_to(base) else path.name
        return cls(
            source_id=relative.replace("\\", "/"),
            path=str(path),
            text=text,
            metadata={"extension": path.suffix.lower(), "checksum": checksum(text), "title": infer_title(text, path)},
        )


@dataclass(slots=True)
class Chunk:
    """A chunk of a local document."""

    chunk_id: str
    source_id: str
    text: str
    start_char: int
    end_char: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        """Return a JSON-compatible record."""
        return {
            "chunk_id": self.chunk_id,
            "source_id": self.source_id,
            "text": self.text,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "metadata": self.metadata,
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "Chunk":
        """Build a chunk from a stored record."""
        return cls(
            chunk_id=str(record["chunk_id"]),
            source_id=str(record["source_id"]),
            text=str(record["text"]),
            start_char=int(record["start_char"]),
            end_char=int(record["end_char"]),
            metadata=dict(record.get("metadata", {})),
        )


def infer_title(text: str, path: Path) -> str:
    """Infer a title from Markdown heading or filename."""
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("# "):
            return cleaned[2:].strip()
    return path.stem.replace("_", " ").title()


def make_chunk_id(source_id: str, index: int) -> str:
    """Return a stable chunk id."""
    return f"{source_id}#chunk-{index}"

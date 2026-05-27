"""Metadata extraction for local documents."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .documents import checksum, infer_title
from .normalization import tokenize


@dataclass(slots=True)
class DocumentMetadata:
    """Rich metadata about a local document."""

    source_id: str
    title: str
    extension: str
    checksum: str
    headings: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    word_count: int = 0

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible metadata."""
        return {
            "source_id": self.source_id,
            "title": self.title,
            "extension": self.extension,
            "checksum": self.checksum,
            "headings": self.headings,
            "tags": self.tags,
            "word_count": self.word_count,
        }


def extract_headings(text: str) -> list[str]:
    """Extract Markdown headings."""
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
    return headings


def infer_tags(text: str) -> list[str]:
    """Infer domain tags from local document content."""
    terms = set(tokenize(text))
    rules = {
        "routing": {"routing", "route", "alias", "policy"},
        "retrieval": {"retrieval", "evidence", "chunk", "citation"},
        "agents": {"agent", "supervisor", "planner", "verifier"},
        "evaluation": {"evaluation", "metric", "recall", "precision"},
        "privacy": {"local", "trace", "redaction", "storage"},
        "recovery": {"fallback", "retry", "failure", "circuit"},
    }
    tags = [tag for tag, needles in rules.items() if terms & needles]
    return sorted(tags)


def metadata_for_file(path: Path, root: Path | None = None) -> DocumentMetadata:
    """Extract metadata for a file."""
    text = path.read_text(encoding="utf-8")
    source_id = str(path.relative_to(root)) if root and path.is_relative_to(root) else path.name
    return DocumentMetadata(
        source_id=source_id.replace("\\", "/"),
        title=infer_title(text, path),
        extension=path.suffix.lower(),
        checksum=checksum(text),
        headings=extract_headings(text),
        tags=infer_tags(text),
        word_count=len(tokenize(text)),
    )


def extract_front_matter(text: str) -> dict[str, str]:
    """Extract a tiny key/value front matter block if present."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    result: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result

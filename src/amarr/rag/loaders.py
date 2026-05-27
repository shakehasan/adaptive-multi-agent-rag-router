"""Local document loaders."""

from __future__ import annotations

from pathlib import Path

from amarr.core.errors import RetrievalError

from .documents import Document

SUPPORTED_EXTENSIONS = {".md", ".txt"}


def iter_document_paths(path: Path) -> list[Path]:
    """Return supported file paths from a file or directory."""
    if not path.exists():
        raise RetrievalError(f"path does not exist: {path}")
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_EXTENSIONS else []
    return sorted(
        item for item in path.rglob("*") if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def load_documents(path: str | Path) -> list[Document]:
    """Load supported local documents."""
    root = Path(path).resolve()
    documents: list[Document] = []
    for file_path in iter_document_paths(root):
        documents.append(Document.from_path(file_path.resolve(), root if root.is_dir() else root.parent))
    return documents

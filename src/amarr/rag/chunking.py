"""Chunk documents with character-size windows and overlap."""

from __future__ import annotations

from dataclasses import dataclass

from .documents import Chunk, Document, make_chunk_id
from .normalization import normalize_text


@dataclass(slots=True)
class Chunker:
    """Create overlapping chunks with stable ids."""

    chunk_size: int = 800
    overlap: int = 120

    def split(self, document: Document) -> list[Chunk]:
        """Split one document into chunks."""
        text = normalize_text(document.text)
        if not text:
            return []
        chunks: list[Chunk] = []
        index = 0
        start = 0
        while start < len(text):
            end = min(len(text), start + self.chunk_size)
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                if boundary > start + int(self.chunk_size * 0.6):
                    end = boundary
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    Chunk(
                        chunk_id=make_chunk_id(document.source_id, index + 1),
                        source_id=document.source_id,
                        text=chunk_text,
                        start_char=start,
                        end_char=end,
                        metadata={**document.metadata, "chunk_index": index + 1},
                    )
                )
                index += 1
            if end >= len(text):
                break
            start = max(0, end - self.overlap)
        return chunks

    def split_many(self, documents: list[Document]) -> list[Chunk]:
        """Split many documents."""
        chunks: list[Chunk] = []
        for document in documents:
            chunks.extend(self.split(document))
        return chunks

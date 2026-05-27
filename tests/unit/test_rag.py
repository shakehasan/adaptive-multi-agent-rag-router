"""RAG unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.chunking import Chunker
from amarr.rag.citations import citations_from_evidence
from amarr.rag.documents import Document
from amarr.rag.embeddings import DeterministicEmbedder, cosine_similarity
from amarr.rag.grounding import grounding_score
from amarr.rag.ingestion import IngestionPipeline
from amarr.rag.keyword_index import KeywordIndex
from amarr.rag.retrieval import RetrievalPipeline
from amarr.rag.vector_store import VectorStore


class RagTests(unittest.TestCase):
    """Validate ingestion, search, citation, and grounding."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text(
            "# Guide\n\nLocal systems should use deterministic fallback, explicit routing, evidence citations, and trace inspection.",
            encoding="utf-8",
        )
        self.docs = docs
        self.config = AppConfig.defaults()
        self.config.storage_dir = str(self.root / "state")
        self.config.vector_dir = str(self.root / "state" / "vector")
        self.registry = ModelRegistry.from_config(self.config, mock=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_chunker_creates_overlap_chunks(self) -> None:
        doc = Document("x.md", "x.md", "alpha beta gamma delta epsilon zeta")
        chunks = Chunker(chunk_size=14, overlap=4).split(doc)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].source_id, "x.md")

    def test_embeddings_are_stable(self) -> None:
        embedder = DeterministicEmbedder(dimensions=12)
        a = embedder.embed("local routing")
        b = embedder.embed("local routing")
        self.assertEqual(a, b)
        self.assertAlmostEqual(cosine_similarity(a, b), 1.0)

    def test_keyword_index_retrieves_exact_terms(self) -> None:
        doc = Document("guide.md", "guide.md", "local routing evidence")
        chunk = Chunker().split(doc)[0]
        index = KeywordIndex()
        index.add(chunk)
        hits = index.search("routing")
        self.assertEqual(hits[0][0].chunk_id, chunk.chunk_id)

    def test_vector_store_searches(self) -> None:
        doc = Document("guide.md", "guide.md", "local routing evidence")
        chunk = Chunker().split(doc)[0]
        embedder = DeterministicEmbedder()
        store = VectorStore()
        store.add(chunk, embedder.embed(chunk.text))
        hits = store.search(embedder.embed("local routing"))
        self.assertEqual(hits[0][0].source_id, "guide.md")

    def test_ingestion_and_retrieval_pipeline(self) -> None:
        stats = IngestionPipeline(self.config, self.registry).ingest(self.docs)
        self.assertEqual(stats.documents, 1)
        pipeline = RetrievalPipeline(self.config, self.registry)
        evidence = pipeline.retrieve("What does it say about deterministic routing?")
        self.assertTrue(evidence)
        self.assertIn("routing", evidence[0].text.lower())

    def test_citations_and_grounding(self) -> None:
        IngestionPipeline(self.config, self.registry).ingest(self.docs)
        evidence = RetrievalPipeline(self.config, self.registry).retrieve("local evidence")
        citations = citations_from_evidence(evidence)
        self.assertTrue(citations)
        result = grounding_score("Local systems use evidence citations.", evidence)
        self.assertGreater(result.score, 0.0)


if __name__ == "__main__":
    unittest.main()

# RAG

The retrieval system is designed for deterministic local execution. It supports document loading, normalization, chunking, metadata extraction, deterministic embeddings, keyword indexing, vector search, rank fusion, local reranking, citations, and grounding.

![RAG](../assets/rag-flow.svg)

## Ingestion

Markdown and plain text files are loaded from local directories. Metadata includes path, title, extension, checksum, and chunk identifiers. Text is normalized before chunking so indexing is reproducible.

## Hybrid Ranking

Keyword search captures exact terms. Vector search captures semantic proximity through a deterministic hashing embedder. Reciprocal rank fusion combines both lists, then reranking orders the best evidence.

## Citations

Every retrieved chunk keeps a stable citation id based on source path and chunk number. The synthesizer includes citations and the verifier checks whether answer claims have enough evidence coverage.

## Grounding

Grounding is intentionally conservative. The checker measures claim overlap with evidence, citation coverage, and unsupported phrases. The result becomes part of the confidence score.

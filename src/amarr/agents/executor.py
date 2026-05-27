"""End-to-end query workflow executor."""

from __future__ import annotations

from pathlib import Path

from amarr.core.config import AppConfig
from amarr.models.registry import ModelRegistry
from amarr.rag.ingestion import IngestionPipeline
from amarr.rag.retrieval import RetrievalPipeline
from amarr.routing.router import Router

from .retriever import RetrievalAgent
from .state import TaskState
from .supervisor import SupervisorAgent


def ensure_default_ingestion(config: AppConfig, registry: ModelRegistry, docs_path: str | Path = "examples/documents") -> None:
    """Ingest example documents when no local index exists."""
    pipeline = RetrievalPipeline(config, registry)
    if not pipeline.ready() and Path(docs_path).exists():
        IngestionPipeline(config, registry).ingest(docs_path)


def run_query(query: str, config: AppConfig, registry: ModelRegistry) -> TaskState:
    """Run the full local agent workflow."""
    ensure_default_ingestion(config, registry)
    retrieval = RetrievalPipeline(config, registry)
    router = Router(config, registry)
    supervisor = SupervisorAgent(router, RetrievalAgent(retrieval))
    return supervisor.run(TaskState(query=query))

"""Application dependency construction."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from amarr.agents.executor import run_query
from amarr.core.config import AppConfig, load_config
from amarr.core.serialization import to_plain
from amarr.evaluation.agent_eval import evaluate_agent_workflow
from amarr.evaluation.datasets import default_dataset
from amarr.evaluation.rag_eval import evaluate_retrieval
from amarr.evaluation.reports import write_reports
from amarr.evaluation.route_eval import evaluate_routes
from amarr.models.registry import ModelRegistry
from amarr.observability.traces import TraceStore
from amarr.rag.context_builder import evidence_table
from amarr.rag.ingestion import IngestionPipeline
from amarr.rag.retrieval import RetrievalPipeline
from amarr.routing.router import Router


class AppContext:
    """Shared local application context."""

    def __init__(self, config: AppConfig | None = None, *, mock: bool = True) -> None:
        self.config = config or load_config()
        self.registry = ModelRegistry.from_config(self.config, mock=mock)
        self.trace_store = TraceStore(Path(self.config.observability.trace_dir))

    def ingest(self, path: str) -> dict[str, Any]:
        """Run local ingestion."""
        with self.trace_store.span("ingest", "rag", path):
            stats = IngestionPipeline(self.config, self.registry).ingest(path)
        self.trace_store.write()
        return asdict(stats)

    def query(self, query: str) -> dict[str, Any]:
        """Run a complete query workflow."""
        with self.trace_store.span("query", "workflow", query):
            state = run_query(query, self.config, self.registry)
        trace_path = self.trace_store.write()
        answer = to_plain(state.answer) if state.answer else {}
        route = state.route.to_record() if state.route else {}
        return {
            "answer": answer,
            "route": route,
            "evidence": evidence_table(state.evidence),
            "trace_events": [to_plain(message) for message in state.messages],
            "trace_path": str(trace_path),
        }

    def evaluate(self) -> dict[str, Any]:
        """Run local evaluation."""
        dataset = default_dataset()
        retrieval = RetrievalPipeline(self.config, self.registry)
        if not retrieval.ready():
            self.ingest("examples/documents")
        router = Router(self.config, self.registry)
        summaries = [
            evaluate_retrieval(retrieval, dataset),
            evaluate_routes(router, dataset),
            evaluate_agent_workflow(self.config, self.registry, dataset),
        ]
        json_path, md_path = write_reports(summaries, Path(self.config.storage_dir) / "evals")
        return {"summaries": [to_plain(summary) for summary in summaries], "json": str(json_path), "markdown": str(md_path)}

    def config_view(self) -> dict[str, Any]:
        """Return a safe config view."""
        return {
            "environment": self.config.environment,
            "storage_dir": self.config.storage_dir,
            "vector_dir": self.config.vector_dir,
            "network_enabled": self.config.enable_network,
            "telemetry_enabled": self.config.enable_telemetry,
            "aliases": sorted(self.config.models),
        }


def build_context(*, mock: bool = True) -> AppContext:
    """Build default app context."""
    return AppContext(mock=mock)

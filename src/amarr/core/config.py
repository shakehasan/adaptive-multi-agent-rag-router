"""Configuration loading with environment overrides and simple YAML support."""

from __future__ import annotations

import os
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .errors import ConfigError
from .types import MODEL_ALIASES


def _parse_scalar(value: str) -> Any:
    value = os.path.expandvars(value.strip())
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "none"}:
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value.strip('"').strip("'")


def _prepared_lines(text: str) -> list[tuple[int, str]]:
    prepared: list[tuple[int, str]] = []
    for raw in textwrap.dedent(text).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        prepared.append((indent, raw.strip()))
    return prepared


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by local examples."""
    lines = _prepared_lines(text)

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return {}, index
        is_list = lines[index][0] == indent and lines[index][1].startswith("- ")
        if is_list:
            items: list[Any] = []
            while index < len(lines) and lines[index][0] == indent and lines[index][1].startswith("- "):
                items.append(_parse_scalar(lines[index][1][2:]))
                index += 1
            return items, index
        mapping: dict[str, Any] = {}
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ConfigError(f"unexpected indentation near: {content}")
            if ":" not in content:
                raise ConfigError(f"expected key/value near: {content}")
            key, raw_value = content.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            index += 1
            if raw_value:
                mapping[key] = _parse_scalar(raw_value)
                continue
            next_indent = lines[index][0] if index < len(lines) else indent + 2
            value, index = parse_block(index, next_indent)
            mapping[key] = value
        return mapping, index

    parsed, _ = parse_block(0, 0)
    return parsed if isinstance(parsed, dict) else {}


@dataclass(slots=True)
class ModelConfig:
    """Configuration for one neutral alias."""

    alias: str
    type: str = "mock"
    endpoint: str = ""
    capabilities: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RoutingConfig:
    """Router configuration values."""

    default_policy: str = "balanced"
    fallback_model: str = "fast_small"
    timeout_seconds: int = 30
    max_retries: int = 2


@dataclass(slots=True)
class RagConfig:
    """Retrieval configuration values."""

    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 8
    rerank_top_k: int = 5
    hybrid_alpha: float = 0.65


@dataclass(slots=True)
class ObservabilityConfig:
    """Trace configuration values."""

    trace_enabled: bool = True
    trace_dir: str = ".amarr/traces"
    redact_prompts: bool = False


@dataclass(slots=True)
class AppConfig:
    """Complete application configuration."""

    environment: str = "local"
    storage_dir: str = ".amarr"
    vector_dir: str = ".amarr/vector"
    enable_network: bool = False
    enable_telemetry: bool = False
    models: dict[str, ModelConfig] = field(default_factory=dict)
    routing: RoutingConfig = field(default_factory=RoutingConfig)
    rag: RagConfig = field(default_factory=RagConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)

    @classmethod
    def defaults(cls) -> "AppConfig":
        """Return a default local mock configuration."""
        models = {
            alias: ModelConfig(alias=alias, type="mock", endpoint="", capabilities=[])
            for alias in MODEL_ALIASES
        }
        models["reasoning_large"].capabilities = ["planning", "synthesis", "verification"]
        models["coding_large"].capabilities = ["code", "debugging", "architecture"]
        models["fast_small"].capabilities = ["classification", "routing", "summarization"]
        models["retrieval_embedder"].capabilities = ["embedding"]
        models["rerank_local"].capabilities = ["reranking"]
        return cls(models=models)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "AppConfig":
        """Build a config object from a parsed mapping."""
        config = cls.defaults()
        config.environment = str(data.get("environment", config.environment))
        privacy = data.get("privacy", {})
        if isinstance(privacy, dict):
            config.enable_telemetry = bool(privacy.get("telemetry", config.enable_telemetry))
            config.enable_network = bool(privacy.get("external_network", config.enable_network))
        model_data = data.get("models", {})
        if isinstance(model_data, dict):
            for alias, entry in model_data.items():
                if alias in MODEL_ALIASES and isinstance(entry, dict):
                    config.models[alias] = ModelConfig(
                        alias=alias,
                        type=str(entry.get("type", "mock")),
                        endpoint=str(entry.get("endpoint", "")),
                        capabilities=list(entry.get("capabilities", [])),
                    )
        routing = data.get("routing", {})
        if isinstance(routing, dict):
            config.routing = RoutingConfig(
                default_policy=str(routing.get("default_policy", config.routing.default_policy)),
                fallback_model=str(routing.get("fallback_model", config.routing.fallback_model)),
                timeout_seconds=int(routing.get("timeout_seconds", config.routing.timeout_seconds)),
                max_retries=int(routing.get("max_retries", config.routing.max_retries)),
            )
        rag = data.get("rag", {})
        if isinstance(rag, dict):
            config.rag = RagConfig(
                chunk_size=int(rag.get("chunk_size", config.rag.chunk_size)),
                chunk_overlap=int(rag.get("chunk_overlap", config.rag.chunk_overlap)),
                top_k=int(rag.get("top_k", config.rag.top_k)),
                rerank_top_k=int(rag.get("rerank_top_k", config.rag.rerank_top_k)),
                hybrid_alpha=float(rag.get("hybrid_alpha", config.rag.hybrid_alpha)),
            )
        obs = data.get("observability", {})
        if isinstance(obs, dict):
            config.observability = ObservabilityConfig(
                trace_enabled=bool(obs.get("trace_enabled", config.observability.trace_enabled)),
                trace_dir=str(obs.get("trace_dir", config.observability.trace_dir)),
                redact_prompts=bool(obs.get("redact_prompts", config.observability.redact_prompts)),
            )
        config.apply_environment()
        config.validate()
        return config

    def apply_environment(self) -> None:
        """Apply neutral environment variable overrides."""
        self.environment = os.getenv("AMARR_ENV", self.environment)
        self.storage_dir = os.getenv("AMARR_STORAGE_DIR", self.storage_dir)
        self.vector_dir = os.getenv("AMARR_VECTOR_DIR", self.vector_dir)
        self.observability.trace_dir = os.getenv("AMARR_TRACE_DIR", self.observability.trace_dir)
        self.enable_network = os.getenv("AMARR_ENABLE_NETWORK", str(self.enable_network)).lower() == "true"
        self.enable_telemetry = os.getenv("AMARR_ENABLE_TELEMETRY", str(self.enable_telemetry)).lower() == "true"
        endpoint_env = {
            "reasoning_large": "AMARR_MODEL_REASONING_LARGE_URL",
            "coding_large": "AMARR_MODEL_CODING_LARGE_URL",
            "fast_small": "AMARR_MODEL_FAST_SMALL_URL",
            "retrieval_embedder": "AMARR_MODEL_EMBEDDING_URL",
            "rerank_local": "AMARR_MODEL_RERANK_URL",
        }
        for alias, variable in endpoint_env.items():
            if variable in os.environ:
                self.models[alias].endpoint = os.environ[variable]

    def validate(self) -> None:
        """Validate core safety invariants."""
        if self.enable_telemetry:
            raise ConfigError("telemetry must remain disabled in this local project")
        if self.routing.fallback_model not in MODEL_ALIASES:
            raise ConfigError("fallback model must be a known alias")
        if self.rag.chunk_overlap >= self.rag.chunk_size:
            raise ConfigError("chunk overlap must be smaller than chunk size")


def load_config(path: str | Path | None = None) -> AppConfig:
    """Load configuration from a YAML example or defaults."""
    if path is None:
        config = AppConfig.defaults()
        config.apply_environment()
        config.validate()
        return config
    text = Path(path).read_text(encoding="utf-8")
    expanded = re.sub(r"\$\{([A-Z0-9_]+)\}", lambda m: os.getenv(m.group(1), ""), text)
    return AppConfig.from_mapping(parse_simple_yaml(expanded))

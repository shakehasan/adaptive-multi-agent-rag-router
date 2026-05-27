"""Custom error hierarchy for predictable local failures."""

from __future__ import annotations


class AmarrError(Exception):
    """Base exception for the project."""


class ConfigError(AmarrError):
    """Raised when configuration is invalid."""


class RoutingError(AmarrError):
    """Raised when routing cannot select a viable alias."""


class ModelError(AmarrError):
    """Raised when a local model adapter fails."""


class RetrievalError(AmarrError):
    """Raised when ingestion or retrieval cannot proceed."""


class AgentError(AmarrError):
    """Raised when an agent cannot complete its assigned task."""


class ToolError(AmarrError):
    """Raised when a local tool rejects a request."""


class ValidationError(AmarrError):
    """Raised when a structured payload fails validation."""

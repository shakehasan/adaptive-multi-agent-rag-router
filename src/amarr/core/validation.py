"""Small validation helpers for structured local inputs."""

from __future__ import annotations

from typing import Any

from .errors import ValidationError


def require_keys(data: dict[str, Any], keys: list[str], *, context: str) -> None:
    """Validate that a mapping contains required keys."""
    missing = [key for key in keys if key not in data]
    if missing:
        raise ValidationError(f"{context} missing keys: {', '.join(missing)}")


def require_non_empty(value: str, *, field: str) -> str:
    """Validate a non-empty string and return it."""
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(f"{field} must not be empty")
    return cleaned


def bounded_float(value: float, *, field: str, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Validate and clamp a score-like value."""
    if value != value:
        raise ValidationError(f"{field} must be a number")
    return max(minimum, min(maximum, value))


def validate_alias(alias: str, allowed: tuple[str, ...]) -> str:
    """Validate that a model alias is known."""
    if alias not in allowed:
        raise ValidationError(f"unknown model alias: {alias}")
    return alias

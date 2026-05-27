"""Structured output parsing and small schema validation."""

from __future__ import annotations

import json
from typing import Any

from amarr.core.errors import ValidationError


def parse_json_object(text: str) -> dict[str, Any]:
    """Parse the first JSON object found in text."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValidationError("no JSON object found")
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ValidationError(str(exc)) from exc
    if not isinstance(data, dict):
        raise ValidationError("structured output must be an object")
    return data


def validate_schema(data: dict[str, Any], schema: dict[str, type]) -> dict[str, Any]:
    """Validate required keys and Python value types."""
    for key, expected in schema.items():
        if key not in data:
            raise ValidationError(f"missing key: {key}")
        if not isinstance(data[key], expected):
            raise ValidationError(f"key {key} expected {expected.__name__}")
    return data


def coerce_string_list(data: Any) -> list[str]:
    """Coerce structured model output into a string list."""
    if isinstance(data, list):
        return [str(item) for item in data]
    if isinstance(data, str):
        return [line.strip("- ") for line in data.splitlines() if line.strip()]
    return [str(data)]

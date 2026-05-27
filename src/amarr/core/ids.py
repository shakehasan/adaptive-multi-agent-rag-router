"""Identifier helpers with stable prefixes."""

from __future__ import annotations

import hashlib
import time
import uuid


def new_id(prefix: str) -> str:
    """Return a short unique id with a readable prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def stable_id(prefix: str, value: str) -> str:
    """Return a deterministic id for stable local artifacts."""
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def time_ordered_id(prefix: str) -> str:
    """Return an id that sorts roughly by creation time."""
    stamp = int(time.time() * 1000)
    return f"{prefix}_{stamp}_{uuid.uuid4().hex[:8]}"

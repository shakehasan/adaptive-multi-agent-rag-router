"""Path and endpoint safety helpers."""

from __future__ import annotations

import os
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

from .errors import ValidationError


LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


@dataclass(slots=True)
class PathPolicy:
    """Policy for resolving local paths under a workspace root."""

    root: Path
    allow_missing: bool = False

    def resolve(self, value: str | Path) -> Path:
        """Resolve a path and enforce that it remains under root."""
        root = self.root.resolve()
        candidate = Path(os.path.expandvars(str(value))).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root):
            raise ValidationError(f"path escapes local root: {value}")
        if not self.allow_missing and not resolved.exists():
            raise ValidationError(f"path does not exist: {value}")
        return resolved

    def ensure_dir(self, value: str | Path) -> Path:
        """Resolve and create a directory beneath root."""
        old = self.allow_missing
        self.allow_missing = True
        try:
            resolved = self.resolve(value)
        finally:
            self.allow_missing = old
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved


def is_local_endpoint(endpoint: str) -> bool:
    """Return whether an endpoint URL points to a loopback host."""
    parsed = urllib.parse.urlparse(endpoint)
    return parsed.scheme in {"http", "https"} and parsed.hostname in LOCAL_HOSTS


def require_local_endpoint(endpoint: str) -> str:
    """Validate a local endpoint URL."""
    if not is_local_endpoint(endpoint):
        raise ValidationError("endpoint must use a local host")
    return endpoint.rstrip("/")


def workspace_relative(path: Path, root: Path) -> str:
    """Return a stable slash-separated relative path when possible."""
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        return path.name


def find_project_root(start: Path | None = None) -> Path:
    """Find a project root by looking for pyproject metadata."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists():
            return candidate
    return current

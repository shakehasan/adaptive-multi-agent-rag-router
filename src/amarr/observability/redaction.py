"""Local trace redaction helpers."""

from __future__ import annotations

import re


def redact_text(text: str, extra_terms: list[str] | None = None) -> str:
    """Redact common sensitive patterns from local traces."""
    redacted = re.sub(r"\b\d{12,}\b", "[redacted-number]", text)
    redacted = re.sub(r"[A-Za-z]:\\[^\s]+", "[redacted-path]", redacted)
    for term in extra_terms or []:
        if term:
            redacted = redacted.replace(term, "[redacted-term]")
    return redacted

"""Prompt and response audit helpers."""

from __future__ import annotations

from dataclasses import dataclass, field

from .redaction import redact_text


@dataclass(slots=True)
class AuditRecord:
    """One redacted audit record."""

    actor: str
    prompt: str
    response: str
    route_alias: str
    tags: list[str] = field(default_factory=list)

    def redacted(self, extra_terms: list[str] | None = None) -> "AuditRecord":
        """Return a redacted copy."""
        return AuditRecord(
            actor=self.actor,
            prompt=redact_text(self.prompt, extra_terms),
            response=redact_text(self.response, extra_terms),
            route_alias=self.route_alias,
            tags=list(self.tags),
        )

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible record."""
        return {
            "actor": self.actor,
            "prompt": self.prompt,
            "response": self.response,
            "route_alias": self.route_alias,
            "tags": self.tags,
        }


def summarize_audit(records: list[AuditRecord]) -> dict[str, object]:
    """Summarize audit records by route and actor."""
    by_route: dict[str, int] = {}
    by_actor: dict[str, int] = {}
    for record in records:
        by_route[record.route_alias] = by_route.get(record.route_alias, 0) + 1
        by_actor[record.actor] = by_actor.get(record.actor, 0) + 1
    return {"records": len(records), "by_route": by_route, "by_actor": by_actor}

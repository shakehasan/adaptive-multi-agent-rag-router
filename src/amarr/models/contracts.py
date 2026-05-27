"""Local endpoint contract helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class EndpointContract:
    """Describe a neutral local endpoint contract."""

    name: str
    request_shape: dict[str, str]
    response_shape: dict[str, str]
    streaming: bool = False
    notes: list[str] = field(default_factory=list)

    def validate_request(self, payload: dict[str, Any]) -> list[str]:
        """Return missing or mismatched request fields."""
        issues: list[str] = []
        for key, expected in self.request_shape.items():
            if key not in payload:
                issues.append(f"missing {key}")
                continue
            if expected == "list" and not isinstance(payload[key], list):
                issues.append(f"{key} must be a list")
            if expected == "string" and not isinstance(payload[key], str):
                issues.append(f"{key} must be a string")
        return issues

    def markdown(self) -> str:
        """Render the contract for documentation or inspection."""
        lines = [f"### {self.name}", "", "Request:"]
        lines.extend(f"- {key}: {value}" for key, value in self.request_shape.items())
        lines.append("")
        lines.append("Response:")
        lines.extend(f"- {key}: {value}" for key, value in self.response_shape.items())
        if self.notes:
            lines.append("")
            lines.extend(f"- {note}" for note in self.notes)
        return "\n".join(lines)


CHAT_CONTRACT = EndpointContract(
    name="local_chat",
    request_shape={"messages": "list", "temperature": "number", "max_tokens": "number"},
    response_shape={"text": "string"},
    streaming=True,
    notes=["Messages contain role, content, and optional metadata."],
)

COMPLETION_CONTRACT = EndpointContract(
    name="local_completion",
    request_shape={"prompt": "string"},
    response_shape={"text": "string"},
    streaming=True,
)

EMBEDDING_CONTRACT = EndpointContract(
    name="local_embedding",
    request_shape={"texts": "list"},
    response_shape={"vectors": "list"},
    streaming=False,
)


def all_contracts() -> list[EndpointContract]:
    """Return all neutral local endpoint contracts."""
    return [CHAT_CONTRACT, COMPLETION_CONTRACT, EMBEDDING_CONTRACT]

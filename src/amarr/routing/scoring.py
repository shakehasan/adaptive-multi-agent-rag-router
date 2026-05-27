"""Score model alias candidates."""

from __future__ import annotations

from amarr.core.types import Capability
from amarr.models.registry import ModelRegistry

from .decisions import RouteCandidate
from .rules import TaskProfile

CAPABILITY_MAP: dict[str, set[Capability]] = {
    "reasoning_large": {Capability.PLANNING, Capability.SYNTHESIS, Capability.VERIFICATION, Capability.SUMMARIZATION},
    "coding_large": {Capability.CODE, Capability.DEBUGGING, Capability.ARCHITECTURE, Capability.SUMMARIZATION},
    "fast_small": {Capability.CLASSIFICATION, Capability.ROUTING, Capability.SUMMARIZATION},
}

SPEED_MAP: dict[str, float] = {
    "fast_small": 0.95,
    "coding_large": 0.58,
    "reasoning_large": 0.45,
}


def score_candidates(profile: TaskProfile, registry: ModelRegistry) -> list[RouteCandidate]:
    """Score all registered chat aliases."""
    health = {status.name: status.ok for status in registry.health()}
    candidates: list[RouteCandidate] = []
    required = set(profile.required_capabilities)
    for alias in sorted(registry.chat_adapters):
        supported = CAPABILITY_MAP.get(alias, set())
        overlap = len(required & supported)
        capability = overlap / max(1, len(required))
        if profile.complexity > 0.65 and alias == "reasoning_large":
            capability += 0.2
        if profile.complexity < 0.35 and alias == "fast_small":
            capability += 0.1
        capability = min(1.0, capability)
        speed = SPEED_MAP.get(alias, 0.5)
        stability = 1.0 if health.get(alias, False) else 0.0
        total = capability * 0.58 + speed * 0.24 + stability * 0.18
        reasons = [f"capability={capability:.2f}", f"speed={speed:.2f}", f"stability={stability:.2f}"]
        candidates.append(RouteCandidate(alias, capability, speed, stability, total, reasons))
    candidates.sort(key=lambda item: item.total_score, reverse=True)
    return candidates

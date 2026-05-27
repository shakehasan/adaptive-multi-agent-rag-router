"""Workflow recovery planning."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RecoveryStep:
    """One recovery action."""

    action: str
    reason: str
    retryable: bool = True


@dataclass(slots=True)
class RecoveryPlan:
    """Recovery plan for a failed workflow."""

    steps: list[RecoveryStep] = field(default_factory=list)
    final_fallback: str = "fallback"

    def add(self, action: str, reason: str, retryable: bool = True) -> None:
        """Add a recovery step."""
        self.steps.append(RecoveryStep(action, reason, retryable))

    def retryable_steps(self) -> list[RecoveryStep]:
        """Return retryable steps."""
        return [step for step in self.steps if step.retryable]

    def markdown(self) -> str:
        """Render the plan for traces or reports."""
        lines = ["### Recovery Plan", ""]
        for index, step in enumerate(self.steps, start=1):
            lines.append(f"{index}. {step.action}: {step.reason} (retryable={step.retryable})")
        lines.append(f"Final fallback: {self.final_fallback}")
        return "\n".join(lines)


def plan_recovery(error_text: str) -> RecoveryPlan:
    """Create a recovery plan from an error string."""
    lowered = error_text.lower()
    plan = RecoveryPlan()
    if "index" in lowered or "ingest" in lowered:
        plan.add("rebuild local indexes", "retrieval state is missing or stale")
    if "route" in lowered or "alias" in lowered:
        plan.add("select fallback alias", "primary route is unavailable")
    if "timeout" in lowered:
        plan.add("retry with shorter context", "the operation exceeded its time budget")
    if not plan.steps:
        plan.add("return safe fallback answer", "failure did not match a specialized recovery path", False)
    return plan

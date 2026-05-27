"""Circuit breaker for local model aliases."""

from __future__ import annotations

from dataclasses import dataclass, field

from amarr.core.clocks import monotonic_ms


@dataclass(slots=True)
class CircuitState:
    """State for one circuit."""

    failures: int = 0
    opened_at_ms: float = 0.0
    state: str = "closed"


class CircuitBreaker:
    """Track repeated failures and recovery windows."""

    def __init__(self, failure_threshold: int = 3, recovery_seconds: float = 20.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_ms = recovery_seconds * 1000
        self.states: dict[str, CircuitState] = {}

    def state_for(self, alias: str) -> CircuitState:
        """Return state for an alias."""
        return self.states.setdefault(alias, CircuitState())

    def allow(self, alias: str) -> bool:
        """Return whether a request may use this alias."""
        state = self.state_for(alias)
        if state.state == "closed":
            return True
        elapsed = monotonic_ms() - state.opened_at_ms
        if elapsed >= self.recovery_ms:
            state.state = "half-open"
            return True
        return False

    def record_success(self, alias: str) -> None:
        """Close the circuit after success."""
        self.states[alias] = CircuitState()

    def record_failure(self, alias: str) -> None:
        """Increment failures and open when threshold is reached."""
        state = self.state_for(alias)
        state.failures += 1
        if state.failures >= self.failure_threshold:
            state.state = "open"
            state.opened_at_ms = monotonic_ms()

    def snapshot(self) -> dict[str, dict[str, float | int | str]]:
        """Return a JSON-compatible state snapshot."""
        return {
            alias: {"failures": state.failures, "opened_at_ms": state.opened_at_ms, "state": state.state}
            for alias, state in self.states.items()
        }

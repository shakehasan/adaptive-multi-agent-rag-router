"""Clock utilities centralized for tests and traces."""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator


def utc_ms() -> int:
    """Return current time in milliseconds since epoch."""
    return int(time.time() * 1000)


def monotonic_ms() -> float:
    """Return monotonic time in milliseconds."""
    return time.perf_counter() * 1000.0


@dataclass(slots=True)
class Stopwatch:
    """Small stopwatch for trace timings."""

    started_ms: float

    @classmethod
    def start(cls) -> "Stopwatch":
        """Create and start a stopwatch."""
        return cls(monotonic_ms())

    def elapsed_ms(self) -> float:
        """Return elapsed milliseconds."""
        return monotonic_ms() - self.started_ms


@contextmanager
def timed() -> Iterator[Stopwatch]:
    """Yield a stopwatch that continues to report elapsed time."""
    watch = Stopwatch.start()
    yield watch

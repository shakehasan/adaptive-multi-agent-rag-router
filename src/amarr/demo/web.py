"""Demo launcher."""

from __future__ import annotations

from amarr.app.server import run_server


def main() -> None:
    """Launch the local browser demo server."""
    run_server(mock=True)


if __name__ == "__main__":
    main()

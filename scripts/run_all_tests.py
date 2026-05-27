"""Run the standard library test suite."""

from __future__ import annotations

import sys
import os
import shutil
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))
TMP_ROOT = ROOT / ".amarr" / "test-tmp"
TMP_ROOT.mkdir(parents=True, exist_ok=True)
os.environ["TMP"] = str(TMP_ROOT)
os.environ["TEMP"] = str(TMP_ROOT)
os.environ["TMPDIR"] = str(TMP_ROOT)
tempfile.tempdir = str(TMP_ROOT)


class LocalTemporaryDirectory:
    """TemporaryDirectory replacement that uses normal workspace folders."""

    def __init__(self, *args, **kwargs) -> None:
        self.name = str(TMP_ROOT / f"tmp_{uuid.uuid4().hex}")
        Path(self.name).mkdir(parents=True, exist_ok=False)

    def __enter__(self) -> str:
        return self.name

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        shutil.rmtree(self.name, ignore_errors=True)


tempfile.TemporaryDirectory = LocalTemporaryDirectory


def main() -> int:
    """Discover and run tests."""
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    shutil.rmtree(TMP_ROOT, ignore_errors=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

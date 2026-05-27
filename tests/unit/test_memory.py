"""Memory unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.memory.conversation import ConversationMemory
from amarr.memory.long_term import LongTermMemory
from amarr.memory.pruning import prune_namespace
from amarr.memory.store import JsonMemoryStore
from amarr.memory.summarizer import summarize_texts
from amarr.memory.task import TaskMemory


class MemoryTests(unittest.TestCase):
    """Validate local memory persistence."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.store = JsonMemoryStore(Path(self.tmp.name) / "memory.json")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_conversation_memory_roundtrip(self) -> None:
        memory = ConversationMemory(self.store)
        memory.append("c1", "user", "hello")
        memory.append("c1", "assistant", "hi")
        self.assertEqual(len(memory.load("c1")), 2)
        self.assertIn("assistant", memory.recent_text("c1"))

    def test_task_memory_roundtrip(self) -> None:
        tasks = TaskMemory(self.store)
        tasks.save_plan("t1", ["a", "b"])
        self.assertEqual(tasks.load_plan("t1"), ["a", "b"])

    def test_long_term_search(self) -> None:
        memory = LongTermMemory(self.store)
        memory.remember("local routing evidence", tags=["routing"])
        results = memory.search("routing")
        self.assertEqual(len(results), 1)

    def test_summary_and_pruning(self) -> None:
        summary = summarize_texts(["Alpha is first. Beta is second.", "Alpha is first. Gamma follows."])
        self.assertIn("Alpha", summary)
        self.store.put("scratch", "a", {"value": 1})
        self.store.put("scratch", "b", {"value": 2})
        removed = prune_namespace(self.store, "scratch", keep_last=1)
        self.assertEqual(removed, 1)


if __name__ == "__main__":
    unittest.main()

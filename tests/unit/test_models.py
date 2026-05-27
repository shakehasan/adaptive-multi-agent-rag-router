"""Model adapter unit tests."""

from __future__ import annotations

import unittest
from pathlib import Path

from amarr.core.config import AppConfig
from amarr.models.base import EmbeddingRequest, ModelRequest
from amarr.models.messages import ChatPrompt
from amarr.models.mock import DeterministicMockChatAdapter, MockEmbeddingAdapter, MockRerankAdapter
from amarr.models.registry import ModelRegistry
from amarr.models.structured import parse_json_object, validate_schema


class ModelTests(unittest.TestCase):
    """Validate deterministic model layer behavior."""

    def test_mock_chat_is_deterministic(self) -> None:
        adapter = DeterministicMockChatAdapter("fast_small")
        request = ModelRequest(ChatPrompt.from_user("plan local retrieval"), "fast_small")
        first = adapter.complete(request)
        second = adapter.complete(request)
        self.assertEqual(first.text, second.text)
        self.assertIn("fast_small", first.text)

    def test_mock_embedding_shape(self) -> None:
        adapter = MockEmbeddingAdapter(dimensions=16)
        response = adapter.embed(EmbeddingRequest(["alpha beta", "beta gamma"]))
        self.assertEqual(len(response.vectors), 2)
        self.assertEqual(len(response.vectors[0]), 16)

    def test_mock_reranker_scores_overlap(self) -> None:
        reranker = MockRerankAdapter()
        scores = reranker.rerank("local routing evidence", ["local evidence", "unrelated words"])
        self.assertGreater(scores[0], scores[1])

    def test_registry_health(self) -> None:
        config = AppConfig.defaults()
        registry = ModelRegistry.from_config(config, mock=True)
        statuses = registry.health()
        self.assertGreaterEqual(len(statuses), 5)
        self.assertTrue(all(status.ok for status in statuses))

    def test_structured_parser(self) -> None:
        data = parse_json_object('prefix {"answer": "yes", "score": 1} suffix')
        validate_schema(data, {"answer": str, "score": int})
        self.assertEqual(data["answer"], "yes")


if __name__ == "__main__":
    unittest.main()

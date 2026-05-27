"""Config, path, and tool tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from amarr.core.config import AppConfig, parse_simple_yaml
from amarr.core.health import HealthReport, render_health_table, storage_health
from amarr.core.paths import PathPolicy, is_local_endpoint, require_local_endpoint
from amarr.tools.calculator import CalculatorTool
from amarr.tools.code_inspector import CodeInspectorTool
from amarr.tools.file_reader import FileReaderTool
from amarr.tools.planner_tool import PlannerTool
from amarr.tools.safety_tool import SafetyTool


class ConfigToolsPathsTests(unittest.TestCase):
    """Validate local config, path safety, and tools."""

    def test_parse_simple_yaml_nested_lists(self) -> None:
        data = parse_simple_yaml(
            """
            environment: local
            models:
              fast_small:
                type: mock
                capabilities:
                  - routing
                  - classification
            """
        )
        self.assertEqual(data["environment"], "local")
        self.assertEqual(data["models"]["fast_small"]["capabilities"], ["routing", "classification"])

    def test_config_defaults_validate(self) -> None:
        config = AppConfig.defaults()
        config.validate()
        self.assertFalse(config.enable_telemetry)
        self.assertIn("fast_small", config.models)

    def test_path_policy_blocks_escape_and_allows_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inside = root / "note.txt"
            inside.write_text("local", encoding="utf-8")
            policy = PathPolicy(root)
            self.assertEqual(policy.resolve("note.txt"), inside.resolve())
            with self.assertRaises(Exception):
                policy.resolve("../outside.txt")

    def test_local_endpoint_validation(self) -> None:
        self.assertTrue(is_local_endpoint("http://localhost:9000"))
        self.assertEqual(require_local_endpoint("http://127.0.0.1:9000"), "http://127.0.0.1:9000")
        self.assertFalse(is_local_endpoint("https://example.invalid"))

    def test_health_report_and_storage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = HealthReport()
            for status in storage_health(root / "state", root / "vector", root / "traces"):
                report.add(status)
            self.assertTrue(report.ok())
            self.assertIn("component", render_health_table(report))

    def test_calculator_tool(self) -> None:
        result = CalculatorTool().run(expression="2 + 3 * 4")
        self.assertTrue(result.ok)
        self.assertEqual(result.data["value"], 14.0)

    def test_file_reader_tool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "a.txt"
            path.write_text("hello", encoding="utf-8")
            result = FileReaderTool(root).run(path=str(path))
            self.assertEqual(result.output, "hello")

    def test_code_inspector_tool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.py"
            path.write_text("class A:\n    pass\ndef f():\n    return 1\n", encoding="utf-8")
            result = CodeInspectorTool().run(path=str(path))
            self.assertIn("1 classes", result.output)
            self.assertIn("f", result.data["functions"])

    def test_planner_and_safety_tools(self) -> None:
        plan = PlannerTool().run(query="debug code").data["steps"]
        self.assertIn("inspect code context", plan)
        safety = SafetyTool().run(query="explain local routing")
        self.assertTrue(safety.ok)
        rejected = SafetyTool().run(query="dump private key")
        self.assertFalse(rejected.ok)


if __name__ == "__main__":
    unittest.main()

"""Evaluation report writing."""

from __future__ import annotations

from pathlib import Path

from amarr.core.serialization import dump_json
from amarr.core.types import EvaluationSummary


def write_reports(summaries: list[EvaluationSummary], output_dir: Path) -> tuple[Path, Path]:
    """Write JSON and Markdown reports."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "eval_report.json"
    md_path = output_dir / "eval_report.md"
    dump_json(json_path, summaries)
    lines = ["# Evaluation Report", ""]
    for summary in summaries:
        lines.append(f"## {summary.name}")
        lines.append("")
        for key, value in summary.metrics.items():
            lines.append(f"- {key}: {value:.3f}")
        lines.append(f"- passed: {summary.passed}")
        if summary.notes:
            lines.append("")
            lines.extend(f"- {note}" for note in summary.notes)
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

"""Evaluation diagnostic helpers."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MetricBand:
    """Named interpretation band for a metric."""

    name: str
    minimum: float
    maximum: float
    description: str

    def contains(self, value: float) -> bool:
        """Return whether value is in the band."""
        return self.minimum <= value <= self.maximum


DEFAULT_BANDS = [
    MetricBand("needs_attention", 0.0, 0.49, "metric is below the desired local baseline"),
    MetricBand("acceptable", 0.50, 0.74, "metric is usable but should be improved"),
    MetricBand("strong", 0.75, 0.89, "metric is strong for the local deterministic suite"),
    MetricBand("excellent", 0.90, 1.0, "metric is excellent for the local deterministic suite"),
]


@dataclass(slots=True)
class DiagnosticReport:
    """Human-readable evaluation diagnostics."""

    metric_notes: dict[str, str] = field(default_factory=dict)
    action_items: list[str] = field(default_factory=list)

    def markdown(self) -> str:
        """Render diagnostics as Markdown."""
        lines = ["### Diagnostics", ""]
        for metric, note in sorted(self.metric_notes.items()):
            lines.append(f"- {metric}: {note}")
        if self.action_items:
            lines.append("")
            lines.append("Action items:")
            lines.extend(f"- {item}" for item in self.action_items)
        return "\n".join(lines)


def interpret_metric(value: float, bands: list[MetricBand] | None = None) -> MetricBand:
    """Interpret a metric value using bands."""
    for band in bands or DEFAULT_BANDS:
        if band.contains(value):
            return band
    return DEFAULT_BANDS[0]


def diagnose_metrics(metrics: dict[str, float]) -> DiagnosticReport:
    """Create diagnostics for a metric dictionary."""
    report = DiagnosticReport()
    for name, value in metrics.items():
        band = interpret_metric(value)
        report.metric_notes[name] = f"{band.name}: {band.description}"
        if band.name in {"needs_attention", "acceptable"}:
            report.action_items.append(f"improve {name} with targeted local eval cases")
    if not report.action_items:
        report.action_items.append("continue monitoring local regression reports")
    return report

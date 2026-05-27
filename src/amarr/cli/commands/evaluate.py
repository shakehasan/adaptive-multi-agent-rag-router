"""CLI evaluate command."""
from __future__ import annotations
from amarr.app.dependencies import build_context

def run(args) -> int:
    context = build_context(mock=args.mock)
    result = context.evaluate()
    for summary in result["summaries"]:
        metric_text = ", ".join(f"{key}={value:.3f}" for key, value in summary["metrics"].items())
        print(f"{summary['name']}: {metric_text}")
    print(f"json: {result['json']}")
    print(f"markdown: {result['markdown']}")
    return 0

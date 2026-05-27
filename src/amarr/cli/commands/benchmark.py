"""CLI routing benchmark command."""
from __future__ import annotations
from amarr.app.dependencies import build_context
from amarr.routing.benchmarks import run_routing_benchmark
from amarr.routing.router import Router

def run(args) -> int:
    context = build_context(mock=args.mock)
    router = Router(context.config, context.registry)
    results = run_routing_benchmark(router)
    passed = sum(1 for item in results if item.passed)
    for item in results:
        mark = "pass" if item.passed else "fail"
        print(f"{mark}: {item.selected} expected {item.expected} :: {item.query}")
    print(f"passed {passed}/{len(results)}")
    return 0 if passed == len(results) else 1

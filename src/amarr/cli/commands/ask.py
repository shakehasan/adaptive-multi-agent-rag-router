"""CLI ask command."""
from __future__ import annotations
from amarr.app.dependencies import build_context

def run(args) -> int:
    context = build_context(mock=args.mock)
    result = context.query(args.query)
    answer = result["answer"]
    print(answer.get("final_answer", ""))
    print()
    print(f"selected route: {answer.get('selected_route', '')}")
    print(f"confidence: {answer.get('confidence', 0):.2f}")
    print("citations:")
    for citation in answer.get("citations", []):
        print(f"- {citation['chunk_id']}: {citation['preview']}")
    return 0

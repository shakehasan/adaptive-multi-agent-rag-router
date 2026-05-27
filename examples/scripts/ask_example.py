"""Ask the sample end-to-end question."""
from __future__ import annotations
from amarr.app.dependencies import build_context
QUESTION = "What design principles does this knowledge base recommend for building reliable local AI systems?"
if __name__ == "__main__":
    print(build_context(mock=True).query(QUESTION)["answer"]["final_answer"])

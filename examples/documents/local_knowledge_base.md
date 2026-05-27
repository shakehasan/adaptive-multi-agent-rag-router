# Local Knowledge Base

Reliable local AI systems should keep user documents, memory, traces, and indexes in local storage by default. A local-first design reduces operational risk because every important artifact is available for inspection.

The knowledge base recommends deterministic fallbacks for development and evaluation. Mock responses, stable embeddings, and replay fixtures make failures reproducible and reduce ambiguity during debugging.

Routing should be explicit. A system that labels planning, retrieval, coding, critique, verification, and synthesis work can choose the smallest capable model alias for each step while preserving traceability.

Evidence should be cited. Every retrieved chunk should retain a source id and chunk id so the final answer can explain where claims came from.

# Design Decisions

## Local First

Local-first execution makes the project easy to review, easy to test, and safe to run in constrained environments. The default mock adapters keep the complete path runnable immediately.

## Generic Adapters

Model adapters are split by capability rather than by vendor. This keeps routing policy independent from the concrete endpoint a user chooses.

## Hybrid Retrieval

Keyword retrieval is precise for exact terms, while deterministic embeddings provide soft matching. Fusion improves robustness without requiring a heavyweight local database.

## Typed Messages

Agents communicate through dataclasses so state transitions, audit logs, tests, and trace exports all share the same shape.

## Local Observability

Trace spans are written as JSON and rendered as local HTML. This keeps debugging practical while avoiding external monitoring requirements.

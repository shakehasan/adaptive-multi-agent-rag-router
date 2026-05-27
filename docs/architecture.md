# Architecture

Adaptive Multi-Agent RAG Router is a local-first reference system for complex question answering. The architecture makes every stage explicit: safety and intent classification, routing, planning, retrieval, coworker execution, verification, synthesis, and trace export.

![Architecture](../assets/architecture.svg)

## Request Flow

1. A request enters through the CLI, local API, or browser demo.
2. The safety tool checks for unsupported actions and records a local event.
3. The router classifies task type, complexity, and capability needs.
4. The supervisor creates a task state and delegates work to agents.
5. The planner decomposes the query into subtasks.
6. The retrieval agent gathers evidence from local indexes.
7. Coworker agents research, critique, inspect code, or summarize.
8. The verifier checks that claims map back to evidence.
9. The synthesizer returns a cited answer and confidence metadata.
10. The trace writer exports spans to local JSON and optional HTML.

## Boundaries

The model layer is intentionally generic. It supports local chat, completion, embedding, and reranking endpoints through neutral aliases. The default deterministic adapters make tests and demos reproducible without any external dependency.

## Tradeoffs

The repository favors transparent interfaces over hidden framework behavior. The RAG store uses simple files so reviewers can inspect state easily. The local server uses the standard library to keep installation light. The architecture is modular enough to swap in stronger storage, scheduling, or inference backends while preserving the same typed contracts.

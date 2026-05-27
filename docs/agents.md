# Agents

The agent system uses a supervisor-worker pattern with typed messages and shared task state.

![Agents](../assets/agent-graph.svg)

## Supervisor

The supervisor owns the workflow, selects which coworker agents run, records state changes, handles recoverable failures, and requests synthesis when verification passes.

## Planner

The planner converts a user question into a small task graph. It marks retrieval needs, code inspection needs, and verification criteria.

## Retrieval And Research

The retrieval agent calls the RAG pipeline. The researcher reads evidence and produces concise findings with citations.

## Coding And Critique

The coding agent handles implementation-oriented requests. The critic reviews the current plan and evidence for missing context, vague claims, or weak support.

## Verification And Synthesis

The verifier checks grounding and confidence. The synthesizer writes a final response with citations, active agents, route metadata, and verification notes.

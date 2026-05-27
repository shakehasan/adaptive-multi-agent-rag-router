# Adaptive Multi-Agent RAG Router

**World-class local NLP architecture for multi-agent RAG, intelligent model routing, grounded citations, evaluation, memory, and fully auditable reasoning traces.**

`local-first` `NLP` `multi-agent` `RAG` `model-routing` `hybrid-search` `evaluation` `observability` `privacy-first` `no-telemetry`

![Architecture](assets/architecture.svg)

Adaptive Multi-Agent RAG Router is a production-grade reference implementation for building serious local AI systems. It shows how to orchestrate specialized agents, route tasks across neutral model aliases, retrieve evidence from a local knowledge base, verify grounded answers, and inspect every decision through local traces.

This is not a toy chat wrapper. It is an AI systems architecture portfolio project: modular, typed, testable, local-first, and built to demonstrate senior-level thinking across retrieval, orchestration, routing, evaluation, privacy, and operational visibility.

## Why This Repository Stands Out

- **Local-first AI architecture**: no account setup, no billing, no telemetry, no remote dependency required.
- **Supervisor-worker agent system**: planner, retriever, researcher, coder, critic, verifier, synthesizer, and fallback agents.
- **Dynamic model routing**: rule-based, score-based, policy-based, fallback-aware routing across neutral aliases.
- **Hybrid RAG pipeline**: document ingestion, normalization, chunking, deterministic embeddings, keyword search, vector search, rank fusion, reranking, citations, and grounding checks.
- **Evaluation maturity**: retrieval recall, citation precision, answer faithfulness, route accuracy, workflow success, and latency reporting.
- **Local observability**: structured traces, route timelines, agent timelines, retrieval timelines, redaction, and a local HTML trace viewer.
- **Portfolio-grade engineering**: clean interfaces, dataclasses, typed messages, deterministic tests, CLI, API server, browser demo, docs, and visual architecture diagrams.

## System Flow

```text
User Query
  -> Safety and Intent Classifier
  -> Router
  -> Supervisor Agent
  -> Planner
  -> RAG Retriever
  -> Coworker Agents
  -> Critic
  -> Verifier
  -> Synthesizer
  -> Final Answer with citations, route metadata, confidence, and trace id
```

The design makes every important decision inspectable. A reviewer can see why a route was chosen, which evidence was retrieved, which agents participated, what the verifier checked, and how confidence was calculated.

## Architecture

![Routing Flow](assets/routing-flow.svg)

The system is split into explicit architecture layers:

| Layer | Responsibility |
| --- | --- |
| `core` | config, validation, ids, events, serialization, health, local path safety |
| `models` | generic local chat, completion, embedding, mock, replay, streaming, structured output |
| `routing` | task classification, candidate scoring, policies, circuit breakers, fallback, decision logs |
| `agents` | supervisor-worker orchestration, typed messages, task state, recovery planning |
| `rag` | loaders, chunking, normalization, embeddings, keyword index, vector store, hybrid retrieval |
| `memory` | conversation memory, task memory, long-term memory, summarization, pruning |
| `evaluation` | datasets, retrieval metrics, route metrics, workflow metrics, reports |
| `observability` | spans, traces, timeline export, redaction, local HTML viewer |
| `app` / `cli` / `demo` | local API, command-line interface, browser demo |

## Model Routing Aliases

The repository uses neutral aliases so users can map them to any locally available open model endpoint of their choice. No hosted account is required.

| Alias | Role | Typical Tasks |
| --- | --- | --- |
| `reasoning_large` | Deep reasoning | planning, synthesis, verification |
| `coding_large` | Code intelligence | code review, code generation, debugging |
| `fast_small` | Fast utility model | classification, routing, summaries |
| `retrieval_embedder` | Embeddings | document and query embeddings |
| `rerank_local` | Reranking | context ranking and evidence ordering |

Routing decisions are logged with candidate scores, selected alias, policy, fallback state, attempts, and rationale.

## Agent Graph

![Agent Graph](assets/agent-graph.svg)

| Agent | Purpose |
| --- | --- |
| Supervisor | Owns the workflow, delegates work, records state, handles recoverable failure |
| Planner | Converts the query into concrete subtasks and verification criteria |
| Retrieval | Calls the RAG pipeline and returns scored evidence chunks |
| Researcher | Summarizes retrieved evidence into cited findings |
| Coder | Handles code-oriented questions and code inspection workflows |
| Critic | Finds missing context, ambiguity, weak evidence, and risk |
| Verifier | Checks grounding, citation coverage, unsupported claims, and confidence |
| Synthesizer | Produces the final answer with citations and metadata |
| Fallback | Returns a safe local response when the standard workflow cannot complete |

Agents communicate through typed messages and shared task state. The graph is intentionally reviewable rather than hidden behind framework magic.

## RAG Pipeline

![RAG Flow](assets/rag-flow.svg)

The retrieval system is designed for reproducible local NLP:

1. Load local Markdown and text documents.
2. Normalize text and extract metadata.
3. Split documents into overlapping chunks.
4. Build deterministic local embeddings.
5. Build a local keyword index.
6. Retrieve with vector search and keyword search.
7. Fuse rankings with reciprocal rank fusion.
8. Rerank evidence locally.
9. Generate citations from stable source and chunk ids.
10. Verify answer grounding before synthesis is accepted.

## Evaluation Dashboard

![Evaluation Dashboard](assets/evaluation-dashboard.svg)

The evaluation suite measures the parts that matter in real AI systems:

| Metric | What It Checks |
| --- | --- |
| retrieval recall | Whether expected evidence appears in retrieved chunks |
| citation precision | Whether citations point to useful supporting context |
| answer faithfulness | Whether answer claims overlap with evidence |
| route accuracy | Whether the router selects the expected capability |
| workflow success | Whether the agent graph completes required stages |
| latency | Local timing across routing, retrieval, and workflow execution |

Reports are generated as JSON and Markdown under `.amarr/evals`.

## Quickstart

```bash
python -m venv .venv
# Activate the virtual environment with the command for your shell.
python -m pip install -e .
copy .env.example .env
python -m amarr.cli.main ingest examples/documents
python -m amarr.cli.main ask "What design principles does this knowledge base recommend for building reliable local AI systems?"
python -m amarr.cli.main evaluate
python -m amarr.cli.main benchmark-routing
python -m amarr.cli.main serve --mock --port 8765
```

Mock mode is the default. It works immediately with no downloads, no internet, no remote account, and no paid service.

## CLI

```bash
python -m amarr.cli.main ingest examples/documents
python -m amarr.cli.main ask "What are the key system design principles?"
python -m amarr.cli.main evaluate
python -m amarr.cli.main trace latest
python -m amarr.cli.main benchmark-routing
python -m amarr.cli.main inspect config
python -m amarr.cli.main serve
```

## Local API

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | `GET` | Local server health |
| `/config` | `GET` | Safe configuration view |
| `/ingest` | `POST` | Ingest local documents |
| `/query` | `POST` | Run the full agent workflow |
| `/traces` | `GET` | List local traces |
| `/traces/{trace_id}` | `GET` | Inspect a specific trace |
| `/evaluate` | `POST` | Run local evaluations |

## Example Output

```text
Final answer:
Reliable local AI systems should isolate local data, make model routing explicit,
retain deterministic fallbacks, verify evidence before synthesis, and keep every
trace available for inspection.

Cited sources:
- engineering_handbook.md#chunk-2
- local_knowledge_base.md#chunk-1
- research_notes.md#chunk-3

Selected route: reasoning_large
Active agents: supervisor, planner, retrieval, researcher, critic, verifier, synthesizer
Confidence score: 0.86
Retrieval evidence: 5 chunks after hybrid fusion and local reranking
Verification notes: all major claims are supported by cited evidence
```

## Libraries And Runtime

This project is intentionally standard-library-first. It does not require external packages for runtime, tests, the API server, the CLI, the demo, retrieval, routing, evaluation, or tracing.

| Area | Libraries / Modules Used |
| --- | --- |
| CLI | `argparse`, `pathlib` |
| Local API and demo server | `http.server`, `mimetypes`, `urllib`, `json` |
| Typed architecture | `dataclasses`, `typing`, `enum`, `abc`, `collections` |
| Local persistence | `json`, `pathlib`, plain local files |
| RAG and NLP utilities | `re`, `hashlib`, `math`, `collections.Counter` |
| Model adapters | `urllib.request`, `urllib.parse`, deterministic mock adapters |
| Evaluation and tests | `unittest`, `tempfile`, `contextlib`, `io` |
| Observability | local JSON traces, HTML rendering with `html` |

External libraries: **none required**. Users can optionally connect neutral local model endpoints through alias configuration.

## Privacy And Security

- No remote account is required.
- No telemetry is sent.
- No paid service is required.
- Documents remain local.
- Memory remains local.
- Traces remain local.
- Evaluation reports remain local.
- Local endpoint mode is opt-in.
- Redaction utilities are included for trace review.

## Validation

```bash
python scripts/check_forbidden_names.py
python scripts/syntax_check.py
python scripts/count_lines.py
python scripts/run_all_tests.py
```

The repository includes deterministic tests for routing, fallback, circuit breakers, model adapters, RAG retrieval, citations, grounding, memory, evaluation, observability, local API behavior, and end-to-end query workflows.

## What This Demonstrates

This repository demonstrates how to design an AI system as an actual platform:

- agent orchestration rather than a single prompt chain
- retrieval with auditable evidence rather than unsupported generation
- model routing as a first-class architecture concern
- local-first privacy and reproducibility
- deterministic evaluation instead of vibes-only demos
- traces, timelines, and redaction for operational review
- clean Python interfaces that can be inspected and extended

## Visual Index

![Architecture](assets/architecture.svg)
![Routing](assets/routing-flow.svg)
![RAG](assets/rag-flow.svg)
![Agents](assets/agent-graph.svg)
![Evaluation](assets/evaluation-dashboard.svg)

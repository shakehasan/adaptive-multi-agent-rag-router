# Product Specs

The browser demo contains five panels: chat, retrieval evidence, route decisions, agent trace, and confidence. The demo runs against the local API server and does not load remote assets.

The CLI supports document ingestion, direct questions, agent workflows, evaluation, trace inspection, routing benchmarks, and local demo serving.

The API exposes health, ingest, query, traces, evaluation, and config endpoints. Every endpoint is intended for local use.

The default mode is mock mode. Local endpoint mode is optional and uses neutral aliases configured through environment variables.

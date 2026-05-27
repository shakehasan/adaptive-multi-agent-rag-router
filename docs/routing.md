# Routing

Routing chooses a neutral model alias for each task. The router combines rules, scores, policies, circuit breaker state, retries, timeout configuration, and structured decision logs.

![Routing](../assets/routing-flow.svg)

## Aliases

- `reasoning_large` handles planning, verification, and synthesis.
- `coding_large` handles code generation, code review, debugging, and architecture inspection.
- `fast_small` handles classification, routing, short summaries, and lightweight transformations.
- `retrieval_embedder` creates document and query embeddings.
- `rerank_local` orders retrieved context.

## Policies

The balanced policy prefers the smallest capable alias while respecting complexity. The quality policy gives higher weight to reasoning capabilities. The economy policy keeps short transformations on `fast_small` when safe.

## Fallback

If the selected alias is unhealthy or its circuit is open, fallback routing chooses the next healthy candidate. Retries are recorded as decision metadata so failures remain inspectable.

## Circuit Breakers

Each alias has failure counters, cooldown state, and success recovery. Repeated failures open a circuit. A half-open probe can later restore the alias without losing observability.

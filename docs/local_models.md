# Local Models

The repository uses neutral aliases instead of naming concrete models or services. Users can map each alias to any locally available open model endpoint that follows the simple local HTTP contracts.

## Aliases

- `reasoning_large`
- `coding_large`
- `fast_small`
- `retrieval_embedder`
- `rerank_local`

## Mock Mode

Mock mode is the default and works immediately. It uses deterministic adapters for chat, embeddings, and reranking so the demo, CLI, tests, and evaluations run without downloads.

## Local Endpoint Mode

Set the endpoint variables in `.env` and enable local network mode only when you intentionally want to call local endpoints. The adapters validate that endpoints use local hosts.

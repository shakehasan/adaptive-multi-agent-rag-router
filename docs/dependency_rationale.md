# Dependency Rationale

The runtime depends only on the Python standard library. This keeps the project free to run locally, easy to audit, and independent from external package services once Python is available.

## Library Inventory

| Area | Libraries / Modules | Rationale |
| --- | --- | --- |
| CLI | `argparse`, `pathlib` | Provides a portable command interface and local path handling. |
| API server | `http.server`, `mimetypes`, `urllib.parse` | Runs a local HTTP server without a web framework. |
| Serialization | `json`, `dataclasses`, `enum` | Keeps traces, indexes, reports, and state inspectable. |
| Configuration | `os`, `re`, `textwrap`, `pathlib` | Loads local YAML-like config examples and environment overrides. |
| RAG / NLP | `re`, `hashlib`, `math`, `collections.Counter` | Supports tokenization, deterministic embeddings, vector scoring, and keyword search. |
| Model adapters | `urllib.request`, `urllib.error`, `urllib.parse` | Calls optional local endpoints through generic HTTP contracts. |
| Memory | `json`, `pathlib` | Persists conversation, task, and long-term memory locally. |
| Evaluation | `unittest`, `time`, `statistics-style helpers` | Runs deterministic local tests and metric reports. |
| Observability | `html`, `contextlib`, `time` | Writes local traces and renders a local HTML viewer. |
| Scripts | `ast`, `base64`, `re`, `pathlib` | Validates syntax, line count, and forbidden terms without external tools. |

## External Dependencies

None are required. The project is designed to run with Python alone.

Development can still use optional tools if a contributor chooses, but the repository does not require them.

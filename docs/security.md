# Security And Privacy

The default execution mode is local-only. Documents, indexes, traces, memory, and reports remain in the workspace.

## Network Posture

External network access is disabled by default. When local endpoint mode is enabled, adapters only accept loopback-style local URLs.

## Redaction

The observability layer includes prompt and response redaction helpers. Redaction can remove long numeric sequences, local path details, and configured sensitive terms before traces are viewed.

## File Access

Tools resolve paths under an allowed root and reject traversal outside that root. The file reader is read-only. The demo does not load external assets.

## Trace Storage

Trace files are plain local JSON. The trace viewer renders local files through the local API server and sends nothing elsewhere.

# Failure Recovery Playbook

## Missing Index
Symptom: retrieval reports that local indexes are missing.
Recovery: run ingestion for the target document directory.
Trace expectation: an ingest span records document and chunk counts.
Verification: a follow-up query returns at least one evidence chunk.

## Weak Evidence
Symptom: retrieval returns chunks with low term coverage.
Recovery: inspect query terms, increase top_k, or add a more direct document.
Trace expectation: retrieval quality notes show weak coverage.
Verification: citation previews contain the important terms from the query.

## Unhealthy Alias
Symptom: selected alias fails health checks or opens a circuit.
Recovery: choose the fallback alias and record fallback_used in the route decision.
Trace expectation: route decision includes candidate scores and circuit state.
Verification: the workflow continues in mock mode or with another healthy local endpoint.

## Timeout
Symptom: a local endpoint exceeds the configured time budget.
Recovery: retry with a shorter context and lower max token budget.
Trace expectation: retry count and timeout detail are stored locally.
Verification: final confidence includes a penalty if evidence is incomplete.

## Unsupported Claim
Symptom: verifier finds an answer sentence with weak evidence overlap.
Recovery: either retrieve more evidence or lower confidence and add a verification note.
Trace expectation: unsupported claims appear in workflow metadata.
Verification: the final answer cites only supported claims.

## Stale Memory
Symptom: conversation or long-term memory conflicts with current retrieved evidence.
Recovery: prefer cited evidence, prune stale memory, and summarize durable facts.
Trace expectation: memory use is visible in agent messages.
Verification: final answer mentions current evidence rather than old scratchpad content.

## Tool Rejection
Symptom: file access or calculator input is rejected.
Recovery: explain the local safety rule and continue with available context.
Trace expectation: tool result includes ok=false and a short reason.
Verification: no filesystem path outside the allowed root is read.

## Evaluation Regression
Symptom: route accuracy, retrieval recall, or citation precision drops below the local baseline.
Recovery: inspect the failing case, compare traces, and add a focused regression test.
Trace expectation: the evaluation report links failures to query text and metrics.
Verification: rerun the deterministic suite and compare report values.

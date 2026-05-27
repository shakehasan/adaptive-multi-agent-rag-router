# Reliability Patterns

## Pattern 1: Explicit Local Boundaries
Reliable local AI systems define a clear boundary around documents, traces, memory, indexes, and configuration.
The boundary should be visible in code and easy to inspect during review.
A local boundary prevents accidental dependency on external runtime behavior.
The boundary also makes tests simpler because state can be created and removed deterministically.

## Pattern 2: Deterministic Mock Execution
A serious local system should boot in mock mode before it connects to any model endpoint.
Mock mode should exercise the same router, retriever, agent graph, verifier, and synthesizer used by endpoint mode.
Deterministic responses make failures reproducible and make evaluation results comparable across runs.
Mock mode should not be a separate toy path; it should be a realistic local substitute.

## Pattern 3: Observable Routing
Route decisions should explain task classification, candidate scores, selected alias, policy, fallback state, and retry attempts.
Reviewers should be able to answer why a query used reasoning_large instead of fast_small.
A route table should include capability score, speed score, stability score, and total score.
Circuit breaker transitions should be traceable rather than hidden in logs.

## Pattern 4: Evidence Before Answering
Retrieval should happen before synthesis for knowledge-base questions.
Evidence chunks should include source id, chunk id, score, and preview.
The synthesizer should cite local evidence instead of relying on unsupported statements.
The verifier should check whether answer claims overlap with retrieved evidence.

## Pattern 5: Graceful Degradation
Local systems should degrade predictably when an index is missing, an alias is unhealthy, or evidence is weak.
Recovery plans should rebuild indexes, choose fallback aliases, shorten context, or return a safe fallback answer.
Every degradation should appear in the trace so a reviewer can reproduce it.
The user should receive confidence metadata when the answer is uncertain.

## Pattern 6: Small Interfaces
Agents should communicate with typed messages and shared state instead of passing unstructured strings through hidden globals.
Retrieval should expose a small evidence interface.
Routing should expose a route decision object.
Evaluation should consume the same answers and evidence that production paths create.

## Pattern 7: Local Evaluation
Evaluation should run without network access and should not rely on external datasets.
Synthetic cases should test recall, citation precision, route accuracy, workflow success, and latency.
Reports should include both machine-readable JSON and reviewer-friendly Markdown.
The benchmark should be deterministic so regressions are easy to identify.

## Pattern 8: Inspectable Persistence
Local persistence should favor simple formats when the project is meant for review.
JSON traces, JSON indexes, and Markdown reports are easy to inspect.
More advanced storage can be added behind interfaces after the core architecture is validated.
Simplicity is a reliability feature when it improves reviewability.

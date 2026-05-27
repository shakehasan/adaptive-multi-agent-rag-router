# Engineering Handbook

The system design principles are separation of concerns, local persistence, deterministic testing, graceful fallback, and inspectable execution.

Agents should communicate with typed messages instead of hidden shared strings. Typed messages make traces clearer and make tests easier to write.

A supervisor should coordinate workflow stages but avoid doing every task itself. Coworker agents should own planning, retrieval, research, critique, verification, synthesis, and code inspection.

Failure recovery should be boring and visible. Retries, fallback route decisions, circuit breaker transitions, and verification failures should be written to local traces.

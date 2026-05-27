# Routing Benchmark Notes

## Case 1
Query: Summarize this short note.
Expected alias: fast_small.
Reason: the task is short, low complexity, and utility oriented.
Expected trace: classification mentions a short utility task.

## Case 2
Query: Debug this function and explain the failing test.
Expected alias: coding_large.
Reason: the query contains code, debug, function, and test indicators.
Expected trace: route candidates show coding_large with the strongest capability score.

## Case 3
Query: What design principles guide reliable local AI systems?
Expected alias: reasoning_large.
Reason: architecture and design tasks require planning, synthesis, and verification.
Expected trace: supervisor delegates planning, retrieval, research, critique, verification, and synthesis.

## Case 4
Query: Verify whether these claims are supported by the citations.
Expected alias: reasoning_large.
Reason: verification requires careful evidence checking and answer faithfulness.
Expected trace: verifier records grounding notes and unsupported claims when present.

## Case 5
Query: Route this one sentence.
Expected alias: fast_small.
Reason: the task is narrow and can be handled by a fast classification path.
Expected trace: no retrieval span is required unless the workflow explicitly asks for evidence.

## Case 6
Query: Review this module for architecture boundaries and test gaps.
Expected alias: coding_large.
Reason: the task combines code review, architecture, and tests.
Expected trace: coding agent contributes a code-specific finding.

## Case 7
Query: Compare retrieval strategies for evidence-heavy local question answering.
Expected alias: reasoning_large.
Reason: the task asks for comparison and synthesis over evidence.
Expected trace: retrieval quality diagnostics should be attached to the answer metadata.

## Case 8
Query: Create a concise summary of the last message.
Expected alias: fast_small.
Reason: short summarization is a lightweight utility task.
Expected trace: route confidence is high because the task is simple.

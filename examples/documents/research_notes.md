# Research Notes

Hybrid retrieval performs better than a single retrieval strategy when documents contain both exact terminology and paraphrased concepts. Keyword search finds exact terms, vector search finds nearby language, and rank fusion balances both.

Grounding checks should happen before synthesis is accepted. A final answer should not merely sound plausible; it should map claims to cited evidence.

Confidence should combine retrieval quality, verification coverage, and route stability. A high confidence answer has relevant evidence, adequate citations, and no critical verifier warnings.

Evaluation should be local and repeatable. Synthetic datasets can cover retrieval recall, citation precision, route accuracy, workflow success, and latency.

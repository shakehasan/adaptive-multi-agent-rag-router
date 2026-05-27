# Evaluation

Evaluation is local, deterministic, and repeatable. The suite measures retrieval, citation quality, answer grounding, route decisions, agent workflow success, and latency.

## Datasets

Synthetic examples are generated from local documents. Each item includes a query, expected evidence terms, expected route family, and minimal answer criteria.

## Metrics

- Retrieval recall: expected evidence found in top results.
- Citation precision: cited chunks that support answer claims.
- Faithfulness: overlap between answer claims and evidence.
- Route accuracy: selected alias compared with expected capability.
- Workflow success: supervisor completed all required stages.
- Latency: per-stage and total timing from local traces.

## Reports

The runner writes JSON for machines and Markdown for humans under `.amarr/evals`. Reports include route tables, failure notes, and trace identifiers.

# Evaluation Design

## Purpose

The evaluation layer measures whether the workflow behaves consistently against known scenarios. Its purpose is to make comparison quality inspectable and regressions detectable.

The eval system is not a benchmark for general intelligence. It is a regression-oriented harness for a narrow policy-control audit workflow.

## Evaluation goals

The evaluation design focuses on five goals:

1. verify that deterministic contradiction logic behaves as intended
2. ensure citations are produced for material findings
3. confirm review routing remains consistent
4. expose degraded-mode behavior rather than hiding it
5. provide a machine-readable latest report for UI and CI usage

## Evaluation artifacts

### Eval datasets

Synthetic cases are stored under `evals/datasets/` and grouped by scenario family.

### Eval runs

`EvalRun` stores run label, status, configuration snapshot, summary metrics, and timestamps.

### Latest report

A machine-readable report is written to `evals/reports/latest.json`.

The eval API serves this report directly when present, and falls back to the latest stored `EvalRun.summary_metrics` when the JSON artifact is absent.

## Dataset families

The evaluation design uses explicit scenario groups.

### `contradiction_cases`

Cases that should produce a contradiction finding, such as timeline mismatches or direct control inconsistencies.

### `drift_cases`

Cases where version or wording drift should create a meaningful discrepancy or coverage concern.

### `stale_reference_cases`

Cases that test whether older referenced artifacts are recognized as stale in the presence of newer governing versions.

### `no_conflict_cases`

Cases that should not generate a contradiction. These help protect precision.

### `adversarial_cases`

Cases designed to stress brittle wording assumptions, paraphrases, or ambiguous phrasing.

### `fallback_cases`

Cases that exercise degraded behavior when assistive model components are unavailable or intentionally disabled.

## Case structure

A typical synthetic eval case includes:

- case identifier
- scenario type
- source and target document payloads
- expected statement patterns
- expected conflict type
- expected severity
- expected review requirement
- expected citation targets

This structure is designed to test end-to-end workflow behavior rather than only isolated functions.

## Metrics

The current seeded baseline exposes the following metrics:

- contradiction precision
- contradiction recall
- stale-reference accuracy
- citation validity rate
- review routing accuracy

These metrics are chosen because they reflect both detection quality and workflow quality.

## Why these metrics matter

### Contradiction precision

Helps answer whether generated findings are usually valid rather than noisy.

### Contradiction recall

Helps answer whether important seeded contradictions are being missed.

### Stale-reference accuracy

Captures a key governance-specific failure mode that ordinary text diff systems handle poorly.

### Citation validity rate

Ensures that findings remain evidence-backed rather than unsupported summaries.

### Review routing accuracy

Confirms that material findings are being pushed into the right human workflow.

## Threshold philosophy

The eval suite is designed to fail when important workflow quality drops below expected thresholds.

This keeps CI valuable. A passing build should mean more than syntax validity. It should also mean the core policy-audit workflow still behaves credibly against seeded cases.

## Current seeded baseline

The seeded baseline currently reports:

- contradiction precision: `0.89`
- contradiction recall: `0.86`
- stale-reference accuracy: `0.93`
- citation validity rate: `1.00`
- review routing accuracy: `0.91`

These values represent seeded regression targets for the current implementation, not claims of production performance.

## Eval execution flow

A typical eval flow is:

1. generate or load eval cases
2. execute current comparison logic against them
3. compute summary metrics
4. write `evals/reports/latest.json`
5. fail the process if required thresholds drop below the acceptable floor

This allows evals to support both local inspection and CI enforcement.

## Interaction with seeded workflow

The evaluation design complements the seeded demo data. Seeded data demonstrates the live application workflow, while eval datasets test repeatable scenario families more broadly.

## Design principles

### Deterministic and inspectable

Eval outputs should be understandable and reproducible.

### Workflow-aware

The system measures more than classification. It also measures evidence and routing behavior.

### Useful in CI

The eval suite should catch regressions that syntax checks and unit tests cannot.

### Honest in scope

These evals test a narrow audit workflow and should not be presented as general regulatory-intelligence benchmarks.

## v1 limitations

Not emphasized in v1:

- very large dataset management
- statistically rigorous confidence intervals
- human-annotated legal corpora
- cross-jurisdiction evaluation at scale
- model-vs-model benchmark leaderboards

## Summary

The evaluation design provides a regression-focused quality layer for the audit workflow. It measures whether contradictions, citations, stale references, and review routing continue to behave as intended across seeded synthetic scenarios.
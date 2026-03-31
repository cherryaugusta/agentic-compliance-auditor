# Contradiction Model

## Purpose

The contradiction model defines how the system identifies meaningful mismatches across policy artifacts. It exists to detect differences that matter operationally rather than merely flagging any textual variation.

The model is rules-first. Deterministic logic is authoritative. AI may assist with explanation or observability, but it does not override the core discrepancy logic.

## Comparison substrate

Comparisons are performed against normalized control statements extracted from sections.

A statement includes structured fields such as:

- statement type
- normalized text
- deadline text
- threshold text
- extraction confidence
- optional embedding

This gives the contradiction engine a controlled surface to inspect.

## Comparison run

A `ComparisonRun` captures one audit attempt between:

- one source document
- one or more target documents
- a run type
- a configuration snapshot
- lifecycle timestamps
- a correlation identifier

Comparison runs are explicit system objects because findings, model logs, metrics, and audit events all need a stable parent context.

## Rules-first principle

The contradiction engine begins from explicit pattern checks and state transitions.

Current seeded logic focuses on deterministic detection such as:

- timeline mismatches
- threshold mismatches
- degraded-mode handling when AI assistance is unavailable

This approach keeps findings reproducible, testable, and understandable.

## Current contradiction families

### Timeline conflict

Triggered when the source and target express different required timelines for comparable obligations.

Example:
source says within 10 business days  
target says within 5 business days

### Threshold conflict

Triggered when the source and target define different numeric thresholds.

Example:
source says above £500  
target says above £1,000

### Stale reference

Triggered when a document references an outdated artifact that appears to have been superseded or replaced in the active governance chain.

### Coverage gap

Used where a required concept appears in a governing source but is absent from an expected downstream implementation or aligned artifact.

### Terminology drift

Used where important wording has shifted enough to warrant inspection even if direct contradiction is not yet proven.

### Missing control

Used where a required control expression is expected but absent.

### Approval conflict

Used where approval or sign-off responsibilities differ across aligned documents.

### Weaker internal control

Used where an internal artifact appears to impose a less stringent requirement than a relevant governing source.

## Current seeded implementation

The seeded implementation materially exercises timeline and threshold conflict logic.

For timeline comparisons:

- extract day values from source and target
- compare numeric values
- create a `ConflictFlag` when they differ
- create source and target citations
- create a finding memo
- route a review task

For threshold comparisons:

- extract threshold values
- compare numeric values
- create equivalent downstream artifacts

## Finding structure

Each finding is represented by `ConflictFlag`.

Key fields include:

- comparison run
- source statement
- target statement
- conflict type
- severity
- status
- confidence
- requires review
- reason summary
- rules triggered
- model version

This model separates the discrepancy itself from supporting evidence and reviewer action.

## Citation model

Every meaningful finding should be supported by explicit citations.

Citations are stored as `EvidenceCitation` with:

- citation role
- document
- section
- excerpt text

This allows the system to show exactly which source and target text led to the finding.

## Memo model

A `FindingMemo` provides a structured summary and suggested action. In v1 it remains an assistive artifact, not the authoritative decision engine.

The memo captures:

- recommended action
- summary
- structured rationale
- confidence
- prompt version reference

## Severity model

Severity reflects the operational seriousness of the contradiction.

In the current implementation:

- timeline conflicts are treated as high severity
- threshold conflicts are treated as high severity
- stale-reference issues are treated as medium severity by default
- other types default conservatively until expanded scoring rules are added

## Degraded mode

If the contradiction-analysis prompt is unavailable, deterministic rules still run.

In degraded mode:

- findings may still be created
- review tasks may still be created
- citations are still attached
- model execution is logged as fallback
- comparison status becomes degraded rather than completed

This preserves continuity without pretending the assistive layer was available.

## Why this model is credible

The contradiction model is built around five credibility principles:

1. compare structured statements, not only raw documents
2. require concrete evidence excerpts
3. keep deterministic logic authoritative
4. preserve run-level context and auditability
5. allow human review where material discrepancies exist

## v1 limitations

The current contradiction engine is intentionally narrower than a production policy-analysis platform.

Not emphasized in v1:

- advanced semantic contradiction inference
- cross-document reasoning over many-hop dependency chains
- probabilistic contradiction ensembles
- large-scale retrieval-augmented matching
- regulatory interpretation

## Summary

The contradiction model identifies policy-control discrepancies through deterministic comparison of structured control statements. It prioritizes explainability, citations, reproducibility, and auditable workflow behavior over opaque automation.
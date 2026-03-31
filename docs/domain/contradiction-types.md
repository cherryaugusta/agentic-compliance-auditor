# Contradiction Types

## Purpose

This document defines the discrepancy categories used by the system when comparing policies, procedures, control libraries, and guidance. These categories are intended to represent operationally meaningful forms of misalignment, not just arbitrary text differences.

## `direct_contradiction`

### Definition

Two aligned statements express incompatible requirements in a way that cannot both be true in the same operational context.

### Example

- source: complaints must be acknowledged within 10 business days
- target: complaints must be acknowledged within 5 business days

### Why it matters

This creates immediate execution ambiguity and likely indicates a governance problem.

## `weaker_internal_control`

### Definition

An internal artifact appears to impose a less strict requirement than the controlling or aligned source it should satisfy.

### Example

- guidance requires proactive review of vulnerable-customer escalations
- internal procedure says review may occur when capacity allows

### Why it matters

The organization may be under-controlling a process relative to intended governance requirements.

## `missing_control`

### Definition

An expected control expression is absent from a downstream or aligned artifact.

### Example

A policy requires escalation logging, but the implementing procedure contains no logging step.

### Why it matters

A control gap may exist even without a direct contradiction.

## `stale_reference`

### Definition

A document references an older artifact that appears to have been superseded or replaced.

### Example

A procedure references control library v2 while control library v5 is active.

### Why it matters

Operational teams may be following outdated instructions or standards.

## `threshold_conflict`

### Definition

Two aligned statements express different quantitative thresholds.

### Example

- source: escalate above £500
- target: escalate above £1,000

### Why it matters

Threshold differences create inconsistent decisions, routing, and customer outcomes.

## `timeline_conflict`

### Definition

Two aligned statements express different required timelines.

### Example

- source: acknowledge within 10 business days
- target: acknowledge within 5 business days

### Why it matters

Timeline conflicts are usually operationally material and easy to audit against real process evidence.

## `approval_conflict`

### Definition

Two aligned statements assign different approval authority or sign-off expectations.

### Example

- policy: manager approval required
- procedure: team lead approval sufficient

### Why it matters

Approval ambiguity weakens governance and may create unauthorized actions.

## `terminology_drift`

### Definition

Wording has drifted enough to create interpretive risk even when a direct contradiction is not yet proven.

### Example

One document uses complaint escalation, another uses customer concern fast-track handling for what appears to be the same process boundary.

### Why it matters

Terminology drift can hide future control gaps or create inconsistent handling across teams.

## `coverage_gap`

### Definition

A source artifact covers a requirement area that a related downstream or aligned artifact does not cover adequately.

### Example

An external guidance document includes vulnerable-customer escalation expectations, but the internal aligned policy lacks any corresponding section.

### Why it matters

Coverage gaps often indicate silent governance drift rather than explicit conflict.

## Prioritization notes

Not all contradiction types carry equal operational risk.

In the current implementation:

- timeline conflicts are high severity
- threshold conflicts are high severity
- stale references are medium severity by default
- other types are available in the domain model and can receive expanded scoring rules over time

## Evidence expectations

Every contradiction type should ideally be supported by:

- source citation
- target citation where applicable
- a structured reason summary
- linked review handling for material cases

## Summary

These contradiction types provide a domain-specific vocabulary for policy-control drift. They help distinguish direct disagreement, missing implementation, outdated references, and broader governance misalignment.
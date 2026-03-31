# Severity Model

## Purpose

Severity expresses the operational significance of a finding. It helps determine how urgently a discrepancy should be reviewed and whether it should receive stronger routing, escalation, or scrutiny.

Severity is not the same as confidence. A finding can be high severity and still require review.

## Severity levels

### `low`

Used for issues with limited immediate operational impact or primarily informational value.

### `medium`

Used for meaningful governance concerns that warrant review but are not immediately among the highest-risk discrepancy classes.

### `high`

Used for contradictions likely to create materially inconsistent operational outcomes, customer treatment differences, or significant governance ambiguity.

### `critical`

Reserved for the most serious future classes of issue where delay or inconsistency could create severe regulatory, legal, or operational harm.

## Current implemented scoring behavior

The current implementation scores:

- timeline conflicts as `high`
- threshold conflicts as `high`
- stale references as `medium`
- other current defaults conservatively as `medium`

This reflects the seeded v1 workflow and can expand later.

## Severity factors

Severity should be influenced by factors such as:

- contradiction type
- whether timelines or thresholds diverge materially
- whether the source is external guidance or an internal governing standard
- whether a downstream artifact weakens a controlling requirement
- whether customer-impacting behavior is affected
- whether the discrepancy affects approvals, escalations, or mandatory handling
- whether the issue reflects stale governance or direct contradiction

## Examples

### Low severity example

Terminology drift with no proven downstream process impact yet.

### Medium severity example

A procedure references an older version of a standard, but the practical effect is not yet shown to change customer handling.

### High severity example

Two aligned documents specify different customer acknowledgment timelines.

### Critical severity example

Reserved for future use, such as severe governance contradictions affecting mandatory regulated handling with high impact.

## Relationship to review routing

Severity influences but does not fully determine review routing.

A finding may be reviewable because of:

- high severity
- degraded mode
- low confidence
- provider failure
- schema failure
- manual sampling policy

Severity should therefore be read together with review reason codes and workflow state.

## Relationship to confidence

Confidence measures how strongly the system believes the detected issue is valid.

Severity measures how important the issue would be if valid.

These are distinct dimensions and should remain distinct.

## Design principles

### Conservative by default

Where richer scoring logic is not yet implemented, the system should prefer conservative, review-friendly behavior over exaggerated claims.

### Explainable

Severity should be understandable from the evidence and discrepancy type.

### Expandable

The model should allow future rules for jurisdiction, domain area, customer impact, and control criticality.

## v1 limits

The current severity model is intentionally simple. It does not yet include:

- domain-specific weighting tables
- jurisdiction-sensitive escalation logic
- customer-harm scoring
- cumulative severity across related findings
- policy-owner criticality maps

## Summary

The severity model helps prioritize findings based on operational significance. In v1 it intentionally favors explainable, type-driven scoring over complex but opaque weighting.
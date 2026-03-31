# Review Workflow

## Purpose

The review workflow turns machine-detected discrepancies into controlled human decisions. Its purpose is not only to surface findings, but to ensure that reviewable findings are assigned, acted on, and recorded with traceable state changes.

## Why review exists

Even when rules are deterministic, policy contradictions still require human judgment.

Examples include:

- deciding whether a mismatch is a real governance problem
- determining whether a downstream artifact is intentionally stricter
- deciding whether a stale reference is still acceptable temporarily
- escalating material findings to the right owner

The review layer ensures findings are operationally processed rather than merely detected.

## Core objects

### `ReviewTask`

Represents a queued unit of human review tied to a single finding.

Important fields include:

- linked conflict flag
- queue name
- assigned reviewer
- task status
- reason code
- SLA due time

### `ReviewerAction`

Represents a concrete reviewer decision or intervention.

Important fields include:

- review task
- reviewer
- action type
- old value
- new value
- comment
- override reason code

### `AuditEvent`

Records important workflow transitions and reviewer actions for traceability.

## Review-task lifecycle

The primary task statuses are:

- `unassigned`
- `assigned`
- `in_review`
- `approved`
- `overridden`
- `dismissed`
- `escalated`
- `closed`

This lifecycle keeps queue operations explicit and inspectable.

## Common workflow path

A typical review flow is:

1. comparison creates a finding
2. finding requires review
3. review task is created in the configured queue
4. task is assigned to a reviewer
5. reviewer inspects citations and memo
6. reviewer approves, overrides, dismisses, or escalates
7. linked finding status is updated
8. reviewer action is stored
9. audit event is written

## Creation of review tasks

Review tasks are created automatically for findings that require review.

Inputs that influence task creation include:

- conflict severity
- degraded mode
- failure conditions
- configured queue name
- configured SLA hours

This ensures that high-value discrepancies become operational work items immediately.

## Action semantics

### Assign

Assign binds the task to a specific reviewer and moves it from unassigned toward active review.

Expected effects:

- update task assignee
- update task status
- write reviewer action where appropriate
- write audit event

### Approve

Approve confirms the finding as valid.

Expected effects:

- update review-task status to approved
- update linked finding status appropriately
- record reviewer action
- write audit event

### Override

Override changes or replaces the machine interpretation.

Expected effects:

- preserve evidence that the reviewer changed the original machine conclusion
- record old and new values where relevant
- record override reason
- write audit event

### Dismiss

Dismiss marks the finding as not requiring further action.

Expected effects:

- update task status
- update linked finding status to dismissed where appropriate
- record reviewer comment
- write audit event

### Escalate

Escalate pushes the issue upward because the finding requires broader governance attention or cross-team action.

Expected effects:

- update task status to escalated
- update linked finding state
- record escalation note
- write audit event

## Link to findings

The review layer is tightly coupled to findings but remains a separate workflow object.

This separation is important because:

- not every finding must remain in the same workflow state as its review task
- human action history deserves its own record
- reporting can distinguish detection volume from review throughput

## SLA model

Every review task includes an SLA due time.

This supports:

- queue prioritization
- operational monitoring
- overdue review metrics
- review-ops reporting

The current configuration uses `DEFAULT_SLA_HOURS` for seeded and local workflows.

## Queue model

The current queue model is intentionally simple.

A task is routed into a named queue such as `policy-review`. This is enough for v1 to support:

- seeded demonstrations
- review-ops metrics
- future expansion to role-based or domain-specific queues

## Auditability

Every meaningful review transition should emit an `AuditEvent`.

This allows operators to reconstruct:

- who acted
- what they did
- when it happened
- which entity changed
- which correlation id linked the workflow

This matters because audit systems are judged not only by detection quality, but by how clearly they preserve decision history.

## UI usage

The review queue page exposes the review workflow through:

- task rows
- current status
- reason code
- SLA visibility
- action buttons for assign, approve, dismiss, and escalate

This allows the seeded workflow to demonstrate a full path from machine detection to human action.

## Design principles

### Human review is first-class

Review is not an afterthought appended to detection. It is part of the core workflow.

### Reviewer intervention is explicit

Changes are represented as reviewer actions, not hidden side effects.

### Evidence stays attached

Review decisions remain grounded in citations and memos.

### Audit history matters

Every meaningful action should be reconstructable later.

## v1 limitations

Not emphasized in v1:

- multi-step approvals
- role-based entitlements
- parallel review branches
- escalation trees
- external ticketing-system integration
- reviewer productivity analytics beyond simple metrics

## Summary

The review workflow converts findings into accountable human decisions. It preserves queue state, reviewer actions, linked finding transitions, SLA timing, and audit history so that contradiction detection leads to governed outcomes.
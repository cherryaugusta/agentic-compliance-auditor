# Failure Modes

## Purpose

This document describes how the system behaves when expected components, data, or assistive capabilities are unavailable or degraded. The goal is not to promise perfect resilience. The goal is to preserve truthful behavior, explicit status, and replayable workflows.

## Design principle

Agentic Compliance Auditor is designed so that deterministic rules remain authoritative. Because of that, assistive AI failures should reduce convenience or explanation quality, but should not silently invalidate the entire workflow.

When something fails, the system should prefer:

- explicit degraded state
- preserved evidence
- replayable workflow objects
- audit-visible transitions
- continued deterministic operation where possible

## Failure-mode categories

### Dependency failures

Failures involving PostgreSQL, Redis, or background worker availability.

### Assistive-model failures

Failures involving prompt configuration, schema validation, provider availability, timeout, or provider-level errors.

### Data-shape failures

Failures involving malformed source text, incomplete extraction, or unexpected statement structure.

### Workflow-state failures

Failures where a task or run reaches a terminal or inconsistent state that requires replay, retry, or manual intervention.

## Health endpoints

The health layer provides three levels of operational visibility:

- `/health/live`
- `/health/ready`
- `/health/deps`

These support fast diagnosis of process state and dependency reachability.

## Representative failure modes

### Database unavailable

If PostgreSQL is unavailable, the backend cannot persist or query core workflow objects.

Expected outcome:

- readiness and dependency health should fail
- no misleading success response should be emitted for dependent operations

### Redis unavailable

If Redis is unavailable, asynchronous dispatch and dependency checks may fail.

Expected outcome:

- dependency health should fail
- queued execution may be unavailable
- local workflow may require direct or eager execution paths in tests

### Celery worker not running

If the worker is not active, tasks may be queued but not processed.

Expected outcome:

- document creation may succeed
- parse or comparison completion may not happen until the worker starts
- this should be treated as an operational state, not a silent success of downstream stages

### Prompt version missing or inactive

If the contradiction-analysis prompt is missing or inactive, the comparison engine should still run deterministic rules.

Expected outcome:

- findings may still be created
- citations may still be created
- review tasks may still be created
- the comparison run should be marked `degraded`
- a fallback model execution log should be written

This is one of the most important designed failure modes in the system.

### Provider timeout or provider error

If an assistive provider fails, the system should prefer deterministic fallback behavior rather than pretending the run was fully model-assisted.

Expected outcome:

- execution log records timeout or provider failure
- run may be degraded
- deterministic rules remain active where implemented

### Schema validation failure

If structured model output cannot be trusted, the workflow should not silently accept it.

Expected outcome:

- schema failure is logged
- deterministic path remains preferred where available
- reviewer-facing artifacts should remain grounded in citations

### Stale reference not modeled yet

Sometimes the workflow may surface evidence of drift but not yet encode the richer reasoning needed to classify it perfectly.

Expected outcome:

- conservative handling
- eval coverage expansion over time
- no false claim of exhaustive policy interpretation

## Degraded mode

Degraded mode is a deliberate system behavior, not an accident.

It exists to preserve useful workflow execution when assistive AI capabilities are unavailable or intentionally disabled.

### What degraded mode preserves

- deterministic rule execution
- finding creation for rule-detectable discrepancies
- citation creation
- review-task routing
- observability logs
- auditable run records

### What degraded mode does not pretend

- full assistive explanation quality
- comprehensive semantic reasoning
- production-grade automation accuracy

## Replay and retry

The comparison workflow includes replay and retry actions.

These are important because they allow operators to:

- rerun a comparison after a transient problem
- preserve the original source, targets, and configuration
- inspect operational differences between runs

Replayability is a core mitigation strategy for workflow-state failures.

## Audit visibility

Every meaningful failure or degraded transition should remain inspectable through run status, model logs, task state, and audit events.

This matters because silent fallback degrades trust. Explicit fallback preserves trust.

## Local development considerations

The local Windows environment has a few specific operational lessons:

- PostgreSQL host port uses `55432`, not `5432`, in local Docker mapping
- Celery should run with `-P solo`
- frontend tests are more reliable through `npx vitest run`
- psql pager mode should be avoided with `-P pager=off` when needed

These are not theoretical notes. They are part of the known working operational profile.

## v1 limits of resilience

The current system does not attempt to provide:

- distributed failover
- exactly-once job semantics
- automatic incident remediation
- sophisticated dead-letter processing
- tenant-isolated recovery controls

The emphasis is truthful degraded behavior and replayable local workflow execution.

## Summary

Failure handling in Agentic Compliance Auditor is built around explicit degraded state, preserved auditability, and deterministic continuity. The system is designed to fail visibly and recover inspectably rather than hide uncertainty behind false success.
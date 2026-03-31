# System Overview

## Purpose

Agentic Compliance Auditor is a rules-first, AI-assisted policy-control audit workflow. Its purpose is to detect alignment problems across internal policies, procedures, control libraries, and external guidance while preserving evidence, review traceability, and audit lineage.

The system is designed to answer a practical question: when related policy artifacts evolve over time, do they still say compatible things, and if not, what evidence supports the discrepancy?

## Architectural style

The application is implemented as a modular monolith.

This choice keeps deployment and local development simple while preserving clear separation between domain boundaries. The backend is a single Django codebase with domain-oriented apps. The frontend is a single React application organized by feature area. Shared persistence, audit logging, and seeded workflows remain easy to reason about without introducing distributed-system overhead.

## Runtime shape

The intended local runtime model is:

- Django backend runs locally
- React frontend runs locally
- PostgreSQL runs in Docker Compose
- Redis runs in Docker Compose
- Celery worker runs locally with `-P solo` on Windows
- Django Channels is configured for HTTP and future WebSocket expansion

For v1, Docker Compose is intentionally limited to infrastructure services only. Application code runs directly on the host machine.

## Core backend domains

The backend is organized into domain apps with explicit responsibility boundaries.

### `core`

Shared model and middleware utilities, including timestamped base models and correlation-id handling.

### `accounts`

User and authentication-adjacent behavior for local workflow participation.

### `documents`

Policy-document ingestion, metadata storage, checksums, sections access, statement access, and document-level workflow entry points.

### `lineage`

Parent-child and cross-document relationships such as supersedes, derived-from, references, implements, and aligned-to.

### `sectioning`

Reserved boundary for document sectioning logic and future parser specialization.

### `statements`

Normalized control statements extracted from sections. This is the core comparison substrate.

### `comparisons`

Comparison-run creation, execution, replay, retry, and status tracking.

### `findings`

Typed discrepancies, evidence citations, and finding memos produced from comparisons.

### `reviews`

Human review queue, assignments, reviewer actions, overrides, dismissals, escalations, and linked state transitions.

### `audits`

Immutable-style audit-event records for operational and reviewer traceability.

### `evals`

Evaluation cases, evaluation runs, persisted metrics, and latest-report exposure.

### `observability`

Execution telemetry, prompt versions, model logs, and metrics endpoints.

### `health`

Liveness, readiness, and dependency health endpoints.

## Frontend structure

The frontend is a React, TypeScript, and Vite application organized by user workflow rather than technical layer.

Primary feature areas include:

- documents
- lineage
- comparisons
- findings
- review queue
- metrics
- evals
- admin tools

This structure mirrors the operator journey: inspect source material, launch comparisons, review findings, process tasks, and inspect metrics.

## Primary data flow

The system follows a deterministic audit flow:

1. A policy document is created or ingested.
2. A checksum is computed for deduplication.
3. Content is split into sections.
4. Sections are transformed into normalized control statements.
5. A comparison run is launched against target documents.
6. Deterministic rules identify contradictions, timeline mismatches, threshold mismatches, stale references, and related discrepancy types.
7. Findings are created with source and target citations.
8. Review tasks are created for findings requiring human review.
9. Audit events record lifecycle actions.
10. Metrics and eval outputs expose system behavior.

## Persistence model

### PostgreSQL

PostgreSQL is the primary system of record. It stores:

- policy documents
- sections
- control statements
- lineage links
- comparison runs
- findings
- citations
- memos
- review tasks
- reviewer actions
- audit events
- eval cases and eval runs
- observability records

### pgvector

`pgvector` is enabled for limited statement-similarity support on `ControlStatement.embedding`.

It is not the primary contradiction engine and is not the identity mechanism for products or policies. Deterministic comparison logic remains authoritative.

### Redis

Redis supports Celery brokering and result-backend use, and provides channel-layer support for future real-time features.

## Asynchronous execution model

Two main workflow stages are asynchronous:

- parse-and-extract document processing
- comparison-run execution

These are executed through Celery tasks. On Windows, the worker runs with `-P solo` to preserve stable local development behavior.

## API shape

The API is deliberately conventional.

Patterns used include:

- `ModelSerializer`
- `ModelViewSet`
- `ReadOnlyModelViewSet`
- `APIView`
- `DefaultRouter`

This keeps the backend easy to inspect, test, and extend. Workflow actions such as assign, approve, replay, retry, and export are modeled as explicit REST actions.

## Authority model

The system is rules-first.

That means:

- deterministic rules are the source of truth for core contradiction detection
- AI is used in an assistive role, not an authoritative one
- findings remain tied to concrete citations
- degraded mode is allowed and observable
- human review remains part of the workflow where needed

## Traceability model

Traceability is a first-class design constraint. The system preserves:

- document versions
- document lineage relationships
- source and target citations
- review-task state transitions
- reviewer actions
- comparison-run identifiers
- audit events
- eval results
- degraded-mode indicators

This allows every surfaced discrepancy to be inspected from source material to reviewer decision.

## Local workflow summary

A typical local demo session looks like this:

1. Start PostgreSQL and Redis through Docker Compose.
2. Run Django migrations.
3. Seed deterministic demo data.
4. Run the backend server.
5. Run the Celery worker.
6. Run the frontend.
7. Inspect seeded workflows through the UI and API.

## Boundaries for v1

Version 1 intentionally limits scope.

Included:

- document ingestion and versioning
- section parsing
- control statement extraction
- version and source-pair comparison
- typed findings with citations
- review-task routing
- audit logging
- eval and metrics exposure
- seeded workflow rendering in the UI

Not emphasized in v1:

- advanced semantic retrieval
- production-grade OCR pipelines
- enterprise identity and authorization policies
- multi-tenant isolation
- large-scale distributed execution
- legal or regulatory interpretation automation

## Summary

Agentic Compliance Auditor is a modular, inspectable, rules-first audit system built to make policy drift visible. It favors explicit domain boundaries, deterministic workflow behavior, reproducible seeded scenarios, and audit-ready traceability over opaque automation.
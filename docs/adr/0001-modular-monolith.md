# ADR 0001: Modular Monolith

## Status

Accepted

## Context

The system needs to support document ingestion, lineage management, statement extraction, comparison runs, findings, reviews, audit logging, evaluation, and observability. These are distinct business concerns, but the initial delivery target is a local, inspectable v1 with seeded workflows, reproducible tests, and simple deployment.

A distributed multi-service architecture would increase operational complexity before the workflow itself is stable.

## Decision

The system will be implemented as a modular monolith.

The backend will use a single Django project with domain-oriented apps. The frontend will use a single React application with feature-oriented organization. Shared persistence will remain in one PostgreSQL database.

## Consequences

### Positive

- simpler local development
- simpler debugging
- single deployment unit for application code
- easy transaction boundaries
- straightforward seeded demo workflows
- lower operational overhead
- clear domain separation without distributed-system complexity

### Negative

- all backend domains deploy together
- scaling boundaries are logical rather than physically isolated
- strong internal discipline is required to preserve module boundaries
- future extraction of services would require deliberate refactoring

## Notes

This decision favors workflow clarity, local reproducibility, and delivery speed for v1. It does not prevent future decomposition if growth or operational pressure later justifies it.
# ADR 0002: PostgreSQL as Primary Store

## Status

Accepted

## Context

The system must persist structured domain records with strong relational links across documents, sections, statements, lineage, comparison runs, findings, review tasks, audit events, eval runs, and observability logs.

The data model is highly relational and requires durable transactional integrity.

## Decision

PostgreSQL will be the primary system of record.

The application will use Django ORM models backed by PostgreSQL. `pgvector` will be enabled in PostgreSQL only for limited statement-similarity support on `ControlStatement.embedding`.

## Consequences

### Positive

- strong relational modeling
- durable transactional behavior
- mature Django integration
- good support for queryable audit workflows
- extension support through `pgvector`
- clean fit for seeded local infrastructure in Docker Compose

### Negative

- document-heavy workloads still require application-level parsing and transformation
- vector support remains limited compared with specialized retrieval platforms
- larger-scale analytical workloads may later require additional read models or warehouse patterns

## Notes

This decision keeps the core workflow grounded in explicit relational data rather than in opaque document stores. It also aligns with the rules-first design of the project.
# ADR 0004: Rules-First, AI-Assisted Workflow

## Status

Accepted

## Context

The system needs to detect contradictions and drift in a way that remains testable, reproducible, and explainable. AI can help with extraction, summarization, and observability, but relying on probabilistic outputs as the sole source of truth would make the workflow harder to audit and harder to trust.

## Decision

The system will be rules-first and AI-assisted.

Deterministic rules will remain authoritative for core comparison behavior. AI will be used in assistive roles such as extraction support, memo generation, and execution observability. The default provider posture for local development will remain mock-backed.

## Consequences

### Positive

- core workflow remains reproducible
- tests can verify contradiction behavior deterministically
- degraded mode becomes practical and honest
- findings remain easier to explain and defend
- AI can still add value without being the control authority

### Negative

- the workflow may detect fewer nuanced contradictions than a more model-heavy system
- some language variation may require future rule expansion
- assistive outputs still require prompt and schema governance

## Notes

This decision is foundational to the product identity. The system is not a chatbot and not a model-first interpretation engine. It is a policy-control audit workflow with AI in a bounded support role.
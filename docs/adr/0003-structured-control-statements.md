# ADR 0003: Structured Control Statements as Comparison Substrate

## Status

Accepted

## Context

Direct comparison of full documents is noisy and hard to audit. Policy documents contain formatting differences, narrative context, and procedural wording that may obscure the actual control obligations being compared.

The system needs a narrower, inspectable representation for contradiction detection.

## Decision

The system will extract normalized control statements from document sections and use those statements as the primary comparison substrate.

Each control statement will preserve raw text while also storing structured and normalized fields such as statement type, normalized text, deadline text, threshold text, and optional embeddings.

## Consequences

### Positive

- comparison logic becomes more focused
- findings can point to structured evidence
- rules can operate over normalized fields
- extraction and comparison are easier to test independently
- future semantic enhancements have a stable substrate

### Negative

- extraction quality constrains downstream comparison quality
- some nuance in full-document context may be compressed
- v1 statement extraction remains intentionally narrow

## Notes

This decision is central to the workflow. It separates document ingestion from contradiction analysis and makes the audit surface more explicit and reproducible.
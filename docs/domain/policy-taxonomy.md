# Policy Taxonomy

## Purpose

This document defines the main taxonomy used by the system for classifying policy artifacts and related domain dimensions. These values shape ingestion, filtering, seeded data, and workflow interpretation.

## Document types

### `internal_policy`

Used for internal policy statements that define governing requirements, controls, or principles for the organization.

Example:
Complaints Escalation Policy v3

### `procedure`

Used for operational procedures that describe how teams carry out policy or control obligations.

Example:
Complaints Procedure v2

### `control_library`

Used for structured control definitions or standards that internal artifacts are expected to align with.

Example:
Complaints Control Standard v5

### `guidance`

Used for guidance material, often external, that informs or influences internal policy decisions.

Example:
Vulnerable Customer Guidance 2026

### `standard`

Reserved for standard-like policy artifacts not otherwise captured as control libraries.

### `board_paper`

Reserved for governance or decision artifacts originating from board-level processes.

## Domain areas

### `complaints`

Used for complaints handling, escalation, and redress-related workflows.

### `consumer_support`

Used for customer-support and service-handling obligations.

### `communications`

Used for communication requirements, notices, wording, and customer-facing content rules.

### `escalations`

Used for escalation pathways and escalation handling rules.

### `governance`

Used for policy governance, approval, oversight, and administrative control structures.

### `vulnerable_customers`

Used for obligations specific to vulnerable-customer treatment and escalation.

### `other`

Used where a document does not fit the current narrower taxonomy.

## Document status values

### `draft`

Document exists but is not yet active for intended operational use.

### `active`

Document is currently in force or intended for use.

### `retired`

Document is no longer active but remains historically important.

### `archived`

Document is retained for record purposes and is not part of the active control estate.

## Lineage relationship taxonomy

### `supersedes`

A newer document replaces an older version.

### `derived_from`

A document is materially based on another.

### `references`

A document cites or points to another document.

### `implements`

A document operationalizes a requirement from another artifact.

### `aligned_to`

A document is expected to remain substantively aligned with another document.

## Control statement types

### `obligation`

A required action or expected compliance behavior.

### `control`

A control-oriented statement that does not fit more specific categories.

### `procedure_step`

An operational step within a procedure.

### `timeline`

A time-bound requirement.

### `threshold`

A numeric or monetary boundary.

### `exception_rule`

A statement defining exception handling.

### `approval_rule`

A statement defining approval or sign-off behavior.

## Finding conflict taxonomy summary

The system supports the following discrepancy families:

- direct contradiction
- weaker internal control
- missing control
- stale reference
- threshold conflict
- timeline conflict
- approval conflict
- terminology drift
- coverage gap

Detailed definitions and examples are documented separately in `contradiction-types.md`.

## Review-task status taxonomy

Review tasks move through the following statuses:

- unassigned
- assigned
- in review
- approved
- overridden
- dismissed
- escalated
- closed

## Review reason codes

Current review reason-code categories include:

- low confidence
- high severity
- schema failure
- stale reference
- missing control
- manual sampling
- provider failure

## Summary

This taxonomy keeps the workflow consistent across ingestion, comparison, findings, review operations, and seeded demo scenarios. It is intentionally compact for v1, with room to expand as the domain model grows.
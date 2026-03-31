# Seeded Policy Packs

## Purpose

This document describes the deterministic seeded content used to demonstrate the application end to end. The seed set is designed to populate the UI, API, review workflow, lineage view, and eval reporting with coherent sample records.

## Seed objectives

The seeded data is intended to:

- make the system immediately demoable after setup
- provide a known contradiction scenario
- populate all major workflow views
- create reviewable findings with citations and memo output
- create audit events and eval metrics
- support reproducible screenshots

## Seeded users

The current seed creates three users:

- `admin`
- `reviewer1`
- `reviewer2`

These users support local admin access and reviewer workflow demonstration.

## Seeded document inventory

The seed creates twelve documents.

### 1. Complaints Escalation Policy v3

- type: `internal_policy`
- source: Internal Policy Office
- domain: complaints
- owner team: Compliance
- effective date: 2026-01-15
- purpose: source side of the canonical timeline contradiction

### 2. Complaints Control Standard v5

- type: `control_library`
- source: Internal Standards Board
- domain: complaints
- owner team: Risk
- effective date: 2026-02-01
- purpose: target side of the canonical timeline contradiction

### 3. Complaints Procedure v2

- type: `procedure`
- source: Operations
- domain: complaints
- owner team: Operations
- effective date: 2025-10-01
- purpose: example procedure artifact with reference-drift potential

### 4. Vulnerable Customer Guidance 2026

- type: `guidance`
- source: External Regulator
- domain: vulnerable customers
- owner team: Compliance
- effective date: 2026-02-15
- purpose: example external guidance artifact

### 5 through 12. Seeded Demo Policy 5 to Seeded Demo Policy 12

- type: `internal_policy`
- source: Seed Generator
- domain: other
- owner team: Governance
- purpose: populate library views and provide additional seeded coverage

## Canonical contradiction scenario

The seed’s main contradiction scenario compares:

- `Complaints Escalation Policy v3`
- `Complaints Control Standard v5`

The source states:

- escalated complaints must be acknowledged within 10 business days

The target states:

- escalated complaints must be acknowledged within 5 business days

This produces a `timeline_conflict` finding.

## Seeded lineage

The seed also creates a lineage link between the main source and target documents using:

- relationship type: `aligned_to`

This ensures the lineage view has meaningful data and gives structural context to the contradiction.

## Seeded prompt versions

The seed creates prompt-version records for:

- sectioning
- statement extraction
- contradiction analysis
- memo generation

These support observability views and degraded-mode demonstrations.

## Derived seeded workflow objects

Running the seed creates not only documents but also downstream workflow records, including:

- parsed sections
- extracted control statements
- a comparison run
- a finding
- evidence citations
- a finding memo
- a review task
- audit events
- an eval run

## Expected seeded summary

The known seeded baseline currently reaches:

- users: 3
- documents: 12
- sections: 12
- statements: 12
- comparison runs: 1
- findings: 1
- citations: 2
- memos: 1
- review tasks: 1
- audit events: 13
- eval runs: 1

## Where the seed comes from

The seed logic is implemented in:

- `infra/scripts/seed_demo_data.py`

It creates or updates known records so the local environment can be re-seeded predictably.

## Demo usage recommendations

After seeding:

1. open the document library
2. inspect the seeded complaints policy and control standard
3. open the lineage view
4. inspect the findings dashboard
5. open the finding detail
6. inspect the review queue
7. inspect metrics and evals
8. optionally demonstrate degraded mode

## Summary

The seeded policy packs provide a coherent, deterministic data foundation for demonstrating the application’s full workflow from source documents to findings, review tasks, audit events, and metrics.
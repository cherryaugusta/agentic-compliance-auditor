# Synthetic Data Specification

## Purpose

This document defines the shape and intent of the synthetic data used for seeded workflows and evaluation cases. Synthetic data exists to make system behavior reproducible, inspectable, and safe to share.

## Two synthetic-data layers

The repository uses two related but distinct synthetic-data layers:

### Seeded demo data

Used to populate the live application database for UI and API workflows.

Location highlights:

- `demo_data/`
- `infra/scripts/seed_demo_data.py`

### Eval datasets

Used for repeatable regression-oriented scenario testing.

Location highlights:

- `evals/datasets/`
- `infra/scripts/generate_eval_cases.py`
- `infra/scripts/run_eval_suite.py`

## Seeded demo data goals

Seeded demo data should:

- produce a working end-to-end local workflow
- create visible documents, sections, statements, findings, citations, memo output, review tasks, audit events, and eval results
- support screenshot capture
- remain deterministic and easy to explain

## Eval dataset goals

Eval datasets should:

- test contradiction behavior against known scenarios
- protect against regression
- include both positive and negative cases
- exercise degraded and adversarial paths
- remain machine-readable and simple to regenerate

## Eval case structure

An eval JSON file should contain fields such as:

- `case_id`
- `scenario_type`
- `documents`
- `expected_statements`
- `expected_conflict_type`
- `expected_severity`
- `expected_requires_review`
- `expected_citation_targets`

## Document payload shape

A synthetic document payload typically includes:

- `document_type`
- `title`
- `version_label`
- `effective_date`
- `text`

This is enough for seeded extraction and comparison logic to run.

## Expected-output shape

A synthetic eval case can define expectations such as:

- expected statement type
- expected normalized text pattern
- expected contradiction type
- expected severity
- expected review requirement
- expected citation target titles

This helps the eval suite test both detection and workflow artifacts.

## Current eval scenario families

The current generator creates cases for:

- contradiction cases
- drift cases
- stale reference cases
- no-conflict cases
- adversarial cases
- fallback cases

## Seeded database shape

The seeded local workflow currently targets a compact but complete set of records, including:

- users
- policy documents
- sections
- control statements
- comparison runs
- findings
- citations
- memos
- review tasks
- audit events
- eval runs
- prompt versions

## Seed design principles

### Deterministic

A seed run should produce stable, explainable results.

### Safe

No real confidential policy material should be required.

### Representative

The dataset should resemble plausible policy-control scenarios without claiming production completeness.

### Traceable

Each seeded discrepancy should be inspectable through source records, citations, memo, review task, and audit history.

## Example seeded contradiction

The canonical seeded contradiction is a timeline mismatch between:

- `Complaints Escalation Policy v3`
- `Complaints Control Standard v5`

This creates a concrete finding with source and target citations and a review task.

## Naming conventions

Synthetic files and payloads should use names that make scenario intent obvious.

Examples:

- `eval-direct_contradiction-001`
- `Seeded Demo Policy 5`
- `Complaints Procedure v2`

## What synthetic data is not

Synthetic data in this repository is not:

- a legal corpus
- a real regulatory rulebook
- a complete enterprise policy estate
- a benchmark proving production performance

Its purpose is reproducible workflow demonstration and regression coverage.

## Summary

The synthetic data specification ensures that seeded demos and eval runs remain deterministic, safe, and aligned with the workflow’s real design goals: inspectable contradiction detection, evidence preservation, review routing, and regression awareness.
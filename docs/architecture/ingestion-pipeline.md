# Ingestion Pipeline

## Purpose

The ingestion pipeline turns raw policy material into structured, comparable records. It exists to move from document-level text to section-level and statement-level artifacts that can be inspected, compared, cited, and routed into review.

## Pipeline stages

The v1 ingestion flow is:

1. document creation
2. checksum calculation and deduplication
3. asynchronous parse-and-extract dispatch
4. section creation
5. control-statement extraction
6. audit-event emission
7. downstream comparison readiness

## Stage 1: document creation

A policy document enters the system through the documents API.

Stored document attributes include:

- document type
- title
- source name
- jurisdiction
- domain area
- owner team
- version label
- effective date
- superseded document reference
- external-source flag
- status
- storage path
- checksum
- raw content text

This stage is intentionally simple. The document itself is the persistent source object for later workflow stages.

## Stage 2: checksum calculation and deduplication

On create, the system computes a SHA-256 checksum from `content_text`.

This supports deduplication at ingestion time. If an equivalent payload already exists, the workflow can avoid re-materializing duplicate source records unnecessarily.

The checksum is not a business meaning layer. It is a content-identity mechanism for ingestion hygiene.

## Stage 3: parse-and-extract dispatch

After persistence, the backend enqueues asynchronous processing through:

- `parse_and_extract_document.delay(document_id)`

This stage separates API responsiveness from extraction work. It also keeps the workflow extensible if parsing or extraction becomes more expensive later.

## Stage 4: section creation

The current v1 parser is deterministic and intentionally simple.

It splits content by blank-line boundaries and creates one or more `DocumentSection` rows with:

- section index
- heading
- raw text
- character offsets
- parser confidence
- optional page number

The current seeded workflow typically produces one section per seeded document, but the model supports multi-section documents.

## Stage 5: control-statement extraction

Each section is transformed into one `ControlStatement` in the current baseline flow.

Stored statement fields include:

- statement type
- raw text
- normalized text
- subject entity
- action verb
- condition text
- deadline text
- threshold text
- owner role
- schema-valid flag
- extraction confidence
- extraction version
- optional embedding

The current extraction logic identifies structured signals such as:

- timelines
- thresholds
- approval language
- obligations
- general controls

This extraction is deliberately narrow and deterministic for v1.

## Statement normalization

Normalization reduces superficial wording variability and produces a more stable comparison substrate.

Examples of normalized attributes include:

- lower-cased normalized text
- isolated timeline expressions
- isolated threshold expressions
- classified statement type

The point is not to produce a perfect semantic model. The point is to create a structured surface that deterministic comparison rules can inspect reliably.

## Audit behavior

When parse-and-extract completes, the system writes an `AuditEvent` that records the completion of document processing.

This provides an auditable transition from document creation to extraction completion.

## Output artifacts

By the end of ingestion, one source document has produced:

- a persistent `PolicyDocument`
- one or more `DocumentSection` rows
- one or more `ControlStatement` rows
- at least one audit event describing completion

These outputs make the document comparable and reviewable.

## Failure behavior

If parsing or extraction fails in a future expanded implementation, the ingestion boundary should preserve the original document row and expose enough state for retry or inspection.

The current baseline flow is intentionally compact, but the model and audit boundaries already support richer retry behavior later.

## Why the pipeline is structured this way

This design preserves several useful properties:

- the original document remains the source of truth
- sectioning is inspectable
- extraction is inspectable
- comparison does not depend on raw text alone
- audit logs can reflect stage completion
- asynchronous processing does not block document creation

## v1 limitations

The current ingestion pipeline does not attempt to solve every document-processing problem.

Not in scope for v1:

- OCR-heavy ingestion
- advanced PDF layout reconstruction
- cross-page table recovery
- multilingual extraction
- high-recall semantic segmentation
- production-grade parser orchestration

The current focus is clear seeded workflows and deterministic inspection.

## Summary

The ingestion pipeline converts source policy material into structured sections and normalized control statements. It keeps raw source content, produces auditable intermediate artifacts, and prepares documents for deterministic comparison and review.
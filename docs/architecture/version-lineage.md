# Version Lineage

## Purpose

Version lineage captures how documents relate to one another across time and across policy layers. It allows the system to distinguish not only what a document says, but also where it sits in a broader governance chain.

This is essential because policy-control misalignment often comes from relationship drift, not only text drift.

## Core idea

Documents are not isolated records. They may:

- supersede earlier versions
- derive from parent material
- reference external guidance
- implement a control standard
- align to another policy artifact

The lineage model makes those relationships explicit and queryable.

## Data model

Lineage is represented by `DocumentLineage`.

Each lineage link includes:

- `parent_document`
- `child_document`
- `relationship_type`

A uniqueness constraint prevents duplicate links for the same parent, child, and relationship combination.

## Relationship types

### `supersedes`

Used when a newer document replaces an older version in authority or intended use.

Example:
Policy v4 supersedes Policy v3.

### `derived_from`

Used when one document is materially based on another but is not necessarily its formal replacement.

Example:
An operational procedure derived from a control standard.

### `references`

Used when one document cites or depends on another without implementing or replacing it.

Example:
A procedure referencing an older control library version.

### `implements`

Used when a downstream artifact operationalizes a higher-level requirement.

Example:
A procedure implementing an internal policy requirement.

### `aligned_to`

Used when two documents should remain substantively consistent even if they belong to different governance layers.

Example:
An internal policy aligned to an internal control standard.

## Why lineage matters operationally

Lineage supports several critical questions:

- Which document version should be considered current?
- Which procedure is tied to which policy version?
- Which documents are expected to align?
- Which external guidance source influenced an internal artifact?
- Which stale references indicate governance drift?

Without lineage, contradiction detection becomes flatter and less credible because it cannot distinguish expected relationships from incidental wording overlap.

## Version chains

The lineage API exposes grouped relationship chains through `version_chains`.

These chains present parent-child relationships by document title and associated relationship labels so that operators can inspect how a document family evolved.

This is useful for:

- UI lineage views
- seeded-demo storytelling
- future impact analysis
- tracing supersession history

## Effective-date interaction

Version lineage should be interpreted together with effective dates.

Typical rules include:

- newer effective dates do not automatically mean a document supersedes another unless the relationship is modeled or inferred explicitly
- references to older artifacts may still be valid if the older artifact remains active
- a stale reference becomes higher risk when a referenced artifact has a newer superseding version
- aligned documents should be checked for substantive consistency even when effective dates differ

## Example lineage scenarios

### Formal version progression

- Complaints Escalation Policy v2
- Complaints Escalation Policy v3

Relationship:
v3 supersedes v2

Interpretation:
v3 should usually be treated as the active successor and comparison workflows may prioritize it for version-diff analysis.

### Cross-layer alignment

- Complaints Escalation Policy v3
- Complaints Control Standard v5

Relationship:
policy aligned to control standard

Interpretation:
A timeline mismatch between these documents is meaningful because they are expected to remain aligned.

### Reference drift

- Complaints Procedure v2
- Control Library v2
- Control Library v5

Relationships:
procedure references control library v2  
control library v5 supersedes control library v2

Interpretation:
The procedure may now contain a stale reference and should be reviewed.

## UI and workflow usage

Lineage is surfaced in:

- document detail
- lineage page
- seeded workflows
- future replay and impact-analysis narratives

It is also part of human interpretation when reviewing findings.

## Design principles

### Lineage is explicit

Where possible, relationships should be modeled rather than assumed.

### Lineage is not identical to similarity

Two documents can be textually similar without having a governance relationship. Conversely, two related documents may use different language but still need alignment.

### Lineage improves finding credibility

A finding is more persuasive when it is attached to a known governance relationship rather than an arbitrary pairing.

## v1 limitations

The current lineage model is intentionally compact.

Not emphasized in v1:

- automatic lineage inference from large corpora
- graph-based impact propagation
- temporal reasoning over complex lifecycle intervals
- confidence-scored inferred relationships
- document-family clustering beyond simple relationship chains

## Summary

Version lineage makes document relationships explicit. It provides the structural context required to distinguish legitimate policy evolution from untracked drift and to keep contradiction findings grounded in governance reality.
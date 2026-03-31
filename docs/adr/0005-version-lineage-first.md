# ADR 0005: Version Lineage First

## Status

Accepted

## Context

Policy drift often emerges because related artifacts evolve asynchronously. A procedure may reference an older control standard. A policy may be updated while an aligned artifact remains unchanged. Without explicit lineage, contradiction findings lose governance context.

## Decision

The system will treat version lineage as a first-class concept.

Document relationships such as supersedes, derived-from, references, implements, and aligned-to will be explicitly modeled and exposed through the API and UI.

## Consequences

### Positive

- contradiction findings gain structural context
- stale-reference detection becomes more credible
- version chains become inspectable
- seeded demos can show governance evolution, not only text differences
- future impact analysis has a stronger foundation

### Negative

- lineage data must be maintained accurately
- some relationships may still require manual modeling
- future inference logic may be needed for broader corpora

## Notes

This decision supports the core idea that audit value comes not only from what a document says, but from how it relates to the rest of the policy estate over time.
# 0005: Two-pass Dataplex deploy with deterministic link IDs

**Status:** accepted

## Context
Entry links connect a BigQuery column to a glossary term, and a term to a term. A link can only be created when both ends exist.

## Decision
Pass 1 writes categories and terms. Pass 2 writes entry links. A link ID is a hash of its two ends.

## Consequences
- A first deploy into an empty glossary works without ordering tricks.
- Reruns are idempotent: the same input gives the same IDs.
- Links whose source was removed from a term can be found and pruned.

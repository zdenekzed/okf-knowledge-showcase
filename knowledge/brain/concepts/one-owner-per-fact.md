---
title: One owner per fact
type: concept
description: Every fact is edited in exactly one place. Every other appearance is compiled from it and never edited by hand.
tags:
- governance
---
## The rule
| Fact | Edited in | Compiled into |
| :-- | :-- | :-- |
| Metric meaning, formula, additivity, synonyms | Glossary term | Dataplex glossary, bundles |
| Table, columns, partitioning, lineage | Dataform `.sqlx` | Generated table record, graph |
| Column description | BigQuery (or Dataform where BigQuery has none) | Generated table record, Dataplex |
| Grain, column kinds, golden queries | Semantics overlay | Bundles |
| Which tables an agent may use | Data product contract | Bundles, agent allowlist |
| Rules for agents | Brain concept or bundle body | Bundles |

## Why
When the same definition lives in a wiki, a BI tool and a prompt, the three drift apart and nobody knows which one is right. With one owner, fixing the owner and rebuilding fixes every copy.

## Consequences
- Generated files carry a "do not edit" note, and CI fails if a committed generated file differs from a fresh generation.
- Curated knowledge about a generated table goes into a separate overlay file, so regeneration never overwrites it.
- Agents never get hand-written table lists in their prompts; they get compiled bundles. See [[knowledge-layers]].

---
title: Human Readable Name
type: term
description: One or two sentences, at most 300 characters (Dataplex limit).
category: metrics            # folder under glossary/terms/: metrics | entities
domain: sales
owner: team@example.com
aliases:                     # every word users say for this term
- synonym one
resource:                    # only if a column stores it: project.dataset.table.column
- project.dataset.table.column
related_terms:
- '[[other-term]]'
labels:                      # ^[a-z0-9_-]{1,63}$ for keys and values
  domain: sales
  additive: "true"
data_agent_hints:            # whatever an agent needs to write correct SQL
  aggregation: SUM
---
### 1. Business definition
What it means, in words a business user would use.

### 2. Calculation
Where it is stored or how it is computed.

### 3. Additivity
Over which dimensions it can be summed, and how to combine it otherwise.

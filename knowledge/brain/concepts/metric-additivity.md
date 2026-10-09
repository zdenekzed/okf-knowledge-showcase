---
title: Metric additivity
type: concept
description: Which numbers can be summed, which only within a slice, and which must be recomputed. The most common source of wrong answers from people and agents.
tags:
- metrics
- data-agent
---
## Three kinds of measures
- **Additive** ([[net-revenue]], [[orders]]): sum over any dimension.
- **Distinct counts** ([[active-customers]]): sum only where the dimension splits people into disjoint groups (cohorts); otherwise recount distinct ids.
- **Ratios** ([[average-order-value]], [[monthly-retention-rate]]): never sum, never average. Sum numerator and denominator over the selected rows, then divide.

## Where this is recorded
- In the glossary term: `labels.additive` and `data_agent_hints` (`cannot_average`, `cannot_sum_across`, `formula`).
- In the semantics overlay: `kind` and `how_to_count` per column.

The validator requires `how_to_count` for every ratio and distinct-count column, so an agent never meets a non-additive column without instructions.

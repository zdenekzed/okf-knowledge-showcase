---
title: Average Order Value
type: term
description: Net revenue divided by orders in the same slice. A ratio, so it is never stored per row and never averaged.
category: metrics
domain: sales
owner: analytics@folio.example
aliases:
- aov
- average basket
- basket size
related_terms:
- '[[net-revenue]]'
- '[[orders]]'
labels:
  domain: sales
  term_role: derived
  additive: "false"
data_agent_hints:
  formula: SUM(net_revenue_eur) / SUM(orders)
  cannot_average: true
  unit: EUR
---
### 1. Business definition
How much an order is worth on average in a given month, country or segment.

### 2. Calculation
`SUM(net_revenue_eur) / SUM(orders)` over the rows of [[r_sales_monthly]] that match the question. The term has no `resource` on purpose: no column stores it, it is always computed from two additive measures.

### 3. Additivity
Not additive. The AOV of Europe is **not** the average of the AOVs of its countries: sum [[net-revenue]] and [[orders]] first, then divide. See [[metric-additivity]].

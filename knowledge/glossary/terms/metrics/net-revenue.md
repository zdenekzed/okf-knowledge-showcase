---
title: Net Revenue
type: term
description: Revenue from paid orders in EUR after discounts, with refunded orders counted at zero. The money Folio keeps from its orders.
category: metrics
domain: sales
owner: analytics@folio.example
aliases:
- revenue
- net sales
- sales
resource:
- folio-analytics-demo.reporting.r_sales_monthly.net_revenue_eur
related_terms:
- '[[orders]]'
- '[[average-order-value]]'
labels:
  domain: sales
  term_role: standard
  additive: "true"
data_agent_hints:
  aggregation: SUM
  unit: EUR
  available_granularities:
  - month
---
### 1. Business definition
Net revenue is the value of all paid orders after discounts. A refunded order stays in the data but counts as zero; a cancelled order never enters it. When someone says "sales" or "revenue" without more context, this is the number they mean.

### 2. Calculation
`SUM(net_revenue_eur)` in [[r_sales_monthly]]. The order-level value comes from `amount_eur` in [[raw_orders]], set to zero for refunds in [[stg_orders]].

### 3. Additivity
Fully additive: it can be summed across months, countries and customers.

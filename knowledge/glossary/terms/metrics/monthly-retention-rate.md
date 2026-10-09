---
title: Monthly Retention Rate
type: term
description: Share of a cohort's customers who order again N months after their first order. Ratio; combine cohorts by summing customers first.
category: metrics
domain: sales
owner: analytics@folio.example
aliases:
- retention
- repeat rate
- cohort retention
resource:
- folio-analytics-demo.reporting.r_customer_retention_monthly.retention_rate
related_terms:
- '[[active-customers]]'
- '[[cohort-month]]'
labels:
  domain: sales
  term_role: standard
  additive: "false"
data_agent_hints:
  formula: SUM(active_customers at offset N) / SUM(active_customers at offset 0), same cohorts
  cannot_average: true
---
### 1. Business definition
For customers who first ordered in [[cohort-month]] M, the retention rate at offset N is the share of them who order in month M + N. Offset 0 is always 100 %.

### 2. Calculation
`retention_rate` in [[r_customer_retention_monthly]] is correct for one cohort. For several cohorts together, sum `active_customers` at offset N, sum `active_customers` at offset 0 for the same cohorts, then divide.

### 3. Additivity
Not additive and not averageable: a small cohort would weigh as much as a large one.

---
title: Active Customers
type: term
description: Distinct customers with at least one paid or refunded order in the period. A distinct count, not additive across periods or countries.
category: metrics
domain: sales
owner: analytics@folio.example
aliases:
- buyers
- active buyers
- monthly active customers
resource:
- folio-analytics-demo.reporting.r_sales_monthly.active_customers
- folio-analytics-demo.reporting.r_customer_retention_monthly.active_customers
related_terms:
- '[[customer]]'
- '[[monthly-retention-rate]]'
labels:
  domain: sales
  term_role: standard
  additive: "false"
data_agent_hints:
  aggregation: COUNT(DISTINCT customer_id)
  cannot_sum_across:
  - month
  - country
---
### 1. Business definition
A [[customer]] is active in a month when they ordered in that month at least once.

### 2. Calculation
Stored per month and country in [[r_sales_monthly]] and per cohort and month in [[r_customer_retention_monthly]].

### 3. Additivity
A customer can order in two countries or in two months, so summing rows double-counts. For a total over several countries or months, count distinct `customer_id` again from [[customer_monthly_activity]]. Summing across countries is only an upper bound.

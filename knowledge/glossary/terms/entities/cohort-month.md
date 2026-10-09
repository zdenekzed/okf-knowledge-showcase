---
title: Cohort Month
type: term
description: Month of a customer's first order. Frozen at acquisition, so a customer belongs to exactly one cohort forever.
category: entities
domain: sales
owner: analytics@folio.example
aliases:
- acquisition month
- first order month
resource:
- folio-analytics-demo.reporting.r_customer_retention_monthly.cohort_month
related_terms:
- '[[customer]]'
- '[[monthly-retention-rate]]'
labels:
  domain: sales
  term_role: entity
---
### 1. Business definition
Customers who first ordered in the same month form a cohort. Comparing cohorts shows whether newer customers come back as often as older ones did.

### 2. Where it lives
Computed in [[customer_monthly_activity]] as the minimum order month per customer and used as a dimension in [[r_customer_retention_monthly]].

---
title: Orders
type: term
description: Number of paid or refunded orders. Cancelled orders are not counted.
category: metrics
domain: sales
owner: analytics@folio.example
aliases:
- order count
- number of orders
resource:
- folio-analytics-demo.reporting.r_sales_monthly.orders
related_terms:
- '[[net-revenue]]'
- '[[average-order-value]]'
labels:
  domain: sales
  term_role: standard
  additive: "true"
data_agent_hints:
  aggregation: SUM
---
### 1. Business definition
An order is one checkout by one [[customer]]. Refunded orders still count as orders (the customer did order); cancelled orders do not.

### 2. Calculation
`SUM(orders)` in [[r_sales_monthly]].

### 3. Additivity
Fully additive across months and countries.

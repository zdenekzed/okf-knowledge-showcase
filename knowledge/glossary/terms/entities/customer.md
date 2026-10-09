---
title: Customer
type: term
description: A person with a Folio account who placed at least one order. Identified by customer_id.
category: entities
domain: general
owner: analytics@folio.example
aliases:
- buyer
- client
related_terms:
- '[[active-customers]]'
- '[[cohort-month]]'
labels:
  domain: general
  term_role: entity
data_agent_hints:
  key_column: customer_id
---
### 1. Business definition
Accounts that never ordered are visitors, not customers. One customer can order from several countries.

### 2. Where it lives
`customer_id` in [[raw_orders]], [[stg_orders]] and [[customer_monthly_activity]]. Reporting marts hold counts of customers, never single customers.

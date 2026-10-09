---
title: Country
type: term
description: Shipping country of an order as an ISO 3166-1 alpha-2 code (DE, FR, CZ).
category: entities
domain: general
owner: analytics@folio.example
aliases:
- market
- shipping country
resource:
- folio-analytics-demo.reporting.r_sales_monthly.country_code
labels:
  domain: general
  term_role: entity
data_agent_hints:
  key_column: country_code
  value_format: ISO 3166-1 alpha-2, upper case
---
### 1. Business definition
The country the order ships to, not the customer's home country or the country of the website.

### 2. Filtering
Filter with upper-case codes: `country_code = "DE"`. "Germany", "German market" and "DE" all mean the same filter.

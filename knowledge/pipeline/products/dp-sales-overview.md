---
title: Sales Overview
type: data_product
description: Monthly sales and customer retention of the Folio shop for management reporting and the analytics agent.
status: active
owner: analytics@folio.example
schedule: daily 06:00 UTC
assets:
- '[[r_sales_monthly]]'
- '[[r_customer_retention_monthly]]'
published_metrics:
- '[[net-revenue]]'
- '[[orders]]'
- '[[average-order-value]]'
- '[[active-customers]]'
- '[[monthly-retention-rate]]'
north_star:
  purpose: Show how much Folio sells, where, and whether new customers come back.
  questions:
  - How did net revenue and average order value develop by country?
  - What share of a month's new customers orders again in the following months?
  boundaries:
  - Monthly grain, closed months only.
  - Aggregated data only; no single customers.
---
A data product is a contract: which tables are its public surface (`assets`), which glossary terms it promises to deliver (`published_metrics`) and what it is for (`north_star`). Only tables listed here are offered to the analytics agent; everything else stays available for lineage and engineering.

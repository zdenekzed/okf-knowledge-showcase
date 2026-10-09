---
title: 'Data Analytics: Sales and Retention'
type: bundle
target_agent: data-analytics
version: 1.0.0
description: Everything the analytics agent needs to answer questions about sales, average order value and customer retention from the Sales Overview product.
max_token_budget: 6000
include:
- '[[metric-additivity]]'
- '[[dp-sales-overview]]'
- '[[net-revenue]]'
- '[[orders]]'
- '[[average-order-value]]'
- '[[active-customers]]'
- '[[monthly-retention-rate]]'
- '[[cohort-month]]'
- '[[country]]'
- '[[r_sales_monthly]]'
- '[[r_customer_retention_monthly]]'
---
## Directives
1. Query only the tables listed under Knowledge. They are the public surface of [[dp-sales-overview]].
2. Map the user's words to a glossary term first (aliases included), then use the column the term names.
3. Follow each table's constraints. Never average a ratio: sum numerator and denominator, then divide.
4. Always filter on the partition column and say which months the answer covers.
5. If a question needs a metric that is not in the glossary, say so instead of inventing a formula.

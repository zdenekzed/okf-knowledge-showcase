---
title: 'Data Engineering: Pipeline and Knowledge Governance'
type: bundle
target_agent: data-engineering
version: 1.0.0
description: Rules and lineage for an engineering agent that changes Dataform models or the vault.
max_token_budget: 8000
include:
- '[[knowledge-layers]]'
- '[[one-owner-per-fact]]'
- '[[gcp-project-map]]'
- '[[raw_orders]]'
- '[[stg_orders]]'
- '[[customer_monthly_activity]]'
- '[[r_sales_monthly]]'
- '[[r_customer_retention_monthly]]'
---
## Directives
1. Never edit files in `knowledge/pipeline/tables/`. Change the `.sqlx` file and run `okf-showcase tables`.
2. Before changing a column, follow `downstream` links to every table and glossary term that depends on it, and update them in the same pull request.
3. A new metric starts as a glossary term; a new reporting table gets a semantics overlay before an agent may use it.
4. Run `okf-showcase build` before opening a pull request; CI runs the same commands.

# 5. Bundles: context for AI agents

## The problem bundles solve

An AI agent answering "what was the average order value in Germany last quarter?" needs: the definition of average order value (a ratio, never averaged), the synonyms (AOV, basket size), the table and its partition column, what one row is, the country code format, and a verified query. That knowledge is spread over a term, an entity, a table record and an overlay.

Hand-writing it into a prompt copies four owners into a fifth place that nobody updates. A bundle **lists** what the agent needs; the compiler **assembles** it on every build.

## Anatomy of a bundle

```yaml
---
title: 'Data Analytics: Sales and Retention'
type: bundle
target_agent: data-analytics       # data-analytics | data-engineering | universal
version: 1.0.0
max_token_budget: 6000             # the build fails above this
include:                           # what the agent needs to know, by link
- '[[metric-additivity]]'          # a concept
- '[[dp-sales-overview]]'          # the product contract
- '[[average-order-value]]'        # terms
- '[[r_sales_monthly]]'            # a table (record + overlay are merged)
---
## Directives                      # how the agent must behave; no definitions here
1. Query only the tables listed under Knowledge.
2. Map the user's words to a glossary term first (aliases included).
3. Never average a ratio: sum numerator and denominator, then divide.
```

## What the compiler produces

`dist/bundles/da-sales-analytics.md`, one self-contained Markdown file:

```
# Data Analytics: Sales and Retention
<directives>
## Knowledge
### Average Order Value
Also called: aov, average basket, basket size
formula: SUM(net_revenue_eur) / SUM(orders)
cannot_average: True
<term body>
---
### r_sales_monthly
BigQuery: folio-analytics-demo.reporting.r_sales_monthly
Grain: One row per order_month × country_code.
| Column | Kind | Description |          ← kind from the overlay, description from BigQuery/Dataform
Constraints: ...
Golden query: ...
```

## Design choices

- **Directives and knowledge are separate.** The body says how to behave; definitions come only from their owners. A reviewer can read the directives in ten lines.
- **Tables are rendered from record + overlay.** The record knows the columns; the overlay knows what they mean for aggregation. Neither alone is enough for correct SQL.
- **A token budget per bundle.** Context windows are large, but irrelevant context still degrades answers and costs money. A budget forces the question "does this agent need this?" and turns growth into a visible CI failure.
- **One bundle per agent role, not per question.** Analytics and engineering agents need different things: the analytics agent gets products and terms, the engineering agent gets lineage and ownership rules.
- **Markdown output.** Every agent framework accepts text; nothing is tied to one vendor.

## Bundles for development agents vs. production agents

The same compile idea serves two audiences:
- **Development agents** (coding assistants in the repo) read bundles like the ones here, or follow `AGENTS.md` directly.
- **Production agents** (a conversational analytics agent in front of business users) get a stricter, product-scoped context: only the product's allowlisted tables, the terms it publishes, golden queries, and an evaluation set to test the agent against. In production this is a second compile target (structured YAML per product) built from the same files.

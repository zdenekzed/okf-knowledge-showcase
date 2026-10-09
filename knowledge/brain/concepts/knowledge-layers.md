---
title: Knowledge layers
type: concept
description: The vault has three layers. Glossary says what things mean, pipeline says where the data physically is, brain says how to use both.
tags:
- architecture
---
## The three layers

| Layer | Folder | Answers | Written by |
| :-- | :-- | :-- | :-- |
| Glossary | `glossary/terms/` | What does "net revenue" mean, how is it computed, can it be summed? | Data stewards |
| Pipeline | `pipeline/tables/` (generated), `pipeline/semantics/`, `pipeline/products/` | Which table and column hold it, what does it depend on, how is a row defined? | Generator + analytics engineers |
| Brain | `brain/concepts/`, `brain/bundles/` | Which rules apply across terms and tables, and what does each agent need to know? | Architects, data leads |

## How they connect
Wikilinks. A term names its column ([[net-revenue]] → [[r_sales_monthly]]), an overlay names its table and terms, a product names its tables and metrics, a bundle names everything an agent needs. Because every link is validated, the connections are as reliable as the documents themselves.

The rule that keeps the layers apart is [[one-owner-per-fact]].

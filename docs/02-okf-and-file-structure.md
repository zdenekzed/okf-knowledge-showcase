# 2. OKF and the file structure

## OKF in one paragraph

The Open Knowledge Format (OKF, v0.1 draft) represents knowledge as a directory of Markdown files with YAML frontmatter. No schema registry, no server, no SDK: if you can `cat` a file you can read it, if you can `git clone` a repository you can ship it. Structured facts go into the frontmatter, explanations for people go into the body, and documents refer to each other by links. This repository uses OKF as the storage format and adds a small set of document types with required fields, plus tools that validate and compile them.

## What OKF requires, and what this repository adds

| | OKF v0.1 | This repository |
| :-- | :-- | :-- |
| Document | Markdown + YAML frontmatter | same |
| Required field | `type` only | per type, a set of required fields (see below), enforced in CI |
| Recommended fields | `title`, `description`, `resource`, `tags`, `timestamp` | used with the same meaning; `resource` is the BigQuery address |
| Reserved files | `index.md` (directory listing), `log.md` (history) | `index.md` generated in every directory; `log.md` not used (git history covers it) |
| Links | standard Markdown links; broken links tolerated | wikilinks `[[slug]]` in frontmatter and body (Obsidian); broken links are an error |
| Strictness | consumers must be permissive | producers here are strict: a pull request with a broken link does not merge |

Two deliberate differences, and why:
- **Wikilinks instead of Markdown links.** Typed relations live in frontmatter (`related_terms`, `upstream`, `include`), where a short `[[slug]]` is readable and survives moving files between folders. Obsidian renders them as a graph. A consumer that only knows standard links still gets every relation from the frontmatter.
- **Strict validation.** OKF is permissive so that any bundle stays readable. This vault is also deployed to Dataplex and fed to agents, so it is checked before merge; the output stays plain OKF that any consumer can read.

A naming note: in OKF a *bundle* is the whole directory tree (here: `knowledge/`). In this repository, `brain/bundles/` holds *context bundles*, specs of what one AI agent gets. The two meanings are unrelated.

## Why Markdown files in git

| Need | How files in git meet it |
| :-- | :-- |
| Review a definition change before it is live | pull request with a readable diff |
| Know who changed a definition and why | git history and the PR discussion |
| Several people editing at once | one file per term: no merge conflicts on a shared spreadsheet |
| AI agents read and write it | plain text, no API, no export step |
| Humans browse it | Obsidian (or any editor) shows the files and their link graph |
| Publish to a catalog | the files are compiled to Dataplex; the catalog is a view, not the source |

## Anatomy of a document

```markdown
---                                   ← frontmatter: facts a machine relies on
title: Average Order Value
type: term                            ← decides which fields are required
description: Net revenue divided by orders in the same slice. ...
category: metrics
owner: analytics@folio.example
aliases: [aov, average basket]
related_terms: ['[[net-revenue]]', '[[orders]]']   ← wikilinks = relations
data_agent_hints:
  formula: SUM(net_revenue_eur) / SUM(orders)
  cannot_average: true
---
### 1. Business definition            ← body: explanation for people
...
```

Rules that apply to every document (`index.md` and `log.md` are reserved OKF file names, not documents):
- The **file name is the slug** and the identity. It must be unique in the vault, so `[[orders]]` always means one file.
- **`type`** selects the required fields (table below). An unknown type is an error.
- **Wikilinks** can use the slug (`[[orders]]`) or the path inside the vault (`[[glossary/terms/metrics/orders]]`). Both are validated.
- **Frontmatter is for facts, the body is for explanation.** A tool may only rely on frontmatter.

## Document types

| `type` | Folder | Required fields | Owner | Purpose |
| :-- | :-- | :-- | :-- | :-- |
| `term` | `glossary/terms/<category>/` | title, description, category, owner | data steward | A business word: meaning, formula, synonyms (`aliases`), column binding (`resource`), agent hints. |
| `dataset` | `pipeline/tables/<layer>/` | title, description, resource, gcp_project, layer, columns | **generator** | One BigQuery table or view: address, columns, partitioning, lineage. |
| `semantics` | `pipeline/semantics/` | table, grain, columns | analytics engineer | What the SQL cannot say: grain, column `kind`, `how_to_count`, constraints, golden queries. |
| `data_product` | `pipeline/products/` | title, description, status, owner, assets | product owner | Contract: public tables, published metrics, purpose and boundaries. |
| `concept` | `brain/concepts/` | title, description | architect, lead | A rule or idea that spans terms and tables (additivity, ownership, project map). |
| `bundle` | `brain/bundles/` | title, description, target_agent, max_token_budget | architect, agent owner | What one agent needs: directives in the body, links in `include`. |

Starting points for each type are in [templates/](../templates/).

## Folder layout and why

```
knowledge/
├── index.md              generated entry point; every directory has one (OKF §6)
├── glossary/terms/
│   ├── metrics/          one file per metric
│   └── entities/         one file per business entity (customer, country, cohort month)
├── pipeline/
│   ├── tables/<layer>/   generated, one file per .sqlx, layer = Dataform folder
│   ├── semantics/        curated, one file per table that needs more than its record
│   └── products/         one contract per data product
└── brain/
    ├── concepts/         cross-cutting knowledge
    └── bundles/          one spec per agent context
```

- **Generated and curated never share a file.** `pipeline/tables/` is rewritten on every run; what people know about a table lives next to it in `pipeline/semantics/`. Regeneration can never overwrite human work, and CI can verify the generated files exactly.
- **Glossary and pipeline are separate** because they change for different reasons and are owned by different people: a definition changes when the business changes, a table changes when the SQL changes. The link between them (`resource` on the term) is validated in both directions.
- **Brain is the only layer that talks about the other two.** Concepts explain rules; bundles decide what an agent sees.

## The term in detail

The term is the center of the design, so its fields deserve a closer look:

| Field | Used by | Example |
| :-- | :-- | :-- |
| `description` (≤ 300 chars) | Dataplex term description, bundle | "Net revenue divided by orders in the same slice." |
| `aliases` | agents mapping user words to terms; search | `aov`, `average basket` |
| `resource` | Dataplex `definition` link; validator | `folio-analytics-demo.reporting.r_sales_monthly.net_revenue_eur` |
| `related_terms` | Dataplex `related` links; graph | `[[net-revenue]]` |
| `labels` | Dataplex labels (format `^[a-z0-9_-]{1,63}$`) | `additive: "false"` |
| `data_agent_hints` | bundles; agents generating SQL | `formula`, `cannot_average`, `cannot_sum_across` |
| body sections 1–3 | people; bundles | definition, calculation, additivity |

A metric that is stored in a column gets a `resource`. A metric that is always computed (a ratio such as average order value) gets no `resource` but a `formula`: storing a ratio per row only invites someone to average it.

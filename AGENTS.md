# Instructions for AI agents

This file is the single source of instructions for any AI agent (Claude Code, Gemini, Copilot, Cursor, …) working in this repository. `CLAUDE.md` and `GEMINI.md` only point here.

## What this repository is

A knowledge-as-code pipeline. Business and technical knowledge lives as OKF documents (Markdown + YAML frontmatter) in `knowledge/`. Tools in `src/okf_showcase/` generate, validate and compile it. The flow: Dataform SQL → generated table records → validation → agent bundles and a Dataplex glossary plan. See the diagram in [README.md](README.md).

## Mental model in five sentences

1. Every fact has exactly one owner file; everything else is compiled from it ([one-owner-per-fact](knowledge/brain/concepts/one-owner-per-fact.md)).
2. **Glossary** (`knowledge/glossary/terms/`) says what a business word means and how to compute it.
3. **Pipeline** (`knowledge/pipeline/`) says where the data physically is: generated table records, curated semantics overlays, data product contracts.
4. **Brain** (`knowledge/brain/`) holds cross-cutting rules (concepts) and the specs of agent context bundles.
5. Wikilinks (`[[slug]]` or `[[path/in/vault]]`) are the relations between all of them, and every link is validated.

## Where to find what

Start at [knowledge/index.md](knowledge/index.md) and follow the indexes down: every directory has an `index.md` listing its documents with a one-line description. Open a document only when its description says it is relevant.


| You need | Look in |
| :-- | :-- |
| What a metric means, its formula, synonyms, whether it can be summed | `knowledge/glossary/terms/metrics/<term>.md` (`aliases`, `data_agent_hints`, body section 3) |
| Which BigQuery column holds a metric | the term's `resource` (`project.dataset.table.column`) |
| A table's columns, GCP project, lineage | `knowledge/pipeline/tables/<layer>/<table>.md` (`resource`, `columns`, `upstream`, `downstream`) |
| What one row of a table is, how to aggregate a column, a verified query | `knowledge/pipeline/semantics/<table>.semantics.md` |
| Which tables an analytics agent may use | `assets` of `knowledge/pipeline/products/dp-*.md` |
| Which GCP project holds what | `okf.yaml` (`gcp_projects`) and [gcp-project-map](knowledge/brain/concepts/gcp-project-map.md) |
| Why something is built this way | `docs/` and `docs/decisions/` |

## Rules for changing things

- **Never edit `knowledge/pipeline/tables/**`.** These files are generated. Change the `.sqlx` file under `example/dataform/definitions/` and run `uv run okf-showcase tables`. CI fails if a committed record differs from a fresh generation.
- **Never edit `dist/` or any `index.md`.** Both are generated; run `uv run okf-showcase index` after adding, renaming or re-describing a document.
- **Curated knowledge about a table goes into its overlay** `knowledge/pipeline/semantics/<table>.semantics.md`, never into the generated record.
- **A new metric starts as a glossary term** (copy `templates/term.md`). If it is stored in a column, set `resource` to the full column address; if it is a ratio, leave `resource` out and give `data_agent_hints.formula`.
- **Every ratio or distinct-count column in an overlay needs `how_to_count`.** The validator enforces it.
- **A new table in a GCP project not listed in `okf.yaml` fails validation.** Add the project to `gcp_projects` with its role first.
- **Bundles list knowledge, they do not copy it.** Add a wikilink to `include`; never paste a definition into a bundle body. The body holds directives only.
- **Term descriptions stay under 300 characters** (Dataplex limit); details go into the body.
- **File names are slugs**: lowercase, digits, `-`, `_` (overlays add `.semantics`). The slug must be unique in the vault.

## Commands

```bash
uv sync                               # install
uv run okf-showcase build             # tables, validate, bundles, dataplex plan, graph
uv run okf-showcase tables --check    # generated records are up to date
uv run okf-showcase index --check     # generated indexes are up to date
uv run okf-showcase validate          # the vault is consistent
uv run pytest                         # tests
uv run ruff check . && uv run ruff format --check .
```

Run `build`, `tables --check`, `index --check` and `pytest` before you say a change is done; CI runs the same.

## When you answer a data question from this knowledge

1. Map the user's words to a glossary term through `title` and `aliases`.
2. Take the column from the term's `resource`; for a ratio take `data_agent_hints.formula`.
3. Read the overlay of that table: grain, `kind`, `how_to_count`, `constraints`.
4. Prefer a golden query from the overlay when it fits the question.
5. If no term covers the question, say so; do not invent a definition.

The compiled version of exactly this context is `dist/bundles/da-sales-analytics.md`.

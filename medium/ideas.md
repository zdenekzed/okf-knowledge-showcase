# Article ideas

Brainstorm and backlog. This file owns the status of every article, for both language versions (`idea`, or e.g. `en: published, cs: drafting`); see [README.md](README.md) for the workflow.

## Article types

| Type | What it does | Length | What the repository gives it |
| :-- | :-- | :-- | :-- |
| Manifesto | Names a problem every data team has and takes a stance | 6–8 min | proof that the stance runs: README, the flow |
| Principle | One rule: why it holds, what it costs | 5–7 min | one concept or decision record |
| Walkthrough | The reader runs it and changes something | 8–12 min | commands, a demo merge request |
| How it works | How one integration works, in detail | 8–10 min | the module and its docs page |
| Anti-pattern | A failure, its cause, the check that now prevents it | 3–5 min | the validator rule or CI gate |
| Decision story | One decision record told as a story: options, choice, cost | 4–6 min | the ADR |
| Comparison | Places the approach among the alternatives | 6–8 min | little; needs outside research |
| Checklist | Something to bookmark and copy | 4–6 min | `validate.py`, the CI workflow |
| Series hub | Index of a series, updated as it grows | 2 min | none |

Two cheap recurring formats keep a steady cadence: each of the six decision records is a ready decision story, and each validator check is a short anti-pattern post.

## Backlog

### A. Knowledge as code (the core series)

| # | Working title | Type | Angle | Repository anchors | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| A1 | Revenue is defined in four places | Manifesto | SQL, BI field, wiki and agent prompt drift apart. One owner per fact, everything else compiled. | [README](../README.md), [the flow](../docs/01-the-flow.md) | idea |
| A2 | One owner per fact | Principle | A wrong answer traces back to exactly one file, and fixing it fixes every place that shows it. | [one-owner-per-fact](../knowledge/brain/concepts/one-owner-per-fact.md), [layers](../docs/03-layers-and-ownership.md) | idea |
| A3 | Never let a machine and a human edit the same file | Principle | Generated records and curated overlays in separate files; CI checks the generated ones byte for byte. | [ADR 0003](../docs/decisions/0003-generated-and-curated-never-share-a-file.md), [tables.py](../src/okf_showcase/tables.py), [semantics/](../knowledge/pipeline/semantics/) | idea |
| A4 | Markdown in git, the catalog is a view | Decision story | Why Dataplex is not the source, and how UI edits come back as a merge request. | [ADR 0001](../docs/decisions/0001-markdown-in-git-is-the-source.md), [dataplex.py](../src/okf_showcase/dataplex.py) | idea |
| A5 | A rule only an LLM can check is not a rule | Checklist | The validator checks worth copying, each with the bug it catches. | [validate.py](../src/okf_showcase/validate.py), [CI and governance](../docs/06-ci-and-governance.md) | idea |
| A6 | A change end to end: net revenue without shipping | Walkthrough | One merge request shows the SQL diff, the record diff and the definition diff side by side. | [the flow, last section](../docs/01-the-flow.md), [net-revenue](../knowledge/glossary/terms/metrics/net-revenue.md); needs a demo MR | idea |

### B. Context for AI agents

| # | Working title | Type | Angle | Repository anchors | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| B1 | Why your data agent averages ratios | Anti-pattern | Additive, distinct count, ratio: three kinds of measures, and `how_to_count` enforced by the validator. Useful without adopting anything else. | [metric-additivity](../knowledge/brain/concepts/metric-additivity.md), [monthly-retention-rate](../knowledge/glossary/terms/metrics/monthly-retention-rate.md), [retention overlay](../knowledge/pipeline/semantics/r_customer_retention_monthly.semantics.md) | idea |
| B2 | Stop writing prompts. Compile them. | Principle | Directives written by hand, knowledge included by link and assembled on every build. | [ADR 0006](../docs/decisions/0006-agents-get-compiled-bundles.md), [bundles.py](../src/okf_showcase/bundles.py), [da-sales-analytics](../knowledge/brain/bundles/da-sales-analytics.md) | idea |
| B3 | A token budget is a CI gate | Principle (short) | Prompt growth shows up as a failing build, not as slowly worse answers. | [bundles](../docs/05-bundles.md), `max_token_budget` | idea |
| B4 | Scope agents with data product contracts | Principle | The agent is offered a product's tables, not the whole warehouse. | [dp-sales-overview](../knowledge/pipeline/products/dp-sales-overview.md), [layers](../docs/03-layers-and-ownership.md) | idea |
| B5 | Golden queries live next to the table | Walkthrough | Verified SQL in the overlay, compiled into the bundle; next step: evaluation sets. | [r_sales_monthly overlay](../knowledge/pipeline/semantics/r_sales_monthly.semantics.md) | idea |
| B6 | One AGENTS.md for every coding agent | Practice | `CLAUDE.md` and `GEMINI.md` only point to it; agents pass the same gates as people. | [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md), [GEMINI.md](../GEMINI.md) | idea |
| B7 | An index.md in every folder | Practice | Progressive disclosure: the agent reads three lines, then descends only where it needs to. Generated, checked in CI. | [index.py](../src/okf_showcase/index.py), [knowledge/index.md](../knowledge/index.md) | idea |

### C. Google Cloud hands-on

Candidates for the Google Cloud – Community publication on Medium.

| # | Working title | Type | Angle | Repository anchors | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| C1 | Linking BigQuery columns to Dataplex glossary terms from git | How it works | Entry links, two passes, link IDs hashed from both ends, so the deploy is idempotent. | [ADR 0005](../docs/decisions/0005-two-pass-dataplex-deploy.md), [back to GCP](../docs/04-back-to-gcp.md), [dataplex.py](../src/okf_showcase/dataplex.py) | idea |
| C2 | Dataform CREATE OR REPLACE erased our column descriptions | Anti-pattern | Why it happens, and persisting and re-applying descriptions in pre/post operations. | [back to GCP, section 3](../docs/04-back-to-gcp.md) | idea |
| C3 | Who owns a column description: BigQuery or Dataform? | Decision story | BigQuery first, Dataform fills the gaps, `description_source` tells the reviewer which writer to fix. | [ADR 0004](../docs/decisions/0004-column-descriptions-bigquery-first.md), [information_schema.json](../example/bigquery/information_schema.json) | idea |
| C4 | Lineage and meaning in one query | How it works | The vault as a BigQuery property graph: which glossary terms break if `stg_orders` changes. | [property graph](../docs/07-property-graph.md), [graph.py](../src/okf_showcase/graph.py) | idea |
| C5 | A GCP project map the validator enforces | Principle (short) | Projects split by role; a table in an undeclared project fails the merge request. | [okf.yaml](../okf.yaml), [gcp-project-map](../knowledge/brain/concepts/gcp-project-map.md) | idea |
| C6 | Generate your table catalog from Dataform | Walkthrough | One record per `.sqlx` with lineage both ways; in production from `dataform compile --json`. | [tables.py](../src/okf_showcase/tables.py), [example/dataform/](../example/dataform/) | idea |

### D. Format and tooling

| # | Working title | Type | Angle | Repository anchors | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| D1 | Open Knowledge Format in practice | Comparison | A permissive spec and a strict producer: what was kept, what was made stricter, and why. | [OKF and file structure](../docs/02-okf-and-file-structure.md) | idea |
| D2 | Anatomy of a glossary term | Checklist | Field by field: who reads it (Dataplex, validator, agent, human). | [the term in detail](../docs/02-okf-and-file-structure.md), [templates/term.md](../templates/term.md) | idea |
| D3 | Obsidian as a free catalog UI | Walkthrough (visual) | Wikilinks become a graph view; screenshots carry the article. | [knowledge/](../knowledge/) | idea |
| D4 | One file per term | Decision story | A glossary designed for merge requests: no merge conflicts, renames caught by the validator. | [ADR 0002](../docs/decisions/0002-one-file-per-term.md) | idea |
| D5 | Decision records people actually read | Practice | Short ADRs that lead with consequences. | [docs/decisions/](../docs/decisions/) | idea |

### E. People and governance

| # | Working title | Type | Angle | Repository anchors | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| E1 | Who edits what | Principle (for leads) | Roles mapped to files; CI edits whatever no person owns. | [README, "Who does what"](../README.md) | idea |
| E2 | Humans decide at a few points only | Principle | Where review is worth it, and why everything else is automatic or blocks the author. | [CI and governance](../docs/06-ci-and-governance.md) | idea |
| E3 | Knowledge as code, semantic layer, catalog first | Comparison | Where dbt's semantic layer, LookML and a catalog-first glossary fit, and where this approach complements them. | none; needs research | idea |
| E4 | How to build an honest showcase of a production system | Practice | The "what is simplified here" table as a pattern for demo repositories. | [README, "What is simplified"](../README.md) | idea |

## What to publish first

1. **A1**: the opener. Every later article links back to it.
2. **B1**: the widest audience, useful to readers who never clone the repository, and it carries the AI hook.
3. **A6**: the proof. The reader sees the whole flow in one merge request.
4. **C1**: the first submission to Google Cloud – Community.
5. **B2**: the second AI article, building on B1.

Then a series hub, and roughly one article every two weeks, alternating a principle with a hands-on piece.

## Assets to prepare in the repository

- A demo merge request for A6 ("exclude shipping from net revenue") and screenshots of its diff.
- The CI on GitLab: today the repository has a GitHub Actions workflow, which GitLab does not run. Articles A5, A6 and E2 need a `.gitlab-ci.yml` with the same gates.
- PNG exports of the Mermaid diagrams (Medium does not render Mermaid).
- A screenshot of the Obsidian graph view (hero image for A1 and D3).
- One tag per article (`article-01`, …) for stable links.
- An "Articles" section in the root README once A1 is published.

## Decided

- **Language:** English is the primary version, every article also gets a Czech version (rules in [README.md](README.md#two-languages)).
- **Repository:** a personal GitLab account; links point to tags there.

## Open questions

- **Partner Program:** paywall or free. Free brings more readers to the repository; the Partner Program pays from member reading time.
- **Where the original lives:** Medium itself, or a personal blog (for example GitLab Pages built from this folder) with Medium importing from it. Decides the canonical URL of every article.
- **Where the Czech version goes:** the personal blog, LinkedIn articles, or both.
- **Livesport:** whether the articles may mention the production setup the showcase is based on.

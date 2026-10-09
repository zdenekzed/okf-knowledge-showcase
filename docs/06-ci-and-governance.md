# 6. CI and governance

## Gates

| Gate | When | Command | Blocks |
| :-- | :-- | :-- | :-- |
| Lint and tests | every pull request | `ruff check`, `ruff format --check`, `pytest` | merge |
| Generated-file guard | every pull request | `okf-showcase tables --check`, `okf-showcase index --check` | a hand edit of a generated record or index, or a change without regenerated files |
| Vault validation | every pull request | `okf-showcase validate` | broken links, missing fields, term → column mismatch, unknown project |
| Bundle budget | every pull request | `okf-showcase bundles` | a bundle over its token budget |
| Glossary deploy | merge to `main` | `okf-showcase dataplex` (+ a real deployer) | nothing; reports what changed |

All of them are in [.github/workflows/ci.yml](../.github/workflows/ci.yml).

## Principles

- **Every check runs locally with the same command.** If CI fails, `uv run okf-showcase build` reproduces it. No check exists only inside CI, and none needs an LLM.
- **`main` is always deployable.** Anything that would break the Dataplex deploy is caught on the pull request (description length, label format, links).
- **Humans decide at a few points only.** Reviewing a definition change, reviewing a large schema change, fixing a failed deploy. Everything else is automatic or blocks the author.
- **A CI job exists only if it does work.** No placeholder jobs; a reader of the workflow file can trust that every step runs.
- **Agents follow the same process.** An AI agent that changes a term opens a pull request and passes the same gates; a human merges.

## In production, additionally

- A **scheduled sync** regenerates table records from the Dataform repository every night. A small change (new column description) is merged automatically; a large one (dropped column, new table) opens a pull request for review.
- A **daily drift check** compares records with BigQuery and reports tables that exist in one but not the other.
- Notifications name the commit, the pipeline run and the exact failed check, so a message is actionable without opening CI.

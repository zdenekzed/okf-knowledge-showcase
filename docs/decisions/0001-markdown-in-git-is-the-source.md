# 0001: Markdown in git is the source of truth, Dataplex is a view

**Status:** accepted

## Context
The glossary has to be visible in Dataplex, where analysts and BigQuery Studio see it. Dataplex is also editable. If both the catalog and files are edited, they drift.

## Decision
Terms are written as OKF Markdown files in git. Dataplex is deployed from them on every merge to `main`. Edits made in the Dataplex UI are turned into a pull request against the files (reverse sync), never kept only in Dataplex.

## Consequences
- Every definition change is reviewed in a pull request and has a history.
- AI agents can read and propose changes without API access.
- The catalog can be rebuilt from scratch at any time.
- Someone who prefers the Dataplex UI still can use it, with a review step in between.

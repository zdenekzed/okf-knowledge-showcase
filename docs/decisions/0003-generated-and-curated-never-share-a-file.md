# 0003: Generated and curated knowledge never share a file

**Status:** accepted

## Context
Table records are generated from Dataform on every run. People also need to write things about tables that SQL cannot express: grain, how to aggregate a column, verified queries. If both live in one file, either regeneration overwrites human work or the generator has to merge, which is fragile.

## Decision
Generated records live in `pipeline/tables/` and are fully rewritten. Curated knowledge lives in `pipeline/semantics/<table>.semantics.md`. Compilers merge the two. CI fails when a committed generated record differs from a fresh generation.

## Consequences
- Generation is a plain overwrite and can be verified byte for byte.
- A hand edit of a generated file is caught on the pull request.
- An overlay referencing a column that no longer exists fails validation, so schema changes surface where curated knowledge needs an update.

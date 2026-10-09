# 0004: Column descriptions: BigQuery first, Dataform second

**Status:** accepted

## Context
Column descriptions are written in two places: the Dataform `columns {}` block and BigQuery itself (console, Dataplex description workflows, DDL). Users see the BigQuery one.

## Decision
The table generator reads descriptions from BigQuery `INFORMATION_SCHEMA` for the projects listed in `okf.yaml` and uses them where present; Dataform fills the gaps. Each column records `description_source`.

## Consequences
- The vault shows what users see.
- Reviewers know which writer to fix.
- Projects without read access keep Dataform descriptions instead of losing them.
- Dataform `CREATE OR REPLACE` must persist and re-apply descriptions set outside Dataform, or each run erases them.

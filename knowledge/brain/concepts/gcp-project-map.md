---
title: GCP project map
type: concept
description: Which GCP project holds which data, where Dataform runs, and how the vault points back to BigQuery.
tags:
- gcp
- dataform
---
## Projects (fictional)
| Project | Role | Holds |
| :-- | :-- | :-- |
| `folio-raw-demo` | sources | Landing tables from the shop backend. Dataform declares them, never writes. |
| `folio-dwh-demo` | transformation | Dataform `defaultProject`: staging and analytics layers. |
| `folio-analytics-demo` | analytics | Reporting marts, the Dataplex business glossary, the data agents. |

The map lives in `okf.yaml`; this page explains it.

## How the vault points back to GCP
- Every table record carries `resource: bigquery:<project>.<dataset>.<table>` and `gcp_project`. The project comes from `database:` in the `.sqlx` config, or from `defaultProject` in `workflow_settings.yaml`.
- Every glossary term with a column carries `resource: <project>.<dataset>.<table>.<column>`; it becomes a Dataplex `definition` link on that BigQuery column.
- Column descriptions are read back from BigQuery `INFORMATION_SCHEMA` for the projects in `bigquery_description_projects`. Each column records `description_source: bigquery | dataform`.

## Why split projects
Separate projects separate costs, permissions and blast radius: the transformation project can be rebuilt freely, while the analytics project is what dashboards and agents read and what the glossary describes. See [[knowledge-layers]].

# 7. Optional: the vault as a property graph

The vault already is a graph: documents are nodes, frontmatter links are edges. `okf-showcase graph` writes it to `dist/graph/graph.json`:

| Edge | From → to | From field |
| :-- | :-- | :-- |
| `DEPENDS_ON` | table → table | `upstream` |
| `DEFINES_COLUMN` | term → table | `resource` |
| `RELATED_TO` | term → term | `related_terms` |
| `DESCRIBES` | overlay → table | `table` |
| `CONTAINS` | product → table | `assets` |
| `PUBLISHES` | product → term | `published_metrics` |
| `INCLUDES` | bundle → anything | `include` |

## When it is worth it

Files and wikilinks answer "what is X" well. A graph answers questions that walk several hops at once:
- Which glossary terms are affected if `stg_orders` changes? (`DEPENDS_ON*` downstream, then `DEFINES_COLUMN` backwards)
- Which agents see a table? (`INCLUDES`, directly or through a product)
- Which published metrics have no golden query?

If nobody asks such questions, skip this step: the graph is derived, so it can be added later without changing a single document.

## Loading it into BigQuery

Load `nodes` and `edges` into two tables, then declare a property graph over them:

```sql
CREATE OR REPLACE PROPERTY GRAPH `folio-analytics-demo.okf_graph.knowledge`
  NODE TABLES (
    `folio-analytics-demo.okf_graph.nodes` KEY (id) LABEL Doc PROPERTIES (id, type, title)
  )
  EDGE TABLES (
    `folio-analytics-demo.okf_graph.edges`
      KEY (source, label, target)
      SOURCE KEY (source) REFERENCES `folio-analytics-demo.okf_graph.nodes` (id)
      DESTINATION KEY (target) REFERENCES `folio-analytics-demo.okf_graph.nodes` (id)
      LABEL Link PROPERTIES (label)
  );
```

Terms affected by a change of `stg_orders`:

```sql
GRAPH `folio-analytics-demo.okf_graph.knowledge`
MATCH (changed:Doc {id: 'pipeline/tables/1_staging/stg_orders'})
      <-[d:Link WHERE d.label = 'DEPENDS_ON']-{1,5}(t:Doc)
      <-[def:Link WHERE def.label = 'DEFINES_COLUMN']-(term:Doc)
RETURN DISTINCT term.title, t.title AS via_table
```

A production setup can go further and model columns as nodes and join keys as edges, which lets an agent find join paths between tables. That is a separate design; this export is the minimal starting point.

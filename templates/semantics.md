---
type: semantics
table: table_slug                       # file name must be table_slug.semantics.md
product: '[[dp-product]]'
grain: One row per ...
columns:
  some_dimension:
    kind: dimension                     # dimension | additive | distinct_count | ratio
  some_ratio:
    kind: ratio
    term: '[[glossary-term]]'
    how_to_count: SUM(numerator) / SUM(denominator)   # required for ratio and distinct_count
constraints:
- Filter on the partition column in every query.
golden_queries:
- question: A question this query answers
  sql: |
    SELECT ...
---
Curated meaning of [[table_slug]].

---
type: semantics
table: r_customer_retention_monthly
product: '[[dp-sales-overview]]'
grain: One row per cohort_month × months_since_first_order. Offsets with no active customer have no row.
columns:
  cohort_month:
    kind: dimension
    term: '[[cohort-month]]'
  months_since_first_order:
    kind: dimension
  active_customers:
    kind: distinct_count
    term: '[[active-customers]]'
    how_to_count: SUM across cohorts is valid (a customer belongs to one cohort); never across offsets
  retention_rate:
    kind: ratio
    term: '[[monthly-retention-rate]]'
    how_to_count: SUM(active_customers at offset N) / SUM(active_customers at offset 0) for the same cohorts
constraints:
- Never AVG(retention_rate) across cohorts; recompute it from active_customers.
- The newest cohorts have no rows for future offsets yet; compare cohorts only at offsets all of them have reached.
golden_queries:
- question: Month-1 retention of all cohorts of the last year together
  sql: |
    SELECT
      SAFE_DIVIDE(
        SUM(IF(months_since_first_order = 1, active_customers, 0)),
        SUM(IF(months_since_first_order = 0, active_customers, 0))
      ) AS m1_retention
    FROM `folio-analytics-demo.reporting.r_customer_retention_monthly`
    WHERE cohort_month >= DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 13 MONTH)
      AND cohort_month < DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
---
Curated meaning of [[r_customer_retention_monthly]].

---
type: semantics
table: r_sales_monthly
product: '[[dp-sales-overview]]'
grain: One row per order_month × country_code.
columns:
  order_month:
    kind: dimension
    role: partition_key
  country_code:
    kind: dimension
    term: '[[country]]'
  orders:
    kind: additive
    term: '[[orders]]'
  active_customers:
    kind: distinct_count
    term: '[[active-customers]]'
    how_to_count: SUM only within one month and one country; recount from customer_monthly_activity otherwise
  net_revenue_eur:
    kind: additive
    term: '[[net-revenue]]'
constraints:
- Filter on order_month in every query; it is the partition key.
- Average order value is SUM(net_revenue_eur) / SUM(orders) over the selected rows, never an AVG of a per-row ratio.
- Do not sum active_customers across months or countries.
golden_queries:
- question: Net revenue and average order value by country, last 3 closed months
  sql: |
    SELECT
      country_code,
      SUM(net_revenue_eur) AS net_revenue_eur,
      SAFE_DIVIDE(SUM(net_revenue_eur), SUM(orders)) AS average_order_value
    FROM `folio-analytics-demo.reporting.r_sales_monthly`
    WHERE order_month >= DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 3 MONTH)
      AND order_month < DATE_TRUNC(CURRENT_DATE(), MONTH)
    GROUP BY country_code
    ORDER BY net_revenue_eur DESC
---
Curated meaning of [[r_sales_monthly]] that the Dataform code cannot express: what one row is, how each column may be aggregated, and a verified query. Written by people, validated by `okf-showcase validate`, merged with the generated record when bundles are compiled.

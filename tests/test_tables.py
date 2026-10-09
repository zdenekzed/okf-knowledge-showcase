from okf_showcase import tables
from okf_showcase.vault import split_frontmatter


def test_config_parser_handles_js_syntax():
    source = """config {
      type: 'table',            // single quotes and a comment
      description: "Status: paid, refunded",
      bigquery: { clusterBy: ["a", "b"], },
    }"""
    config = tables.js_object_to_python(tables.extract_config(source))
    assert config == {
        "type": "table",
        "description": "Status: paid, refunded",
        "bigquery": {"clusterBy": ["a", "b"]},
    }


def test_lineage_and_projects(settings):
    models = {m.name: m for m in tables.load_models(settings)}
    assert models["stg_orders"].upstream == ["raw_orders"]
    assert sorted(models["stg_orders"].downstream) == ["customer_monthly_activity", "r_sales_monthly"]
    assert models["raw_orders"].project == "folio-raw-demo"
    assert models["stg_orders"].project == "folio-dwh-demo"  # defaultProject from workflow_settings.yaml
    assert models["r_sales_monthly"].address == "folio-analytics-demo.reporting.r_sales_monthly"


def test_bigquery_description_wins_over_dataform(settings):
    records = {path.stem: split_frontmatter(text)[0] for path, text in tables.generate(settings).items()}
    columns = records["r_sales_monthly"]["columns"]
    assert columns["net_revenue_eur"]["description_source"] == "bigquery"
    assert columns["orders"]["description_source"] == "dataform"


def test_committed_records_are_up_to_date(settings):
    assert tables.check(settings) == []


def test_check_detects_hand_edit(scratch):
    record = scratch.vault / "pipeline/tables/3_reporting/r_sales_monthly.md"
    record.write_text(record.read_text() + "\nA hand-written note.\n")
    assert any("r_sales_monthly" in problem for problem in tables.check(scratch))

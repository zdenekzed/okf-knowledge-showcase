import pytest

from okf_showcase import bundles, dataplex, graph
from okf_showcase.vault import Vault


def test_bundle_contains_overlay_and_aliases(settings):
    vault = Vault(settings.vault)
    text = bundles.compile_bundle(vault.resolve("da-sales-analytics"), vault)
    assert "**Grain:** One row per order_month × country_code." in text  # from the overlay
    assert "**Also called:** revenue, net sales, sales" in text  # from the term
    assert "folio-analytics-demo.reporting.r_sales_monthly" in text  # from the generated record


def test_bundle_budget_is_enforced(settings):
    vault = Vault(settings.vault)
    bundle = vault.resolve("da-sales-analytics")
    bundle.meta["max_token_budget"] = 100
    with pytest.raises(bundles.BudgetExceeded):
        bundles.compile_bundle(bundle, vault)


def test_dataplex_plan_has_two_passes(settings):
    plan = dataplex.build_plan(settings)
    terms = [op for op in plan["pass_1_terms"] if "/terms/" in op["resource"]]
    assert len(terms) == 8
    definitions = [op for op in plan["pass_2_links"] if op["body"]["entryLinkType"].endswith("/definition")]
    # one definition link per column named by a term
    assert len(definitions) == 7
    source = definitions[0]["body"]["entryReferences"][0]
    assert source["type"] == "SOURCE" and source["path"].startswith("Schema.")


def test_related_links_are_written_once(settings):
    links = [op["resource"] for op in dataplex.build_plan(settings)["pass_2_links"]]
    assert len(links) == len(set(links))


def test_graph_edges(settings):
    edges = {(e["source"], e["label"], e["target"]) for e in graph.build(settings)["edges"]}
    assert (
        "pipeline/tables/3_reporting/r_sales_monthly",
        "DEPENDS_ON",
        "pipeline/tables/1_staging/stg_orders",
    ) in edges
    assert (
        "glossary/terms/metrics/net-revenue",
        "DEFINES_COLUMN",
        "pipeline/tables/3_reporting/r_sales_monthly",
    ) in edges

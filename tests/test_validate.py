from okf_showcase.validate import validate


def test_example_vault_is_valid(settings):
    assert validate(settings) == []


def _messages(settings):
    return [str(issue) for issue in validate(settings)]


def test_broken_wikilink(scratch):
    term = scratch.vault / "glossary/terms/metrics/orders.md"
    term.write_text(term.read_text().replace("[[net-revenue]]", "[[gross-revenue]]"))
    assert any("broken wikilink [[gross-revenue]]" in m for m in _messages(scratch))


def test_term_column_must_exist(scratch):
    term = scratch.vault / "glossary/terms/metrics/orders.md"
    term.write_text(term.read_text().replace("r_sales_monthly.orders", "r_sales_monthly.order_count"))
    assert any("names a column the table does not have" in m for m in _messages(scratch))


def test_ratio_needs_how_to_count(scratch):
    overlay = scratch.vault / "pipeline/semantics/r_customer_retention_monthly.semantics.md"
    text = overlay.read_text()
    start = text.index("    how_to_count: SUM(active_customers at offset N)")
    overlay.write_text(text[:start] + text[text.index("\n", start) + 1 :])
    assert any("retention_rate" in m and "how_to_count" in m for m in _messages(scratch))


def test_unknown_gcp_project(scratch):
    (scratch.root / "okf.yaml").write_text(
        (scratch.root / "okf.yaml").read_text().replace("  folio-raw-demo:", "  folio-other-demo:")
    )
    from okf_showcase.settings import load

    assert any("folio-raw-demo" in m and "gcp_projects" in m for m in _messages(load(scratch.root)))

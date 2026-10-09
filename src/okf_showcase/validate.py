"""Step 2 of the flow: one validator for the whole vault, the same in CI and on a laptop.

What it checks, and why:
- Frontmatter per document type: an agent or a deploy job can rely on a field only if every
  document of that type has it.
- Every wikilink resolves and every slug is unique: links are the lineage and the glossary
  relations, so a broken link is a broken fact, not a cosmetic issue.
- Cross-layer bindings: a glossary term that names a BigQuery column must point at a column that
  exists in a table record; an overlay may only describe columns of its table; a table must live
  in a known GCP project.
- Limits of the target systems (Dataplex label format, description length), so the deploy never
  fails on something a pull request could have caught.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from okf_showcase.settings import Settings
from okf_showcase.vault import Doc, Vault, wikilinks

SLUG = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
LABEL = re.compile(r"^[a-z0-9_-]{1,63}$")
COLUMN_RESOURCE = re.compile(r"^[a-z0-9-]+\.[A-Za-z0-9_]+\.[A-Za-z0-9_]+\.[A-Za-z0-9_]+$")
TERM_DESCRIPTION_MAX = 300

REQUIRED = {
    "term": ["title", "description", "category", "owner"],
    "dataset": ["title", "description", "resource", "gcp_project", "layer", "columns"],
    "semantics": ["table", "grain", "columns"],
    "data_product": ["title", "description", "status", "owner", "assets"],
    "concept": ["title", "description"],
    "bundle": ["title", "description", "target_agent", "max_token_budget"],
}
COLUMN_KINDS = {"dimension", "additive", "distinct_count", "ratio"}
PRODUCT_STATUS = {"draft", "active", "deprecated"}
TARGET_AGENTS = {"data-analytics", "data-engineering", "universal"}


@dataclass(frozen=True)
class Issue:
    rel: str
    message: str

    def __str__(self) -> str:
        return f"{self.rel}: {self.message}"


def validate(settings: Settings) -> list[Issue]:
    vault = Vault(settings.vault)
    issues: list[Issue] = []
    for slug, docs in vault.by_slug.items():
        if len(docs) > 1:
            issues += [Issue(doc.rel, f"slug '{slug}' is not unique") for doc in docs]
    for doc in vault.docs.values():
        issues += _check_doc(doc, vault, settings)
    return issues


def _check_doc(doc: Doc, vault: Vault, settings: Settings) -> list[Issue]:
    issues = []

    def fail(message: str) -> None:
        issues.append(Issue(doc.rel, message))

    if doc.type not in REQUIRED:
        fail(f"unknown type '{doc.type}' (expected one of {sorted(REQUIRED)})")
        return issues
    for key in REQUIRED[doc.type]:
        if doc.meta.get(key) in (None, "", [], {}):
            fail(f"missing '{key}'")
    if not SLUG.match(doc.slug):
        fail("file name must be lowercase letters, digits, '-', '_' or '.'")
    for target in set(wikilinks(doc.meta)) | set(wikilinks(doc.body)):
        if vault.resolve(target) is None:
            fail(f"broken wikilink [[{target}]]")

    check = {
        "term": _check_term,
        "dataset": _check_dataset,
        "semantics": _check_semantics,
        "data_product": _check_product,
        "bundle": _check_bundle,
    }.get(doc.type)
    if check:
        check(doc, vault, settings, fail)
    return issues


def _check_term(doc, vault, settings, fail) -> None:
    if len(str(doc.meta.get("description", ""))) > TERM_DESCRIPTION_MAX:
        fail(f"description is longer than {TERM_DESCRIPTION_MAX} characters (Dataplex term limit)")
    for key, value in (doc.meta.get("labels") or {}).items():
        if not (LABEL.match(str(key)) and LABEL.match(str(value))):
            fail(f"label {key}={value} does not match {LABEL.pattern}")
    for resource in doc.meta.get("resource") or []:
        if not COLUMN_RESOURCE.match(resource):
            fail(f"resource '{resource}' is not project.dataset.table.column")
            continue
        project, dataset, table, column = resource.split(".")
        record = vault.resolve(table)
        if record is None or record.type != "dataset":
            fail(f"resource '{resource}' names a table without a record")
        elif record.meta["resource"] != f"bigquery:{project}.{dataset}.{table}":
            fail(f"resource '{resource}' does not match the table address {record.meta['resource']}")
        elif column not in record.meta.get("columns", {}):
            fail(f"resource '{resource}' names a column the table does not have")


def _check_dataset(doc, vault, settings, fail) -> None:
    if doc.meta.get("gcp_project") not in settings.gcp_projects:
        fail(f"project '{doc.meta.get('gcp_project')}' is not in the gcp_projects map of okf.yaml")


def _check_semantics(doc, vault, settings, fail) -> None:
    table = vault.resolve(str(doc.meta.get("table", "")))
    if table is None or table.type != "dataset":
        fail(f"table '{doc.meta.get('table')}' has no generated record")
        return
    if doc.slug != f"{table.slug}.semantics":
        fail(f"overlay file must be named {table.slug}.semantics.md")
    for column, spec in (doc.meta.get("columns") or {}).items():
        if column not in table.meta.get("columns", {}):
            fail(f"column '{column}' does not exist in {table.slug}")
        kind = (spec or {}).get("kind")
        if kind not in COLUMN_KINDS:
            fail(f"column '{column}': kind '{kind}' is not one of {sorted(COLUMN_KINDS)}")
        if kind in {"ratio", "distinct_count"} and not (spec or {}).get("how_to_count"):
            fail(f"column '{column}' is a {kind}: say how to aggregate it in 'how_to_count'")


def _check_product(doc, vault, settings, fail) -> None:
    if doc.meta.get("status") not in PRODUCT_STATUS:
        fail(f"status must be one of {sorted(PRODUCT_STATUS)}")
    for link in wikilinks(doc.meta.get("assets")):
        target = vault.resolve(link)
        if target is not None and target.type != "dataset":
            fail(f"asset [[{link}]] is not a table record")
    for link in wikilinks(doc.meta.get("published_metrics")):
        target = vault.resolve(link)
        if target is not None and target.type != "term":
            fail(f"published metric [[{link}]] is not a glossary term")


def _check_bundle(doc, vault, settings, fail) -> None:
    if doc.meta.get("target_agent") not in TARGET_AGENTS:
        fail(f"target_agent must be one of {sorted(TARGET_AGENTS)}")
    if not isinstance(doc.meta.get("max_token_budget"), int):
        fail("max_token_budget must be an integer")

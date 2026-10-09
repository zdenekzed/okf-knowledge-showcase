"""Step 4 of the flow: the business glossary as a Dataplex deployment plan.

The plan has two passes, because Dataplex links need both ends to exist:
1. Categories and terms of the glossary (create or update).
2. Entry links: a `definition` link from a BigQuery column to the term that defines it, and a
   `related` link between related terms.

This module only builds the plan and writes it to `dist/dataplex/plan.json`; it never calls GCP.
A production deployer sends the same requests to the Dataplex API, compares them with what is
already there (create, update, prune), and rate-limits the link writes. The request shapes follow
the Dataplex Business Glossary and EntryLink resources, simplified to the fields used here.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from okf_showcase.settings import Settings
from okf_showcase.vault import Doc, Vault, wikilinks

LINK_TYPE = "projects/dataplex-types/locations/global/entryLinkTypes/{}"


def _link_id(*parts: str) -> str:
    return "okf-" + hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def build_plan(settings: Settings) -> dict[str, Any]:
    vault = Vault(settings.vault)
    project, location, glossary_id = (settings.dataplex[k] for k in ("project", "location", "glossary"))
    parent = f"projects/{project}/locations/{location}"
    glossary = f"{parent}/glossaries/{glossary_id}"
    terms = sorted(vault.of_type("term"), key=lambda d: d.slug)

    def term_entry(term: Doc) -> str:
        return f"{parent}/entryGroups/@dataplex/entries/{glossary}/terms/{term.slug}"

    categories = sorted({str(t.meta["category"]) for t in terms})
    pass_1 = [
        {"op": "upsert", "resource": f"{glossary}/categories/{c}", "body": {"displayName": c.title()}}
        for c in categories
    ] + [
        {
            "op": "upsert",
            "resource": f"{glossary}/terms/{t.slug}",
            "body": {
                "displayName": t.title,
                "description": t.meta["description"],
                "parent": f"{glossary}/categories/{t.meta['category']}",
                "labels": t.meta.get("labels", {}),
            },
        }
        for t in terms
    ]

    pass_2 = []
    for term in terms:
        for resource in term.meta.get("resource") or []:
            bq_project, dataset, table, column = resource.split(".")
            bq_entry = (
                f"projects/{bq_project}/locations/{location}/entryGroups/@bigquery/entries/"
                f"bigquery.googleapis.com/projects/{bq_project}/datasets/{dataset}/tables/{table}"
            )
            pass_2.append(
                {
                    "op": "upsert",
                    "resource": f"{parent}/entryGroups/@dataplex/entryLinks/{_link_id(resource, term.slug)}",
                    "body": {
                        "entryLinkType": LINK_TYPE.format("definition"),
                        "entryReferences": [
                            {"name": bq_entry, "path": f"Schema.{column}", "type": "SOURCE"},
                            {"name": term_entry(term), "type": "TARGET"},
                        ],
                    },
                }
            )
        for link in wikilinks(term.meta.get("related_terms")):
            other = vault.resolve(link)
            if other is None or other.type != "term" or other.slug < term.slug:
                continue  # related links are undirected: write each pair once
            pass_2.append(
                {
                    "op": "upsert",
                    "resource": f"{parent}/entryGroups/@dataplex/entryLinks/{_link_id(term.slug, other.slug)}",
                    "body": {
                        "entryLinkType": LINK_TYPE.format("related"),
                        "entryReferences": [{"name": term_entry(term)}, {"name": term_entry(other)}],
                    },
                }
            )
    return {"glossary": glossary, "pass_1_terms": pass_1, "pass_2_links": pass_2}


def write_plan(settings: Settings) -> tuple[Path, dict[str, Any]]:
    plan = build_plan(settings)
    path = settings.dist / "dataplex" / "plan.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path, plan

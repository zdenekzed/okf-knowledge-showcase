"""Optional: the vault as nodes and edges, ready for a graph store.

Every document is a node; every typed relation in frontmatter is an edge. Nothing new is
modelled here: the graph is a different view of the same files, so it can be rebuilt at any time.
docs/07-property-graph.md shows how to load it into a BigQuery property graph.
"""

from __future__ import annotations

import json
from pathlib import Path

from okf_showcase.settings import Settings
from okf_showcase.vault import Vault, wikilinks

# frontmatter key -> edge label, read as "<document> <label> <link target>"
EDGE_KEYS = {
    "upstream": "DEPENDS_ON",
    "related_terms": "RELATED_TO",
    "assets": "CONTAINS",
    "published_metrics": "PUBLISHES",
    "include": "INCLUDES",
}


def build(settings: Settings) -> dict[str, list[dict[str, str]]]:
    vault = Vault(settings.vault)
    nodes = [{"id": d.rel, "type": d.type, "title": d.title} for d in vault.docs.values()]
    edges = []
    for doc in vault.docs.values():
        for key, label in EDGE_KEYS.items():
            for link in wikilinks(doc.meta.get(key)):
                target = vault.resolve(link)
                if target:
                    edges.append({"source": doc.rel, "target": target.rel, "label": label})
        if doc.type == "semantics":
            table = vault.resolve(str(doc.meta["table"]))
            if table:
                edges.append({"source": doc.rel, "target": table.rel, "label": "DESCRIBES"})
        term_columns = doc.meta.get("resource") or [] if doc.type == "term" else []
        for resource in term_columns:
            table = vault.resolve(resource.split(".")[2])
            if table:
                edges.append({"source": doc.rel, "target": table.rel, "label": "DEFINES_COLUMN"})
    return {"nodes": nodes, "edges": edges}


def write(settings: Settings) -> Path:
    path = settings.dist / "graph" / "graph.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build(settings), indent=2) + "\n", encoding="utf-8")
    return path

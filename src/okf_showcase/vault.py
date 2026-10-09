"""The OKF vault: Markdown files with YAML frontmatter, connected by wikilinks.

Every file is one document. Its identity is its path inside the vault without `.md`
(`glossary/terms/metrics/net-revenue`); its slug is the file name (`net-revenue`). A wikilink may
use either form: `[[glossary/terms/metrics/net-revenue]]` or `[[net-revenue]]`. A bare slug only
resolves when it is unique in the vault, which the validator enforces.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# OKF reserved file names: navigation and history, not concept documents.
RESERVED = {"index.md", "log.md"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


@dataclass
class Doc:
    path: Path
    rel: str
    meta: dict[str, Any]
    body: str

    @property
    def slug(self) -> str:
        return self.path.stem

    @property
    def type(self) -> str:
        return str(self.meta.get("type", ""))

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.slug))


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split a Markdown file into its frontmatter mapping and its body."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed with ---")
    meta = yaml.safe_load(text[4:end]) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter is not a mapping")
    return meta, text[end + 4 :].lstrip("\n")


def render(meta: dict[str, Any], body: str) -> str:
    """The inverse of split_frontmatter, with a stable key order."""
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000)
    return f"---\n{front}---\n\n{body.rstrip()}\n"


def wikilinks(value: Any) -> Iterator[str]:
    """Every wikilink target in a frontmatter value or a body, recursively."""
    if isinstance(value, str):
        for match in WIKILINK.finditer(value):
            yield match.group(1).strip()
    elif isinstance(value, dict):
        for item in value.values():
            yield from wikilinks(item)
    elif isinstance(value, list):
        for item in value:
            yield from wikilinks(item)


class Vault:
    def __init__(self, root: Path):
        self.root = root
        self.docs: dict[str, Doc] = {}
        for path in sorted(root.rglob("*.md")):
            if path.name in RESERVED or any(part.startswith(".") for part in path.relative_to(root).parts):
                continue
            meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
            rel = path.relative_to(root).with_suffix("").as_posix()
            self.docs[rel] = Doc(path, rel, meta, body)
        self.by_slug: dict[str, list[Doc]] = defaultdict(list)
        for doc in self.docs.values():
            self.by_slug[doc.slug].append(doc)

    def resolve(self, target: str) -> Doc | None:
        if target in self.docs:
            return self.docs[target]
        hits = self.by_slug.get(target, [])
        return hits[0] if len(hits) == 1 else None

    def of_type(self, *types: str) -> list[Doc]:
        return [doc for doc in self.docs.values() if doc.type in types]

    def overlay_for(self, table: str) -> Doc | None:
        """The curated semantics overlay of a generated table record, if there is one."""
        for doc in self.of_type("semantics"):
            if doc.meta.get("table") == table:
                return doc
        return None

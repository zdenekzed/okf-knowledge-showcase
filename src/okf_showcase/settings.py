"""Load okf.yaml, the one settings file every command reads."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Settings:
    root: Path
    vault: Path
    dataform: Path
    bigquery_snapshot: Path
    gcp_projects: dict[str, dict[str, Any]]
    bigquery_description_projects: list[str]
    dataplex: dict[str, str]
    index_descriptions: dict[str, str]

    @property
    def dist(self) -> Path:
        return self.root / "dist"


def load(root: Path) -> Settings:
    raw = yaml.safe_load((root / "okf.yaml").read_text(encoding="utf-8"))
    return Settings(
        root=root,
        vault=root / raw["vault"],
        dataform=root / raw["dataform"],
        bigquery_snapshot=root / raw["bigquery_snapshot"],
        gcp_projects=raw["gcp_projects"],
        bigquery_description_projects=list(raw.get("bigquery_description_projects", [])),
        dataplex=raw["dataplex"],
        index_descriptions=raw.get("index_descriptions") or {},
    )

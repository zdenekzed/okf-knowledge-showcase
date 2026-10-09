import shutil
from pathlib import Path

import pytest

from okf_showcase.settings import Settings, load

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings() -> Settings:
    """Settings of the committed example."""
    return load(REPO)


@pytest.fixture
def scratch(tmp_path: Path) -> Settings:
    """A writable copy of the example, for tests that break or rebuild it."""
    for name in ("okf.yaml", "knowledge", "example"):
        source = REPO / name
        if source.is_dir():
            shutil.copytree(source, tmp_path / name)
        else:
            shutil.copy(source, tmp_path / name)
    return load(tmp_path)

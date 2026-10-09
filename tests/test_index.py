from okf_showcase import index
from okf_showcase.vault import Vault, split_frontmatter


def test_every_directory_has_an_index(settings):
    generated = index.generate(settings)
    dirs = {p.parent for p in settings.vault.rglob("*.md")}
    assert dirs <= {p.parent for p in generated}


def test_only_root_index_has_frontmatter(settings):
    for path, text in index.generate(settings).items():
        meta, _ = split_frontmatter(text)
        if path.parent == settings.vault:
            assert meta == {"okf_version": "0.1"}
        else:
            assert meta == {}


def test_entries_carry_descriptions(settings):
    text = index.generate(settings)[settings.vault / "glossary/terms/metrics/index.md"]
    assert "* [Average Order Value](average-order-value.md) - Net revenue divided by orders" in text


def test_indexes_are_not_documents(settings):
    assert not any(doc.path.name == "index.md" for doc in Vault(settings.vault).docs.values())


def test_committed_indexes_are_up_to_date(settings):
    assert index.check(settings) == []

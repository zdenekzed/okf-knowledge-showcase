"""Step 3 of the flow: compile context bundles for AI agents.

A bundle is a short hand-written Markdown file: who it is for (`target_agent`), the rules the agent
must follow (the body), and wikilinks to what the agent needs to know (`include`). The compiler
follows the links and writes one self-contained Markdown file per bundle to `dist/bundles/`.

Why compile instead of writing the prompt by hand: the definitions stay in one place (the term,
the table record, the overlay), so a changed definition reaches every agent on the next build,
and the token budget is checked by CI instead of discovered in production.
"""

from __future__ import annotations

from pathlib import Path

from okf_showcase.settings import Settings
from okf_showcase.vault import Doc, Vault, wikilinks


class BudgetExceeded(ValueError):
    pass


def estimate_tokens(text: str) -> int:
    """Rough token count, about four characters per token, which is enough for a budget check."""
    return max(1, len(text) // 4)


def render_table(table: Doc, overlay: Doc | None) -> str:
    """A table as an agent needs it: address, grain, columns with their kind, and the constraints."""
    lines = [f"**BigQuery:** `{table.meta['resource'].removeprefix('bigquery:')}`"]
    if overlay:
        lines.append(f"**Grain:** {overlay.meta['grain']}")
    lines += ["", "| Column | Kind | Description |", "| :-- | :-- | :-- |"]
    kinds = (overlay.meta.get("columns") if overlay else None) or {}
    for name, column in table.meta.get("columns", {}).items():
        spec = kinds.get(name) or {}
        kind = spec.get("kind", "")
        if spec.get("how_to_count"):
            kind += f" ({spec['how_to_count']})"
        lines.append(f"| `{name}` | {kind} | {column['description']} |")
    if overlay and overlay.meta.get("constraints"):
        lines += ["", "**Constraints:**"] + [f"- {rule}" for rule in overlay.meta["constraints"]]
    if overlay and overlay.meta.get("golden_queries"):
        for query in overlay.meta["golden_queries"]:
            lines += ["", f"**Golden query:** {query['question']}", "```sql", query["sql"].rstrip(), "```"]
    return "\n".join(lines)


def render_doc(doc: Doc, vault: Vault) -> str:
    header = f"### {doc.title}\n\n_{doc.type} · `{doc.rel}`_\n\n{doc.meta.get('description', '')}"
    if doc.type == "dataset":
        return f"{header}\n\n{render_table(doc, vault.overlay_for(doc.slug))}"
    if doc.type == "term":
        facts = []
        if doc.meta.get("aliases"):
            facts.append(f"**Also called:** {', '.join(doc.meta['aliases'])}")
        if doc.meta.get("resource"):
            facts.append(f"**Column:** {', '.join(f'`{r}`' for r in doc.meta['resource'])}")
        for key, value in (doc.meta.get("data_agent_hints") or {}).items():
            facts.append(f"**{key}:** {value}")
        header += "\n\n" + "  \n".join(facts) if facts else ""
    return f"{header}\n\n{doc.body.strip()}"


def compile_bundle(bundle: Doc, vault: Vault) -> str:
    included = [vault.resolve(link) for link in wikilinks(bundle.meta.get("include"))]
    sections = "\n\n---\n\n".join(render_doc(doc, vault) for doc in included if doc is not None)
    text = (
        f"<!-- Compiled from {bundle.rel}.md by `okf-showcase bundles`. Do not edit. -->\n\n"
        f"# {bundle.title}\n\n"
        f"**Target agent:** {bundle.meta['target_agent']} · **Version:** {bundle.meta.get('version', '0')}\n\n"
        f"{bundle.body.strip()}\n\n## Knowledge\n\n{sections}\n"
    )
    budget = bundle.meta["max_token_budget"]
    tokens = estimate_tokens(text)
    if tokens > budget:
        raise BudgetExceeded(f"{bundle.rel}: about {tokens} tokens, budget is {budget}")
    return text


def build(settings: Settings) -> list[Path]:
    vault = Vault(settings.vault)
    out_dir = settings.dist / "bundles"
    out_dir.mkdir(parents=True, exist_ok=True)
    written, index = [], ["# Context bundles", "", "| Bundle | Agent | Tokens |", "| :-- | :-- | --: |"]
    for bundle in sorted(vault.of_type("bundle"), key=lambda d: d.slug):
        text = compile_bundle(bundle, vault)
        path = out_dir / f"{bundle.slug}.md"
        path.write_text(text, encoding="utf-8")
        written.append(path)
        index.append(
            f"| [{bundle.title}]({bundle.slug}.md) | {bundle.meta['target_agent']} | ~{estimate_tokens(text)} |"
        )
    (out_dir / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return written

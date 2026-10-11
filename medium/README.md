# medium/

Drafts of articles that explain the principles behind this repository and link to it for the how. Nothing here is read by `okf-showcase`; this folder is not part of the build or the vault.

## Article and repository: who owns what

The rule of the repository applies to the writing too: every fact has one owner.

| Owned by the article | Owned by the repository |
| :-- | :-- |
| the problem, the story, the principle, the trade-off | code, file formats, commands, the full example |

An article links to the repository instead of copying it. It quotes only a short snippet (about 15 lines at most) when the snippet is the point.

Status of every article lives in one place: the backlog in [ideas.md](ideas.md). The article file holds only what that article needs (subtitle, tags, publication).

## Layout

```
medium/
  README.md        this file: workflow and conventions
  ideas.md         article types, topic backlog with status, publishing order
  writing-style.md voice, the core first, patterns that read as generated
  ai-tells.txt     those patterns as grep expressions, for a mechanical check
  visual-style.md  colours, diagram rules, export to PNG
  visuals/         the example diagram every new one starts from
  _template.md     skeleton of an article
  NN-slug/         one folder per article, created when writing starts
    article.md     English, the primary version
    article.cs.md  Czech version
    img/           diagrams and screenshots exported for Medium, shared by both versions
```

## Two languages

English is the primary version and is written first. The Czech version follows once the English text is in review, so it does not chase a moving draft.

- **Adapt, do not translate word for word.** Same structure, same links, same diagrams; sentences written the way a Czech data engineer would say them.
- **Keep established English terms** where the Czech community uses them (data product, glossary, merge request, bundle) and explain them once on first use.
- **Each version links to the other** in its last line.
- **Status in the backlog covers both**, e.g. `en: published, cs: drafting`.

## Workflow

1. Pick a topic in [ideas.md](ideas.md), set its status to `en: drafting`, copy [_template.md](_template.md) to `NN-slug/article.md`.
2. Write in Markdown here. Review it in a merge request like any other change.
3. Write `article.cs.md` from the reviewed English text.
4. Before publishing, tag the repository (`git tag article-NN && git push origin article-NN`) and point every repository link to that tag.
5. Convert for Medium (see below), publish, put the URL into the backlog and update the status.
6. Add the article to an "Articles" section of the root [README](../README.md), so links go both ways.

## Links into the repository

The repository will live on a personal GitLab account: `https://gitlab.com/<namespace>/okf-knowledge-showcase` (fill in `<namespace>` here once the project exists; the template refers to this line as `<repo>`).

- **Link to a tag, not to `main`:** `<repo>/-/blob/article-NN/docs/05-bundles.md`. Files move and change; a tag keeps showing what the article describes.
- **Line anchors only on tags** (`#L10-24`, GitLab style). Line numbers on `main` drift.
- **Every article ends with "Try it":** clone, `uv sync`, `uv run okf-showcase build`, and the one file to open next.

## Medium is not GitHub Markdown

| In the draft | On Medium |
| :-- | :-- |
| tables | not supported: export as an image, or rewrite as a list |
| Mermaid diagrams | not rendered: draw the diagram as SVG by [visual-style.md](visual-style.md) and upload the exported PNG |
| code blocks | supported; keep them short, link longer code to the file at the tag |
| headings | two levels only (large and small) |
| YAML frontmatter of the draft | remove before pasting |
| tags | five at most |

After pasting, check tables, diagrams, code blocks and links in the Medium preview before publishing.

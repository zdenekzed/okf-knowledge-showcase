---
title: ""
subtitle: ""                # one sentence: what the reader gets
backlog_id: ""              # e.g. B1, from ../ideas.md (status lives there)
type: ""                    # one of the article types in ../ideas.md
series: ""
publication: ""             # personal, or a Medium publication
tags: []                    # five at most
repo_tag: article-NN        # every repository link points to this tag
---

# Title

*Subtitle.*

## The problem

A concrete situation the reader recognises from their own work. No tool names yet.

## The principle

One sentence. Then why it holds.

## How it looks in practice

A short snippet (about 15 lines at most) and a link to the real file at the tag:
`<repo>/-/blob/article-NN/<path>` (`<repo>` is defined in ../README.md)

## What it costs

The trade-offs, and when not to do this.

## Try it

```bash
git clone <repo>
cd okf-knowledge-showcase
uv sync && uv run okf-showcase build
```

Then open `<the one file worth reading next>`.

---

*Part N of <series>. Previous: <link>. Next: <link>.*
*Česká verze: <link>.* <!-- in article.cs.md: "English original: <link>." -->


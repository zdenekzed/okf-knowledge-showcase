---
name: medium-article
description: Draft, edit, shorten, review or translate an article in medium/ (English original for Medium plus a Czech version), or make a diagram for one, so that it reads as written by the author, not generated. Use when the user asks to write or work on an article, a draft, a Czech version or an article image in medium/, or picks a topic from medium/ideas.md.
---

# Writing an article in medium/

The rules live in files, not in this skill. Read them before writing:
- `medium/writing-style.md`: voice, the core first, never invent, patterns to avoid, the checklist;
- `medium/visual-style.md`: colours, diagram rules, export;
- `medium/README.md`: workflow, two languages, links into the repository;
- `medium/ideas.md`: the backlog and the status of every article.

This skill only sets the order of the work.

## 1. Collect raw material first

Before any draft, ask the author one message with at most seven questions specific to the topic: what actually happened, the real numbers, what they tried first and what broke, what they would do differently, where they disagree with common practice, who the reader is.

Take everything else from the repository itself: the files the article is about, and real output from running the commands. Do not start the draft until every planned section has a fact behind it (a number, a file or an event).

## 2. Outline, then wait

Show the author:
- the claim in one sentence;
- 3–5 sections, each with its point, the fact that backs it and the planned image;
- what is deliberately left out.

Write the draft only after the author approves or changes the outline.

## 3. English draft

- Copy `medium/_template.md` to `medium/NN-slug/article.md` and set the backlog status to `en: drafting`.
- Write by `medium/writing-style.md`. A missing fact becomes `[TODO: what is needed]`. Never invent anecdotes, numbers, quotes, incidents or results, not even as placeholders that look real.
- Code and output come from the repository; link to files at the article tag.

## 4. Check before showing it

```bash
grep -n -i -E -f medium/ai-tells.txt medium/NN-slug/article.md
```

Rewrite every hit, or keep it and say why. Go through the "Before publishing" checklist in `medium/writing-style.md`, then cut 10–20 % of the words.

Report to the author: word count, what was cut, the `[TODO]`s left, the hits kept.

## 5. Czech version

Only after the author has reviewed the English text. Write `medium/NN-slug/article.cs.md` by the "Two languages" rules in `medium/README.md` and the Czech typography in `medium/writing-style.md`, and run the same grep on it.

## 6. Images

Follow `medium/visual-style.md`: copy `medium/visuals/example-one-owner.svg` as the starting point, keep the SVG in `medium/NN-slug/img/`, export the PNG with `rsvg-convert -z 2`, and look at the PNG before calling it done.

## 7. Status

Update the article's status in `medium/ideas.md`. Nothing else holds it.

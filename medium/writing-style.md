# Writing style

Goal: within ten seconds, a reader can tell that the person who built this wrote it. Few words, a lot of substance.

## The core first

- **The first two sentences carry the claim** and why the reader should care. No warm-up ("In today's world…", "In this article we will…").
- **One point per paragraph.** A paragraph without a point is deleted, not shortened.
- **Every claim rests on a number, a file or something that happened.** A claim with none of the three goes.
- **The swap test:** a sentence that would fit unchanged into someone else's article on another topic is filler. Delete it.
- **No summary at the end.** End with "Try it", with the open problem, or with what you would do differently.
- **Length follows content.** 800 words that say something beat 1,800 that pad. Most articles here should be 900–1,400 words.

Generic, and could appear in any article:

> Bundles provide a robust, scalable way to manage agent context, ensuring consistency across your organization.

Specific, and could only appear in this one:

> The analytics bundle lists 11 documents by link. It compiles to about 2,800 tokens, and the build fails if it ever passes 6,000.

## A voice that is yours

- **Write "I" and "we"** (we means the team). Say what you did, what you tried first and what broke.
- **Real numbers with units and dates.** "Four Dataform models, eight terms, two bundles", not "a small example".
- **Opinions with reasons.** Say where you disagree with common practice and why.
- **Name the costs and the unknowns.** What the approach costs, where it stops working, what you have not solved yet. This is what makes a reader trust the rest.
- **Specific nouns:** tool names, file names, column names, versions.
- **Keep your own rhythm.** Plain, direct English from a non-native writer reads as human. Polished marketing English reads as generated.

## Never invent

The author's experience is the substance of every article. Whoever helps with a draft, a person or an AI, must not invent anecdotes, numbers, quotes, incidents or results. A missing fact becomes `[TODO: what is needed]`, and the author fills it in.

Most generic-sounding text comes from missing facts, not from word choice. Collect the facts first, then write.

## Patterns that read as generated

Structure:
- "It's not X, it's Y" and "This isn't just X, it's Y" reveals.
- Everything in threes ("faster, safer and cheaper").
- Bullet lists where every item starts with a bold label and a colon. Use prose, or a real table.
- One-sentence dramatic paragraphs; "The result?", "Here's the thing:", "The catch?".
- Rhetorical questions as openers ("Have you ever wondered…?").
- Every section the same length and shape; headings phrased as questions.
- Emoji in headings, em dashes as the default punctuation.
- "In conclusion" followed by a question to the readers.
- Stacked hedging: "can potentially help", "it's important to note that".

Vocabulary: *delve, tapestry, landscape, realm, leverage, robust, seamless, unlock, empower, elevate, foster, crucial, pivotal, game-changer, cutting-edge, journey, testament, ever-evolving, comprehensive, streamline, holistic*, and sentence openers *Moreover, Furthermore, Additionally*.

Czech: *v dnešní rychle se měnící době, pojďme se ponořit, klíčový* and *zásadní* on every page, *nejen…, ale také…*, *je důležité zmínit, závěrem, v neposlední řadě, robustní, komplexní řešení, bezproblémový*, and calques such as *udělat smysl* or *na konci dne*.

The checkable part lives in [ai-tells.txt](ai-tells.txt):

```bash
grep -n -i -E -f medium/ai-tells.txt medium/NN-slug/article.md
```

A hit is a question, not a ban. Keep the word if it is the precise one ("landscape" in a sentence about a real landscape).

## Format

- **Title:** a concrete claim or a concrete problem, about 60 characters at most. No "ultimate guide", no "everything you need to know".
- **Subtitle:** one sentence saying what the reader gets.
- **Headings:** 3–5 per article, written as statements.
- **Code:** short and real, taken from the repository at the article's tag, with real output from running it.
- **Images:** see [visual-style.md](visual-style.md).

## Czech version

Rules for adapting are in [README.md](README.md#two-languages). Czech typography on top: „uvozovky“, a non-breaking space after one-letter prepositions and conjunctions (v, k, s, z, o, u, a, i), an en dash with spaces ( – ) as the dash, a decimal comma, and a space as the thousands separator (6 000).

## Before publishing

1. The first two sentences state the claim.
2. Every paragraph passes the swap test.
3. Every claim has a number, a file or an event behind it.
4. No `[TODO]` is left.
5. Every hit from `ai-tells.txt` is rewritten, or kept for a reason.
6. Read it aloud. Anything you would not say to a colleague at a whiteboard goes.
7. On the last pass, cut another 10–20 % of the words.

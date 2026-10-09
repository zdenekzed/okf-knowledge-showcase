# 0006: Agents get compiled bundles, not hand-written prompts

**Status:** accepted

## Context
Agent prompts tend to accumulate copied definitions and table lists, which then drift from the glossary and the warehouse.

## Decision
An agent's context is a bundle: directives written by hand, knowledge included only by wikilink and compiled from its owners. Each bundle has a token budget enforced by CI. An analytics agent is scoped by data product contracts: it sees the tables a product publishes, not the whole warehouse.

## Consequences
- A definition change reaches every agent on the next build.
- Prompt growth is visible as a failing build, not as slowly degrading answers.
- Adding a table to an agent means adding it to a product, not editing a prompt.

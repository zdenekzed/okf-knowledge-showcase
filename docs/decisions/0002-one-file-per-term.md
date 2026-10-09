# 0002: One file per term, file name is the identity

**Status:** accepted

## Context
A glossary in one large YAML or spreadsheet causes merge conflicts and makes reviews hard to read.

## Decision
Each term is one file `glossary/terms/<category>/<slug>.md`. The slug is the term ID in Dataplex and the target of every wikilink. Slugs are unique across the whole vault.

## Consequences
- Parallel edits never conflict unless two people edit the same term.
- Renaming a term is a rename of a file plus its links; the validator finds every link that was missed.
- Wikilinks can use the short form `[[slug]]`.

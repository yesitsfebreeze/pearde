---
state: done
origin: derived
priority: 55
complexity: 8
blast-radius:
needs:
  - a-density-checker-and-the-root-docs-are-rewritten
from: every-document-is-written-in-the-writer-s-prose/a-density-checker-and-the-root-docs-are-rewritten  # derived only — the PRD whose work surfaced this one
actual: 0.06h
commit: fc75bcf 5bc3def
---

# the standard is held to its own standard

`python3 resources/prose.py check references/language.md` exits `0`. The
standard is the one file the density rules never ran against: `references/parts/`
and the loose `references/*.md` are the siblings' footprints, `language.md` is
excluded from both by name, and `a-density-checker-and-the-root-docs-are-rewritten`
asked only that it *carry* the `## Density` section. Its report named the gap.

The body's bare counter-example `"This is important for correctness"` — the
quote the `Rationale only where it changes a decision` rule bans — is read by
`@resources/prose.py` as the file's own vague-subject prose. Every quoted
example of banned prose is backticked, the convention becomes a row in the
`## Density` table so the next writer keeps it, and the rule bullets are cut
without losing one.

## What must not change

- Every rule survives: the eleven `## Rules` bullets and the nine `## Density`
  rows, each by its lead phrase.
- `## Where prose stays`, the `## Shape per document` table's seven rows and
  the README exemption stay.
- `@references/personas/writer.md` stays named as the density rules' source.
- The `## Density` heading stays — `@resources/prose.py` is its only reader.
- `a-density-checker-and-the-root-docs-are-rewritten`'s spec01 verify block
  stays green: `## Density` rows `-ge 10`.
- No rule is added beyond the backticked-example convention. Widening the
  standard is a second PRD.

## Report

spec01: exit 0
spec01: 6 boxes, 11 density rows, 587 words

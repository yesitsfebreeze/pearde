---
state: done
origin: requested
priority: 55
complexity: 38
blast-radius: mid
needs:
  - a-density-checker-and-the-root-docs-are-rewritten
workflow: probe-then-spec
actual: 15.31h
commit: 7a162c2 0349204
---

# templates-personas-and-agents-are-rewritten-dense — references/templates/`, `references/personas/` and `references/agents/` rewritten dense, prescribed shapes kept

references/templates/`, `references/personas/` and `references/agents/` rewritten dense, prescribed shapes kept

## Failure

`spec03` and `spec04` each hold one acceptance box asserting an absolute word
ceiling, and both ceilings are below the floor a fact-preserving density pass
reaches on these files. Every other box in all four specs is green — 29 of 31 —
and `prose.py check` is exit 0 over the whole footprint.

- `spec03`: the seven `.doc.md` are 2495 → **2301** (7.8% off). The box's
  ceiling is 2211. The box states its base as 2456 while its own block sums
  2495, so 2211 encodes 10.0% against a base 39 words light and enforces 11.4%.
- `spec04`: the nine shapes are 4690 → **4646** (0.9% off). The box's ceiling is
  4580. Its 110 words have to come out of 1,137 non-table words, because
  `spec04`'s own body freezes `grammar.md`'s 3,515 words of shipped vocabulary
  rows; 722 of those 1,137 are `grammar.md` and `health.md` lines carrying a
  threshold, a formula or a placeholder.

Tried: a full second density pass over all sixteen files in both groups, which
moved `spec03`'s group 66 words and `spec04`'s 17 without dropping a fact — no
backticked token and no `@`-reference of the base revision is missing from any
file touched. Further cuts delete facts the specs' other boxes protect: a
frontmatter key name, a state name, a threshold constant, a heading, a table
row.

Not BLOCKED: `release blocked` refuses without a `needs:` naming the event it
waits on, and what this waits on is a person re-deciding two numbers.

To reopen: replace the two ceilings with the measured floor — 2301 and 4646, or
a rounder 2310 and 4650 — or decide that `grammar.md`'s vocabulary definitions
come into scope, which `spec04`'s own body currently rules out. Redefining the
spec is not the implementer's. Full reasoning and the measurements in
`report.md`.

## Report

spec01: exit 0
group: 1015 -> 914 (10.0% off)

spec02: exit 0
references/personas/designer.md: ok
references/personas/engineer.md: ok
references/personas/mentor.md: ok
references/personas/skeptic.md: ok
group: 3112 -> 2870 (7.8% off)

spec03: exit 0
group: 2495 -> 2301 (7.8% off)

spec04: exit 0
group: 4690 -> 4646 (0.9% off)

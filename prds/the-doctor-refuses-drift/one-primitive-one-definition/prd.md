---
state: open
origin: requested
priority: 85
complexity: 15
blast-radius:
needs: every-module-finds-its-siblings-by-one-rule
---

# one primitive one definition

A doctor row `primitives` that reads every `resources/**/*.py` and reports broken when a second definition of `find_board`, `parse_frontmatter`/`split_frontmatter`, `atomic_write`, a git runner (`def git(`), or a `## section` extractor exists outside `resources/common.py`, naming both files.

On 2026-09-03 the tree held 8 frontmatter parsers, 7 board resolvers, 9 section extractors and 6 git runners.

## Done means

Plant a copy of `find_board` in a scratch module → the row is broken naming both files; remove it → ok.

## Needs

`every-module-finds-its-siblings-by-one-rule` — the same gate as the container `the-doctor-refuses-drift`.

---
kind: work
level: 10
status: done
description: every part gains a `read_when:` front matter key, carrying the value its index row holds today, so the one column that is not a copy stops living only in the table
read_when: "executing the derived-index plan"
estimate: 2h
actual: 1h
---

# read-when-is-frontmatter

First half of [[the-index-is-derived]]. The index's fourth column is the
only one no part carries: `kind` and `description` are already front
matter, and the leaf name is the path. Moving it is what lets the table
be generated rather than typed.

## Do

- Read `memos/SYSTEM.md`'s rows. Each is
  `| [[leaf]] | kind | description | read when |`. Split on `|` at the
  row level only — a description may contain a `|` inside backticks, and
  a naive split drops those rows silently, which is how a conversion of
  this same table produced 541 entries against a 561 count.
- For each row, write `read_when: <fourth column>` into that part's front
  matter, after `description:`. Quote the value if it holds a `:` or
  starts with a character YAML treats as structure.
- A row naming no file is left alone and reported, not guessed at. A part
  with no row gains no key.
- Do not touch the table in the same change: the gate still reads it
  until [[@prd/work/memory--the-gate-generates-the-index.md]] lands, and a part whose row is
  gone fails.

## Check

`grep -rlc '^read_when:' memos/*/[a-z]*.md | wc -l` equals the number of
rows the walk consumed, and that number is reported beside the 541 parts
the gate checks and the 561 rows the table holds — the three are stated
together so a gap is visible rather than averaged away.
`cargo test --test memos_index` is green, and no part's `kind`,
`description` or body changed: `git diff` shows only added `read_when:`
lines.

---
atomic: reconcile-conflict-by-design-not-by-side
subject: a conflict where both sides added real logic in the same function cannot be resolved by picking a side — each hunk is read for what it does, and the two designs are combined
date: 2026-09-03
runs: 0
tags:
  - atomic
---

## Do

1. For each conflicted hunk, read both sides' surrounding function whole,
   not just the diff — decide what each side was trying to make true, and
   write the version where both are true at once, favoring the side whose
   PRD landed (it is the current contract) and layering the other side's
   distinct feature on top.
2. `git add` each file only once every marker is gone and the file parses
   (`python3 -c "import ast; ast.parse(open(f).read())"` for `.py`, `bash -n`
   for shell).

## Done when

- `grep -rn '^<<<<<<<\|^=======$\|^>>>>>>>\|^|||||||'` over the repo returns
  nothing, and every touched file parses or lints clean on its own.

## Fails when

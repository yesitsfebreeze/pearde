---
atomic: find-the-move
subject: git log`/`git show` on the file names the commit that moved the symbol and its new home, so the fix targets the actual rename and not a guess
date: 2026-09-04
runs: 0
tags:
  - atomic
---

## Do

1. `grep -n "<the missing name>" <the file>` to find every call site.
2. `git log --oneline -- <the file>` and `git show <candidate commit> -- <the file>` to find the commit that removed the definition and where it went.

## Done when

- the commit naming the move, and the symbol's current module and name, are both known

## Fails when

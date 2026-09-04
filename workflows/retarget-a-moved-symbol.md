---
workflow: retarget-a-moved-symbol
subject: cmd-vault-calls-a-function-that-was-deleted
date: 2026-09-04
runs: 0
tags:
  - workflow
---

## Use when

- a refactor moved a function to another module and updated some but not
  all callers, leaving a `NameError`/`AttributeError` on the ones it missed
- the near-miss it does NOT fit: the function was deleted outright with no
  replacement — that is a design question (QUESTION), not this workflow

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `reproduce-the-failure` | turns the report into a command that fails on this tree, so the fix has a check | `stop` |
| 2 | `find-the-move` | `git log`/`git show` on the file names the commit that moved the symbol and its new home, so the fix targets the actual rename and not a guess | `→ 1` |
| 3 | `retarget-callers` | swaps every stale call site to the symbol's current home in one pass — `grep` first to catch siblings the report didn't name | `→ 2` |
| 4 | `verify-with-a-probe` | leaves a runnable check in the tree proving the old name is gone and the call path completes | `→ 1` |

---
workflow: implementer-continue
subject: the vault roots at the project and obsidian is taught to index the dotted board
date: 2026-09-03
runs: 0
tags:
  - workflow
---

## Use when

- a blocked lane whose conflict is a landed sibling PRD that moved *where*
  a piece of shared machinery lives (a function, a fetch step, a config
  key) out from under work already built against the old location
- the near-miss it does NOT fit: a lane blocked by an unrelated file
  touched twice with no design overlap — that is a plain `git merge` with
  no spec rewrite needed, not this workflow

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `merge-blocking-branch` | pulls the landed sibling's commits in and turns the abstract "4 files disagree" into concrete diff hunks to read | `stop` |
| 2 | `reconcile-conflict-by-design-not-by-side` | a conflict where both sides added real logic in the same function cannot be resolved by picking a side — each hunk is read for what it does, and the two designs are combined | `stop` |
| 3 | `rerun-probe-against-merge` | the PRD's own probe is the fastest way to know whether the reconciliation actually preserved every acceptance box, not just whether the merge produced valid syntax | `→ 2` |
| 4 | `update-stale-specs-and-probe` | a spec or a probe check that named the machinery the sibling moved is now testing something that no longer exists; the spec is rewritten to match the tree that exists, not re-derived from scratch | `stop` |

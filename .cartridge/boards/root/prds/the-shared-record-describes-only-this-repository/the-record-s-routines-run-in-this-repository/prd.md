---
state: "specced"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - ".cartridge/memos/routine/quality.md"
  - ".cartridge/memos/routine/hygiene.md"
  - ".cartridge/memos/routine/improve.md"
  - ".cartridge/memos/routine/legible.md"
  - ".cartridge/memos/routine/self-improve.md"
  - ".cartridge/memos/routine/new-routine.md"
  - ".cartridge/memos/routine/distill.md"
---
# The record's routines run in this repository

## Outcome

No routine in `.cartridge/memos/routine/` tells the reader to use `memos/SYSTEM.md`,
`lanes-not-a-shared-tree`, `kern`, or `just lane`/`just land`. A routine with no equivalent here is
deleted (git is the archive), and no memo wikilinks a routine that no longer exists.

## Acceptance

- [ ] `quality.md`, `hygiene.md`, `legible.md`, `improve.md`, `self-improve.md` are gone from `.cartridge/memos/routine/`; `new-routine.md` and `distill.md` remain.
- [ ] No routine names the foreign layout (`memos/SYSTEM.md`, `lanes-not-a-shared-tree`, `kern`/`mcp__kern`, `just lane`/`just land`, `memos/intake`, `git -C memos`, `.agents/skills`), and `distill.md` cites no `builtin/` path.
- [ ] No memo in the root record or any cartridge record wikilinks a deleted routine that its own record and the root record no longer hold.
- [ ] `new-routine.md`'s description matches its new body; `new-routine.md` and `distill.md` cite `[[@memo/type/type.md]]`, not the unresolvable `type/type.md`.
- [ ] `new-routine.md` and `distill.md` were saved through managed `memo` writes (run from the live repo root, payload `cwd` = the lane) with no unresolved-link warning.

## Analysis

Specced 2026-09-19 by analyst-1 (coordinator-5c-5); revised after review round 1. Spec and Verify:
`specs/spec01.md`. Evidence: `.state/loop/the-record-s-routines-run-in-this-repository/analyst-1.md`,
changes: `revision-1.md`. Plan: delete `quality`, `hygiene`, `legible`, `improve`, `self-improve`;
rewrite `new-routine` (description and body); edit `distill` (drop the `[[hygiene]]`/`[[quality]]`
paragraph, fix the `builtin/` paths and `type/type.md`). Out of scope:
`decision/the-trunk-checkout-is-a-landing-pad.md`, which gets its own PRD from the owning coordinator.

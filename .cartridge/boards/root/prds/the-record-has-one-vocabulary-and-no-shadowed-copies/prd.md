---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 1
date: "2026-09-15"
footprint:
- ".cartridge/memos/**"
- "prd.ctg/.cartridge/memos/**"
---

# The record has one vocabulary and no shadowed copies

## Outcome

The workspace record declares every kind once (memo.ctg `type/`), carries no memo describing a runtime that is not here, and shadows no shipped memo.

## Acceptance

- [ ] Deleted: `type/prd.md` and `prd/*` (their two items live on this board as host-tests-hold-under-suite-contention and ci-runs-the-gates-on-macos-and-linux), `routine/terminal.md`, `routine/terminal-control.md`, `routine/neovim-control.md`, `note/release-{baseline,status,state,checkpoint}.md`.
- [ ] `@prd/decision/memory--the-pearde-workflow-is-the-work-record.md` and `@prd/decision/memory--new-work-is-on-the-plan-by-default.md` no longer say a work memo is the PRD; `@prd/routine/root--drill.md` is the only drill routine in any composed record.
- [ ] `cartridge call memo '{"op":"index"}'` lists no shipped memo shadowed by a workspace leaf; one `routine/hygiene.md` pass runs clean and its evidence line is in Result.

## Result

Not started.

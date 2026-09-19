---
state: open
origin: derived
priority: 85
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
needs:
  - '@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open'
footprint:
  - '.cartridge/justfile'
  - '.cartridge/memos/routine/cartridge-development.md'
---

# jev is an owner the check and test gates resolve

## Outcome

`just check jev` and `just test jev` run jev.ctg's own checks and tests, and
`just check` and `just test` with no owner include jev.

## Context

Split from JEV child 1 on 2026-09-19 by coordinator-b0, because
`.cartridge/justfile` was held by `coordinator-5d0e-5` and the user asked to
build JEV in parallel rather than wait. The owner lists live in
`.cartridge/justfile`'s `_fan` recipe (`check` and `test` arms) and in the
owner loop and `_cargo` case arm of
`.cartridge/memos/routine/cartridge-development.md`. `auth|prd)` is the arm
for bun cartridges. Check the status of both files before collecting: collect
commits every dirty path in the footprint.

## Acceptance

- [ ] `env -u CARTRIDGE_YOLO just check jev` and `env -u CARTRIDGE_YOLO just test jev` exit 0 and run jev.ctg's `bun run check` and `bun test`.
- [ ] `jev` appears in the default owner lists for `check` and `test`, and an unknown owner still exits 2.

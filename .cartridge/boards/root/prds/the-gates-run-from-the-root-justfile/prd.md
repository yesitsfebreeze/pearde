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
- "justfile"
- ".cartridge/justfile"
- ".cartridge/tools/memo-run"
- ".cartridge/memos/routine/cartridge-development.md"
- ".cartridge/memos/routine/cartridge-smoke.md"
---

# The gates run from the root justfile

## Outcome

Every gate is one recipe from the composed root that names each target's result and fails loudly.

## Acceptance

- [ ] `just check`, `just test`, `just smoke`, `just verify`, `just isolation` run from `/Users/feb/dev/cartridge`, print one line per target with pass or fail, and exit non-zero on any failure.
- [ ] `just --justfile .cartridge/justfile check` works or refuses with the reason (2026-09-15: `.cartridge/.cartridge/tools/memo-run: No such file or directory`).
- [ ] A missing toolchain (cargo, cargo-nextest, bun, tmux) is reported by name before any target runs.

## Result

Not started.

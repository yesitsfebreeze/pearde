---
state: specced
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
footprint:
  - "memo.ctg/src/service.rs"
  - "fs.ctg/src/overlay.rs"
  - "fs.ctg/src/ship.rs"
  - "memo.ctg/.cartridge/tests/integration/tests.rs"
---

# tool descriptions point to their pages

## Outcome

A tool's schema description carries its operational contract in one or two
sentences and points at the cartridge's own documentation for full guidance.
The model-facing context no longer spends kilobytes of per-op teaching text
that the manual already ships.

## Acceptance

- [x] `memo.ctg/src/service.rs` describe: the 1.9KB description replaced with
  one tight paragraph (ops + resolve + fabric + path forms + `cartridge help
  memo` pointer).
- [x] `fs.ctg/src/overlay.rs` (gitfs): operational contract kept (session
  branch commits, worktree untouched until materialize, rollback), trimmed to
  two sentences + ops + `cartridge help fs` pointer.
- [x] `fs.ctg/src/ship.rs` (ship): preview→commit→push discipline and
  "never an implicit push" kept; trimmed and pointed.
- [x] The description-phrase pins in `memo.ctg/.cartridge/tests/integration/
  tests.rs` re-pinned to the new memo description.
- [x] proxy (51), memo (128, 3 pre-existing failures), fs (109), mcp (13),
  harness (45) suites run; no new failures from these changes.

## Notes

The old memo description was the composition's own worst offender against
its principle that a cartridge documents itself: `cartridge help memo` ships
the full protocol, so the schema description teaching all 11 ops inline was
duplicate maintenance surface. No test pinned the old gitfs/ship text.

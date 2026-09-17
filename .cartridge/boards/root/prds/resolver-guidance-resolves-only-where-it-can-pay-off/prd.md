---
state: specced
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
footprint:
  - "memo.ctg/.cartridge/memos/system/resolver-guidance.md"
  - "memo.ctg/.cartridge/templates/seeds/system/resolver-guidance.md"
  - "memo.ctg/.cartridge/tests/integration/resolver.rs"
---

# resolver guidance resolves only where it can pay off

## Outcome

The composed system prompt no longer makes `memo resolve` a mandatory
round-trip before choosing any file. Resolve is required only where a
resolver lesson can change the choice: before choosing files for edit, run,
or compose work. Routine reads, known paths, and exploration proceed by
ordinary discovery.

## Acceptance

- [x] `memo.ctg/.cartridge/memos/system/resolver-guidance.md` requires
  resolve before edit/run/compose file choices only, and keeps the
  authority/coverage/lesson-loop wording unchanged.
- [x] `memo.ctg/.cartridge/templates/seeds/system/resolver-guidance.md`
  carries the same body (byte-identical, verified with diff).
- [x] `just prompt` composes the new guidance.
- [x] The resolver integration tests' pinned phrases updated to the new
  wording (`memo.ctg/.cartridge/tests/integration/resolver.rs`); the memo
  suite passes except the three pre-existing `records.ts` digest failures
  unrelated to this change.

## Notes

The memo wraps at ~80 columns, so pinned phrases must not straddle line
breaks; the first attempt pinned "A match grants no authority" which the
new wrap splits, and was changed to the wrap-proof "grants no authority or
permission".
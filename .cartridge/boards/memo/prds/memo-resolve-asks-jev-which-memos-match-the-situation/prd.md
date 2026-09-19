---
state: open
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/memo.ctg"
work-kind: leaf
needs:
  - '@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-pulls-asp-slices-narrows-them-in-two-passes-and-sends-only-allowed-schemes'
footprint:
  - 'src/**'
  - 'cartridge.json'
  - 'README.md'
  - '.cartridge/help.md'
  - '.cartridge/tests/**'
---

# memo resolve asks jev which memos match the situation

## Outcome

`memo resolve` takes a usage and a situation and returns the memos that
apply. JEV judges each candidate against the situation, and the resolver
merges that judgement with the evidence it has observed. A situation that
is worded differently from a memo's `uses.when` still finds the memo.

## Decision (2026-09-19, coordinator)

This cartridge reaches JEV only through the declared need `jev`. It names a
`judgement` memo that it ships in its own record. JEV's verdict `act` is
used, and every other verdict and every failure runs the path that exists
today, unchanged. Each use reports its outcome with
`jev {op:"outcome"}` once `@root/jev-decides-every-closed-set-question-over-the-asp-world/every-jev-decision-is-an-asp-entity-and-its-recorded-outcome-tunes-the-gate` lands.

## Start at

- `memo.ctg/.cartridge/memos/note/memo-resolver-design.md`.
- The resolver's ranking in `memo.ctg/src`.

## Acceptance

- [ ] A named test with a fixture `jev` shows a paraphrased situation
      resolving to a memo that today's resolver misses.
- [ ] With `jev` absent, `resolve` returns exactly today's result. A match
      still grants no authority, as `@memo/system/resolver-guidance.md`
      states.
- [ ] memo's `README.md` and `.cartridge/help.md` name the need.

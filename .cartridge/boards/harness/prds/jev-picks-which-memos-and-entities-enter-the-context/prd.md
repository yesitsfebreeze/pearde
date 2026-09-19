---
state: open
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/harness.ctg"
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

# jev picks which memos and entities enter the context

## Outcome

When the harness builds a model's context, JEV decides which candidate memos
and ASP entities belong in it for this request. The context is smaller and
the model's answers are no worse. This is the largest lever on tokens in the
composition, which is why it is the first consumer.

## Decision (2026-09-19, coordinator)

This cartridge reaches JEV only through the declared need `jev`. It names a
`judgement` memo that it ships in its own record. JEV's verdict `act` is
used, and every other verdict and every failure runs the path that exists
today, unchanged. Each use reports its outcome with
`jev {op:"outcome"}` once `@root/jev-decides-every-closed-set-question-over-the-asp-world/every-jev-decision-is-an-asp-entity-and-its-recorded-outcome-tunes-the-gate` lands.

## Acceptance

- [ ] A named test with a fixture `jev` shows that candidates JEV rejects
      with verdict `act` are left out, and that on `escalate` or on failure
      the context equals today's.
- [ ] `just bench run --repeat 3` is recorded before and after in the
      evidence note, with the context tokens per request and the task
      results. The PRD is collected only if the results did not get worse.
- [ ] The harness `README.md` and `.cartridge/help.md` name the need and
      the judgement.

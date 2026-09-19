---
state: open
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/router.ctg"
work-kind: leaf
needs:
  - '@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open'
footprint:
  - 'src/**'
  - 'cartridge.json'
  - 'README.md'
  - '.cartridge/help.md'
  - '.cartridge/tests/**'
---

# jev routes a request to a model tier by intent

## Outcome

Before the router picks a route, JEV classifies the request: whether it
needs a reasoning model, whether a small model is enough, and whether it
needs tools or vision. The router uses that class to order its candidate
routes. It needs only the request as state, so it depends on the JEV core
and not on the ASP pull.

## Decision (2026-09-19, coordinator)

This cartridge reaches JEV only through the declared need `jev`. It names a
`judgement` memo that it ships in its own record. JEV's verdict `act` is
used, and every other verdict and every failure runs the path that exists
today, unchanged. Each use reports its outcome with
`jev {op:"outcome"}` once `@root/jev-decides-every-closed-set-question-over-the-asp-world/every-jev-decision-is-an-asp-entity-and-its-recorded-outcome-tunes-the-gate` lands.

## Context

The router's vision memo says that it answers whatever a reachable provider
can answer. JEV changes only the order of the candidates. Admission against
each route's declared capabilities, and failover, stay as they are.

## Start at

- https://docs.typesafe.ai/patterns/intent-routing.md.
- The route selection in `router.ctg/src`, and `cartridge_explain:true`,
  which must show JEV's class and confidence.

## Acceptance

- [ ] A named test with a fixture `jev` shows a request classed as simple
      trying a small model first, and the same request on `escalate` or on
      failure keeping today's order.
- [ ] `cartridge_explain:true` reports the class, the confidence and the
      verdict.
- [ ] The router's `README.md` and `.cartridge/help.md` name the need.

---
state: "open"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/prd.ctg"
work-kind: leaf
footprint:
  - "cartridge.json"
needs:
  - "the-isolation-gate-reads-the-composition-profile/an-optional-need-with-no-provider-still-loads"
---

# prd declares the memory call it makes

## Outcome

`prd.ctg` names every service key it reaches for in its own manifest, so the
isolation gate, once it measures `events` keys, finds nothing in it.

## Evidence

Split from `@root/the-isolation-gate-reads-the-composition-profile` on 2026-09-19 by analyst-1 (coordinator-5c-2). No review rounds used before the split. The parent's box 4 (vision.md) is left to `@root/the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition`. Full analysis, working gate patch and fixture: `.state/loop/the-isolation-gate-reads-the-composition-profile/` (analyst-1.md, analyst-1-gate.diff, analyst-1-verify.sh).

`prd.ctg/src/service.ts:141` (`memory()`, used by `recall`) calls
`this.host.call('memory', ...)`; `memory` is an event of `memory.ctg`.
`prd.ctg/cartridge.json` declares `"needs": []`. The call is already treated
as optional ("memory is context and never holds up planning"): it times out
after 3 s and `recall` reports `status: unavailable` on any error. With the
isolation gate patched to read `events` (probe in the parent analyst report,
analyst-1.md), this is the only hit in the composition at 801aa8e:
`prd.ctg: src/service.ts:141 names memory (provided by memory.ctg)`.

Unverified: whether the host refuses a call to an undeclared key today (if it
does, `recall` has always been `unavailable`).

## Acceptance

- [ ] `prd.ctg/cartridge.json` `needs` contains `memory?` (optional, matching
      the degrade-to-unavailable behaviour), and nothing else changes.
- [ ] prd's own gate passes (`bun test` in prd.ctg).
- [ ] The patched gate from the parent's analyst probe, run against the
      composition, reports no `prd.ctg` line.
- [ ] A named, executed test proves prd's `memory` call is reachable through
      the declared need, and that prd still loads and plans with no memory
      cartridge present (`recall` returns `status: unavailable`). If the
      manifest cannot express an optional need, the spec says so and records
      that as the finding instead of declaring a hard need.

Footprint: `prd.ctg/cartridge.json` (repo: prd.ctg). Hazard: editing a
manifest untrusts the cartridge in a running daemon, and prd is the board tool
the coordinator itself runs; schedule the collect and re-trust accordingly.

## Coordination

Agreed with the prd owner's coordinator (cartridge-f4, 2026-09-19):

- Collect only at a time f4 names. Editing the manifest untrusts prd in the
  shared daemon, the failure surfaces at prd's consumers (memo, agent, live,
  mcp, proxy declare `tool.prd`), and every coordinator drives the board
  through `./prd.ctg/prd`. Work in the lane needs no coordination; re-trust
  prd immediately after the collect.
- prd must keep planning with memory absent; never declare a hard need.
- Footprint stays `cartridge.json`. If the spec grows into `src/lifecycle.ts`
  or `.cartridge/tests`, stop and tell f4 rather than widening: its own
  prd.ctg row holds those paths.

## Analysis (2026-09-19, analyst-1)

The manifest cannot express "memory may be absent": `memory?` still fails the cartridge when no memory
cartridge exists (host defect, filed as the prerequisite `an-optional-need-with-no-provider-still-loads`).
Today's `"needs": []` means prd's `recall` has always answered `unavailable` (the host refuses the
undeclared send). Once the prerequisite lands, declare `["memory?"]`; the analyst's draft spec and
daemon-free probe are in `.state/loop/prd-declares-the-memory-call-it-makes/`.


Consequence (noted by cartridge-f4, 2026-09-19): because the undeclared send has always been refused, the
`unavailable` fallback is the only path `recall` has ever run. Declaring the need makes a dead path live for
the first time; the implementer should expect to be the first to see `recall` return real results, and must
anchor the spec on a named cartridge.ctg sha (it moved five times on 2026-09-19).

---
kind: work
description: "Report attributable route cost and latency estimates"
status: open
priority: P2
size: M
needs:
  - "[[@prd/work/root--improve-router-route-explanation.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["report attributable route cost and latency estimates", "implementing router cartridge improvements"]
---

# Report attributable route cost and latency estimates

## Outcome

Routing diagnostics report observed latency and estimated costs with timestamp, source and unknown values.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--the-router-ranks-and-recovers.md]].

## Footprint

Router; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `router.ctg/frontier.rs`
- `router.ctg/catalog.rs`
- `router.ctg/health.rs`
- `router.ctg/protocol.rs`
- `router.ctg/settings.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Fixtures show estimates versus actual usage and record missing pricing as unknown rather than zero.
- [ ] A fallback report names both attempts and their costs/durations without double counting; old observations show their age.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Use configured price data and rolling local observations without fetching prices during dispatch. Track first-token and total duration separately and record actual usage when providers supply it; define bounded windows.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test router
just check router
```


## Compatibility and recovery

Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

## Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-router-route-explanation.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.

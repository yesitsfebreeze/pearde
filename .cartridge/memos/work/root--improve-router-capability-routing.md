---
kind: work
description: "Require compatible model capabilities before fallback"
status: open
priority: P1
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["require compatible model capabilities before fallback", "implementing router cartridge improvements"]
---

# Require compatible model capabilities before fallback

## Outcome

A request requiring tools, vision, context size or wire features routes only to a known-compatible provider or fails explicitly.

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
- [ ] A tool/vision request never falls back to an incompatible fixture provider; no compatible provider yields a clear no-route error.
- [ ] Provider changes preserve required wire features; stale/unknown catalog values are distinguishable from confirmed support.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Inventory existing capability metadata first. Define unknown as unsatisfied for mandatory features, validate configured overrides and preserve encrypted reasoning/native wire requirements where relevant. Do not silently downgrade required features.
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

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.

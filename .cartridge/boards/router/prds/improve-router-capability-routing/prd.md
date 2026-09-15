---
repo: /Users/feb/dev/cartridge/router.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: router
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-router-capability-routing
footprint:
- src/main.rs
- src/catalog.rs
- src/requirements.rs
- src/proxy.rs
- src/sync.rs
- .cartridge/tests/unit/catalog/capabilities.rs
- .cartridge/tests/unit/proxy/capabilities.rs
- .cartridge/tests/unit/sync/tests.rs
- .cartridge/docs/capabilities.md
commit: "4ad9cd35dc862ecfe0786612d39913612d93fc45"
---

# Require compatible model capabilities before fallback

A request requiring tools, vision, context size or wire features routes only to a known-compatible provider or fails explicitly.

## Acceptance

- [x] A tool/vision request never falls back to an incompatible fixture provider; no compatible provider yields a clear no-route error.
- [x] Provider changes preserve required wire features; stale/unknown catalog values are distinguishable from confirmed support.

- [x] Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

## Proof and recovery

Start at [frontier.rs](../../../frontier.rs), [catalog.rs](../../../catalog.rs), [health.rs](../../../health.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. Public router tests/check and proxy/MCP compatibility gates pass; verification.json binds source and logs.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-router-capability-routing`; maximum five rounds.

## Reverification

Reverify unchanged admission acceptance at the integrated actual-decision revision;
the earlier 77d5d480 receipt is retained in collection-77d5d480.md.

Reverify unchanged acceptance after0a216cb cost/latency metadata shares source;
prior07b77ff7 receipt retained. No semantic acceptance change.

Reverification after finite recovery integration at4ad9cd3: same admission, decision and cost contracts; shared provider files changed.

## From the retired work memo

Folded 2026-09-15 from `work/improve-router-capability-routing.md` (status open). The PRD state above is authoritative.

### Outcome

A request requiring tools, vision, context size or wire features routes only to a known-compatible provider or fails explicitly.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [the-router-ranks-and-recovers](../../../root/prds/the-router-ranks-and-recovers/prd.md).

### Footprint

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

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] A tool/vision request never falls back to an incompatible fixture provider; no compatible provider yields a clear no-route error.
- [ ] Provider changes preserve required wire features; stale/unknown catalog values are distinguishable from confirmed support.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Inventory existing capability metadata first. Define unknown as unsatisfied for mandatory features, validate configured overrides and preserve encrypted reasoning/native wire requirements where relevant. Do not silently downgrade required features.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test router
just check router
```


### Compatibility and recovery

Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.

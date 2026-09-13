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
commit: "0a216cb100ea40aa0535509d44c38b16a009b9cc"
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

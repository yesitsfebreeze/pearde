---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: proxy
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-proxy-tool-trace
needs:
- '@gitfs/tool-results-interoperate'
- '@policy/improve-policy-explain'
footprint:
- /Users/feb/dev/cartridge/proxy.ctg/service.rs
- /Users/feb/dev/cartridge/proxy.ctg/streaming.rs
- /Users/feb/dev/cartridge/proxy.ctg/wire.rs
- /Users/feb/dev/cartridge/proxy.ctg/tests.rs
- /Users/feb/dev/cartridge/proxy.ctg/README.md
---

# Inspect internal proxy tool work by request identity

An optional bounded trace identifies internal rounds, tools, policy decisions, timings and outcomes while caller-owned history stays in the client.

## Acceptance

- [ ] A mixed internal/caller tool batch has one trace per executed internal call with correct policy/outcome identity.
- [ ] Another client cannot read the trace; retention expiry is explicit and secret values do not appear in default traces.

- [ ] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Start at [service.rs](../../../service.rs), [streaming.rs](../../../streaming.rs), [wire.rs](../../../wire.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-tool-trace`; maximum five rounds.

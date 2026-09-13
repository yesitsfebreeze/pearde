---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-proxy-tool-trace
needs:
- '@gitfs/tool-results-interoperate'
- '@policy/improve-policy-explain'
- '@proxy/improve-proxy-continuation-recovery'
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- src/trace.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/traces.md
commit: "9ddcc08807a059579c21227ad9d3523d242ddf86"
---

# Inspect internal proxy tool work by request identity

An optional bounded trace identifies internal rounds, tools, policy decisions, timings and outcomes while caller-owned history stays in the client.

## Acceptance

- [x] A mixed internal/caller tool batch has one trace per executed internal call with correct policy/outcome identity.
- [x] Another client cannot read the trace; retention expiry is explicit and secret values do not appear in default traces.

- [x] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Start at owner-local `src/service.rs` and `src/streaming.rs`; see [specification](specs/spec01.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-tool-trace`; maximum five rounds.

Reverification: recall integration at9ddcc088 changes shared proxy paths. Bind newly imported context/wire modules and dependency declarations without changing behavior acceptance or executable gates.

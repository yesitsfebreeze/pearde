---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-proxy-programme
needs:
- '@proxy/improve-proxy-total-usage'
- '@proxy/improve-proxy-tool-trace'
- '@proxy/improve-proxy-continuation-recovery'
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- src/continuation.rs
- src/trace.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/usage.md
- .cartridge/docs/continuations.md
- .cartridge/docs/traces.md
commit: "9ddcc08807a059579c21227ad9d3523d242ddf86"
---

# Proxy improvement plan

Coordinate the three linked outcomes at one integrated source revision. No new feature implementation belongs to this rollup; its executable spec validates dependency receipts and runs the complete proxy suite. See [combined proof contract](specs/spec01.md) and [baseline](baseline.json).

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Account for every internal model round consistently](../improve-proxy-total-usage/prd.md)
- [Inspect internal proxy tool work by request identity](../improve-proxy-tool-trace/prd.md)
- [Make continuation lifetime and restart recovery explicit](../improve-proxy-continuation-recovery/prd.md)

## Review

[Round 3 independent agent review](review.md). Inherits round 1 from `improve-proxy-programme`; maximum five rounds.

Reverification: recall integration at9ddcc088 changes shared proxy paths. Bind newly imported context/wire modules and dependency declarations without changing behavior acceptance or executable gates.

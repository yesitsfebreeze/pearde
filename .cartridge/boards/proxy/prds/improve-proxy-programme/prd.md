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

## From the retired work memo

Folded 2026-09-15 from `work/improve-proxy-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Proxy improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Proxy, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Account for every internal model round consistently | [improve-proxy-total-usage](../improve-proxy-total-usage/prd.md) |
| 2. Inspect internal proxy tool work by request identity | [improve-proxy-tool-trace](../improve-proxy-tool-trace/prd.md) |
| 3. Make continuation lifetime and restart recovery explicit | [improve-proxy-continuation-recovery](../improve-proxy-continuation-recovery/prd.md) |

### Downside coverage

1. Internal rounds are hidden: offer an attributable trace without corrupting the public wire.
2. Extra rounds add latency/failure modes: bound and account for every attempt.
3. Continuation IDs expire: report lifetime and test explicit recovery rather than assuming durability.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Review current source and active ownership before implementation; the assessment does not reserve files.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Proxy behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test proxy
just check proxy
just smoke proxy
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.

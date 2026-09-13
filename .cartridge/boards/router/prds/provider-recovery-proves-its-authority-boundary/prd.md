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
canonical-scope: provider-recovery-proves-its-authority-boundary
footprint:
  - src/health.rs
  - src/proxy.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/docs/recovery.md
commit: "4ad9cd35dc862ecfe0786612d39913612d93fc45"
---

# provider-recovery-proves-its-authority-boundary

Place finite incident recovery at the current router/provider boundary. Coalesce concurrent failures by affected route and give each incident a bounded attempt/deadline budget. Missing credentials or diagnosis route is a visible exhausted/degraded outcome; code/config changes remain reviewable proposals.

## Acceptance

- [x] Repeated failures consume a finite shared budget and concurrent callers do not each spawn a separate recovery loop.
- [x] Recovery is declared only after a real fixture stream on the affected route succeeds, including tool/stream completion semantics.
- [x] Interrupted caller work stays interrupted and no uncertain mutation is replayed; memory itself continues to use configured endpoints without owning a router.

## Proof and recovery

Start at owner-local `src/health.rs` and `src/proxy.rs`.

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `provider-recovery-proves-its-authority-boundary`; maximum five rounds.

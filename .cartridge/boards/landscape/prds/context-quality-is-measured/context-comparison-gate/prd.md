---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: context-quality-is-measured
needs:
- '@landscape/context-quality-is-measured/context-baseline-corpus'
- '@landscape/landscape-composes-system-context'
---

# Context regressions fail an explicit comparison gate

Compare old and new selectors on the frozen corpus with five alternating paired runs.

## Acceptance

- [ ] Missing critical facts, forbidden facts and a deliberately broken ranker each fail.
- [ ] Per-ability recall and paired median latency are reported; more than 20 percent latency regression remains a finding.
- [ ] Hydration/count/byte bounds and unreported truncation are checked independently.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `context-quality-is-measured`; maximum five rounds.

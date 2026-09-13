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
---

# A pinned corpus records the old selector baseline

Freeze 100-row and 10000-row fixtures, critical facts and a 16 KiB scenario before observing candidate results; run the old pinned source in a disposable checkout.

## Acceptance

- [ ] Corpus, old source, toolchain and raw results have digests.
- [ ] Critical-fact, scope and provenance expectations are declared before comparison.
- [ ] The old path runs from a second checkout without altering current work.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `context-quality-is-measured`; maximum five rounds.

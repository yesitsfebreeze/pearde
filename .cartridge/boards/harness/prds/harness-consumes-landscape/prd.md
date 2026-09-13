---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: harness-consumes-landscape
needs:
- memory-document-works-end-to-end
- '@landscape/context-quality-is-measured'
footprint:
- /Users/feb/dev/cartridge/harness.ctg/main.rs
- /Users/feb/dev/cartridge/harness.ctg/inspection.rs
- /Users/feb/dev/cartridge/harness.ctg/working.rs
- /Users/feb/dev/cartridge/harness.ctg/eval
- /Users/feb/dev/cartridge/harness.ctg/tests
---

# Harness builds model context from the shared landscape result

Context gathering is currently split between harness, proxy recall, memo, terminal inspection, and memory. Harness should adapt one sourced context to a model conversation.

## Acceptance

- [ ] Native and proxy paths receive equivalent relevant system facts under the same source snapshot, without double-inserting memory recall.
- [ ] Inspection names selection reasons and unavailable sources and can run without a model call.
- [ ] Existing compaction fault cases preserve the previous summary/transcript; latest user constraints and complete tool exchanges survive.
- [ ] Offline context-quality corpus passes with no regression in critical facts; optional live-model evaluation records model/prompt revision separately.

## Proof and recovery

Start at [main.rs](../../../main.rs), [inspection.rs](../../../inspection.rs), [working.rs](../../../working.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test harness` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `harness-consumes-landscape`; maximum five rounds.

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
canonical-scope: improve-harness-quality-eval
needs:
- '@harness/improve-harness-compaction-diff'
footprint:
- /Users/feb/dev/cartridge/harness.ctg/prompt.rs
- /Users/feb/dev/cartridge/harness.ctg/working.rs
- /Users/feb/dev/cartridge/harness.ctg/inspection.rs
- /Users/feb/dev/cartridge/harness.ctg/inspection_tests.rs
- /Users/feb/dev/cartridge/harness.ctg/eval/eval_compaction.py
---

# Measure multi-round context quality with real task outcomes

Repeated compaction is evaluated for constraints, corrections, evidence, abstention and task success, beyond fixed fixture correctness.

## Acceptance

- [ ] Known-good and adversarial summaries trigger the expected classes across at least three rounds; replay checks final task behavior as well as text needles.
- [ ] Opt-in reports include every failure, tokens, latency, model identity and revisions; offline gates explicitly say they do not establish model quality.

- [ ] Keep canonical transcripts intact. New metadata/inspection is additive; revert compaction settings without discarding old summaries or their source. Live evaluation requires separately configured models and a bounded budget.

## Proof and recovery

Start at [prompt.rs](../../../prompt.rs), [working.rs](../../../working.rs), [inspection.rs](../../../inspection.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test harness` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-harness-quality-eval`, `long-horizon-recall-benchmark`; maximum five rounds.

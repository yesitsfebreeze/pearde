---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-graph-converges
---

# the-graph-converges

Honor the latest reopening: collect integrated repeated-ingest evidence in a disposable current record fixture. Keep delivered consolidation/queue fixes intact and retain writer ownership plus parked recall as separate invariants. Do not repair or repeatedly mutate the shared production store.

## Acceptance

- [ ] Two identical fixture ingests followed by the documented consolidation boundary produce the expected stable entity/source counts and no dangling reasons.
- [ ] Distinct-origin claims retain provenance and the documented ratification relationship rather than being merged across origins.
- [ ] The report records current source/fixture/store revisions and exact counts; a changed fixture or failed metric remains a failure instead of rewriting the baseline.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-graph-converges`; maximum five rounds.

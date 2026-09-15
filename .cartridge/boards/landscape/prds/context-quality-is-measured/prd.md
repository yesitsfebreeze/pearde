---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: context-quality-is-measured
needs:
- '@landscape/context-quality-is-measured/context-baseline-corpus'
- '@landscape/context-quality-is-measured/context-comparison-gate'
---

# Fabric context quality and cost are tested against a versioned corpus

Coordinate the linked outcomes; claim and implement a leaf. The measured selector is now memo's: `memo.ctg/src/context.rs` (`context` op over the `evidence` crate in `memo.ctg/evidence`) and `memo.ctg/src/fabric_graph.rs`. The replacement has already landed, so the "before it lands" baseline is no longer capturable from a live path. Default: the baseline is the memo revision pinned when the corpus is frozen; the dissolved landscape source (GitHub history, `landscape-preremame` snapshot per root decision `the-fabric-lives-in-core.md`) is an optional historical comparison, not a gate input.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The comparison gate runs the frozen corpus against the pinned baseline memo revision and the candidate revision in one invocation, reporting both revisions.
- [ ] A missing or unreadable baseline checkout fails the gate by name instead of skipping the comparison.

## Work items

- [A pinned corpus records the old selector baseline](context-baseline-corpus/prd.md)
- [Context regressions fail an explicit comparison gate](context-comparison-gate/prd.md)

## Integration gate

From /Users/feb/dev/cartridge: `just test memo` plus the comparison command the gate leaf creates; neither has run for this plan. Both leaves still cite `landscape.ctg` and `just test landscape` and must be rebased to memo before claiming.

## Review

[Review history](review.md); rounds inherited, maximum five. Target board after rehoming: memo.

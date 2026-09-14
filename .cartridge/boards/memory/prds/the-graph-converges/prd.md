---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: the-graph-converges
---

# Repeating a multi-document ingest converges to stable counts

Most of this outcome already ships. Arrival folding lives in `src/graph/src/accept.rs`. The `memory consolidate` ratification verb (`ratify_near_duplicates`, memory decision `does-a-merge-cross-origins`) and dangling-reason detection in `memory check` both exist. `.cartridge/tests/integration/e2e/near_duplicates.rs` already proves single-claim folding, two-origin ratification that folds nothing, idempotent re-consolidation, and no dangling reasons. The missing evidence is the reopened case: a multi-document fixture ingested twice, then consolidated, with stable counts. Outcome, owned by memory: that test, with its counts recorded.

## Acceptance

- [ ] In a disposable store, a fixture of at least five documents is ingested twice and then consolidated. Its entity, reason and source counts match a single ingest followed by consolidation, and `memory check --json` reports no `dangling_reasons`.
- [ ] A claim shared by two fixture documents stays as two rows, each with its own source, joined by one Ratification edge. A second consolidate adds zero edges.
- [ ] The test asserts exact counts derived from the fixture. A changed fixture or count fails the test instead of silently resetting the baseline. The commit records the source revision and the command.

## Proof and recovery

First probe: run the scenario by hand at memory.ctg `c25af4d` in a temporary store, using the fixed-vector embed stub, and record the counts. If the counts are unstable, file the defect as its own leaf; do not widen this one. Add the test to `e2e/near_duplicates.rs`. Gates, run from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test`, `just e2e` (not run). Never run it against the shared production store.

## Dependencies and review

No hard needs. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

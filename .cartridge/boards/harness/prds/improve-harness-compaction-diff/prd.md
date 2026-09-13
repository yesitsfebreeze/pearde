---
repo: /Users/feb/dev/cartridge/harness.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-harness-compaction-diff
footprint:
- src/main.rs
- src/inspection.rs
- src/compaction.rs
- .cartridge/tests/unit/compaction.rs
- .cartridge/tests/integration/working.rs
commit: "ca7eeabd38f4eaba69063cf98e2071df694a1dc3"
---

# Inspect what each compaction retained and removed

The inspector shows original covered messages, resulting summary, retained tail and revision/time/usage evidence for a compaction.

## Acceptance

- [x] After two compactions, inspection maps each summary to its exact covered prefix and shows corrected user constraints in source and result.
- [x] A failed compaction retains the prior summary; requesting its comparison makes no model call and leaks no authorization headers.

- [x] Keep canonical transcripts intact. New metadata/inspection is additive; revert compaction settings without discarding old summaries or their source. Live evaluation requires separately configured models and a bounded budget.

## Proof and recovery

Start at [prompt.rs](../../../prompt.rs), [working.rs](../../../working.rs), [inspection.rs](../../../inspection.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test harness` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-harness-compaction-diff`; maximum five rounds.

## Verified implementation — 2026-09-13

`cargo test --manifest-path ../harness.ctg/Cargo.toml -p harness` passes 33 unit
and 6 real-process integration tests. The rolling-memory test performs two
compactions, compares exact source message arrays and original tails, checks a
corrected constraint in source and summary, timestamp/revision/numeric usage,
reload, and four failure modes with unchanged history and transcript. Inspection
leaves the router call count unchanged and excludes provider authorization data.
Legacy metadata gaps and changed-source comparisons have explicit diagnostics.
Malformed legacy text is retained during regeneration; unknown history versions
are refused. Historical comparisons grow with the number of retained summaries.

## Reverification — 2026-09-13

Token accounting ca7eeabd changes the shared inspector and working-memory
fixture. Reopened for the unchanged compaction-history proof; original receipt
retained in collection-a282c877.md. No acceptance is waived.

---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: harness-consumes-landscape
needs:
- '@root/memory-document-works-end-to-end'
- '@landscape/context-quality-is-measured/context-comparison-gate'
footprint:
- /Users/feb/dev/cartridge/harness.ctg/src/main.rs
- /Users/feb/dev/cartridge/harness.ctg/src/inspection.rs
- /Users/feb/dev/cartridge/harness.ctg/src/working.rs
- /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests/unit/main/tests.rs
- /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests/unit/inspection_tests.rs
---

# Harness builds model context from the shared context snapshot

Landscape is dissolved (decision `the-fabric-lives-in-core`): the evidence contract is core's
`cartridge::fabric::evidence`, and memo serves the frozen snapshot as `memo {op:"context"}`
(`memo.ctg/src/context.rs`). Proxy already prepares that snapshot (`proxy.ctg/src/service.rs`,
`src/context.rs`); harness uses the contract only for its roster (`src/roster.rs`) and still
composes system text from `memo {op:"system"}` plus working memory (`src/main.rs`
`memo_template`, `build_context`). Harness should adapt the same memo snapshot, through its
declared `memo` need only. Excluded: memo's contributor protocol, proxy behaviour, new needs.

## Acceptance

- [ ] Native and proxy paths receive the same selected rows for one snapshot revision; memory recall is inserted once.
- [ ] Inspection names each row's selection reason and every unavailable contributor, without a model call.
- [ ] An unavailable or timed-out memo snapshot degrades to the current `memo {op:"system"}` composition and says so.
- [ ] Existing compaction fault cases still preserve the prior summary, latest user constraints and complete tool exchanges.

## Proof and recovery

First probe: record what `build_context` and proxy's prepared snapshot insert for one fixed
disposable session, with harness/memo/proxy revisions and the current `just test harness`
baseline (release-status notes one existing working.rs failure). Then add fixtures in the existing unit entry points
above. Gate: `just test harness` (cwd `/Users/feb/dev/cartridge`); critical-fact regression uses
the comparison gate from the dependency, not a new corpus. Not yet run for this plan.
Rollback: the current memo-system composition stays as the fallback path; transcripts and
summaries are never rewritten by this change.

## Dependencies and review

Both needs are open, so this leaf is not ready. [Review history](review.md); rounds inherited from `harness-consumes-landscape`; limit five.

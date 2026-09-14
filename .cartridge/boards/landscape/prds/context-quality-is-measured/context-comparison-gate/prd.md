---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: context-quality-is-measured
needs:
- '@landscape/context-quality-is-measured/context-baseline-corpus'
footprint:
- /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/context-quality/
---

# Context regressions fail an explicit comparison gate

A change to memo's `context` selection can silently drop critical evidence or slow it down. This leaf compares a candidate memo revision against the pinned baseline revision on the frozen corpus from the needed leaf, in one invocation, and fails on quality regressions.

## Acceptance

- [ ] `bun memo.ctg/.cartridge/tests/context-quality/compare.ts --baseline <sha> --candidate <sha> --output <new dir>` runs five alternating paired runs per scenario and size, reports both revisions, and exits nonzero when a critical fact goes missing or a forbidden fact appears. A deliberately broken ranker fixture must fail it.
- [ ] The report lists per-ability recall and paired median latency. A latency regression above 20 percent is reported as a finding, not a failure. Row, byte and deadline bounds and unreported truncation are checked on their own.
- [ ] A missing or unreadable baseline checkout, a corpus digest mismatch or an existing output directory fails by name before any run. Nothing is skipped.

## Proof and recovery

Reuse the baseline runner and its raw-result format. Gates, cwd `/Users/feb/dev/cartridge`: `just test memo` and `bun test memo.ctg/.cartridge/tests/context-quality/compare.test.ts` (created by this leaf), which covers the broken-ranker and missing-baseline cases. Neither has run. Paired latency is valid only on one host and toolchain in one run window; the report records both. Failure leaves earlier reports untouched.

## Dependencies and review

Hard need: the frozen corpus and baseline runner. The roll-up `landscape-composes-system-context` is context, not a prerequisite: every corpus scenario uses contributors that already exist. Rounds 1–2 are inherited; round 3 rebased ([review](review.md)).

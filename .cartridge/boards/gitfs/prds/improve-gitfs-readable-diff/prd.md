---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: gitfs
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-gitfs-readable-diff
needs:
- '@policy/improve-policy-operation-rules'
- '@gitfs/tool-results-interoperate'
footprint:
- src/service.rs
- src/store.rs
- src/tool_result.rs
- src/inspection.rs
- .cartridge/tests/unit/tool_result.rs
- .cartridge/tests/integration/tool-result.test.ts
- .cartridge/docs/inspection.md
commit: "b4b95bb648ea1e99b6ffc9ba3cbd562f255ca9d5"
---

# Inspect session changes without a mutation grant

A read-only caller can list/read session files and compare overlay, disk and base revisions before materialization.

## Acceptance

- [x] With writes denied, real MCP list/read/diff succeed and leave Git refs, index and worktree unchanged.
- [x] An external disk edit is visible as a conflict with both revisions; oversized diffs are bounded with drilldown.

- [x] Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs), [ship.rs](../../../ship.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-readable-diff`; maximum five rounds.

## Current analysis

[Baseline](baseline.json) confirms no diff operation and read-induced store
creation. Add a lazy read-only store attachment, path-specific three-way
inspection and revision-bound byte drilldown. The existing operation policy
owner registers diff as a recognized operation; all decisions still follow its
configured rules. That small dependency addition is committed and its own
existing proof rerun before collection. No migration, materialization or ship.

## Verified result

Actual MCP with actual policy passes 199 assertions: read/list/diff work, four
mutation operations are denied, refs/indexes/worktree bytes are unchanged, large
UTF-8 pages reconstruct exactly, and changed disk bytes reject continuation.
The public GitFS suite passes 25 tests, formatting/clippy passes, and the public
policy suite passes three contract tests plus documentation checks.

Recorded-push revalidation at b4b95bb: shared native registration and new registered module are bound; original acceptance and executable gates are unchanged.

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
footprint: ["src/service.rs","src/store.rs","src/tool_result.rs","src/inspection.rs",".cartridge/tests/unit/tool_result.rs",".cartridge/tests/integration/tool-result.test.ts",".cartridge/docs/inspection.md","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
needs:
- "@policy/improve-policy-operation-rules"
- "@gitfs/tool-results-interoperate"
- "@root/improve-tool-result-contract"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-gitfs-readable-diff.md` (status open). The PRD state above is authoritative.

### Outcome

A read-only caller can list/read session files and compare overlay, disk and base revisions before materialization.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

### Footprint

GitFS and ship; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `gitfs.ctg/service.rs`
- `gitfs.ctg/store.rs`
- `gitfs.ctg/ship.rs`
- `gitfs.ctg/secrets.rs`
- `gitfs.ctg/cartridge.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] With writes denied, real MCP list/read/diff succeed and leave Git refs, index and worktree unchanged.
- [ ] An external disk edit is visible as a conflict with both revisions; oversized diffs are bounded with drilldown.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Expose bounded diff/status under read-only policy and the common result contract. Explain which tree tests will read, owned paths and materialization conflicts; never materialize during inspection.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test gitfs
just check gitfs
just smoke mcp
```


### Compatibility and recovery

Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

### Handoff

Priority P0; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-policy-operation-rules](../../../policy/prds/improve-policy-operation-rules/prd.md), [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.

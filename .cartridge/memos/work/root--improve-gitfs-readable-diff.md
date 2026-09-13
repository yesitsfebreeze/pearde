---
kind: work
description: "Inspect session changes without a mutation grant"
status: open
priority: P0
size: M
needs:
  - "[[@prd/work/root--improve-policy-operation-rules.md]]"
  - "[[@prd/work/root--improve-tool-result-contract.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["inspect session changes without a mutation grant", "implementing gitfs cartridge improvements"]
---

# Inspect session changes without a mutation grant

## Outcome

A read-only caller can list/read session files and compare overlay, disk and base revisions before materialization.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

## Footprint

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

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] With writes denied, real MCP list/read/diff succeed and leave Git refs, index and worktree unchanged.
- [ ] An external disk edit is visible as a conflict with both revisions; oversized diffs are bounded with drilldown.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Expose bounded diff/status under read-only policy and the common result contract. Explain which tree tests will read, owned paths and materialization conflicts; never materialize during inspection.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test gitfs
just check gitfs
just smoke mcp
```


## Compatibility and recovery

Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

## Handoff

Priority P0; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-policy-operation-rules.md]], [[@prd/work/root--improve-tool-result-contract.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.

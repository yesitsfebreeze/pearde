---
kind: work
description: "Preview and control shipping with accurate attribution"
status: open
priority: P1
size: L
needs:
  - "[[@prd/work/root--improve-gitfs-readable-diff.md]]"
  - "[[@prd/work/root--improve-gitfs-snapshot-selection.md]]"
  - "[[@prd/work/root--improve-policy-operation-rules.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["preview and control shipping with accurate attribution", "implementing gitfs cartridge improvements"]
---

# Preview and control shipping with accurate attribution

## Outcome

A caller can preview exact owned changes, gates, commit attribution and remote effects before separately committing or pushing.

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
- [ ] A temporary repository with unrelated staged edits ships only owned paths using the reviewed tree; supplied attribution is correct and push is separately controllable.
- [ ] Change the tree after preview, fail/timeout the required gate, cancel before commit, or advance the remote: each fails at the correct boundary with no unrelated changes and no silent history rewrite.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Split plan/commit/push at stable tree revisions; make actor/coauthor configurable instead of hardcoded. Expose optional gate status, ensure explicit message does not silently bypass a required gate, declare the optional router dependency, and make cancellation outcomes truthful. Provide revert and explicitly leased rewind alternatives.
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

Priority P1; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-gitfs-readable-diff.md]], [[@prd/work/root--improve-gitfs-snapshot-selection.md]], [[@prd/work/root--improve-policy-operation-rules.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.

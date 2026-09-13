---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one
---

# an ancestry test cannot tell a live lane from an abandoned one

Use explicit operation ownership and release records in runtime worktree tooling. Ancestry and age can refuse cleanup but cannot authorize it. Automatic cleanup requires a recorded released owner plus clean/unowned artifact checks; an unknown or live owner is left intact.

## Acceptance

- [ ] A new clean lane and a long-idle live lane both refuse automatic removal, even when HEAD is an ancestor of main.
- [ ] A released completed lane with only attributable artifacts can be removed by the reviewed cleanup operation.
- [ ] Reused path/branch, dirty files and a changed owner after preview invalidate cleanup; memory records and unrelated worktrees remain untouched.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one`; maximum five rounds.

---
repo: /Users/feb/dev/cartridge/tools.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one
footprint:
- /Users/feb/dev/cartridge/tools.ctg/src/service.rs
- /Users/feb/dev/cartridge/tools.ctg/.cartridge/tests/integration/lane.test.ts
---

# an ancestry test cannot tell a live lane from an abandoned one

`lane-rm` removes a lane only after that lane has been released. Today `lane` in [service.rs](../../../../../../tools.ctg/src/service.rs) authorizes removal with `merge-base --is-ancestor` plus clean and unlocked checks. A lane opened seconds ago, clean and still sitting on the trunk commit, passes all three, so a live session's worktree can be deleted. Ancestry and cleanliness stay as refusals only. Per [the-trunk-checkout-is-a-landing-pad](../../../../../../.cartridge/memos/decision/the-trunk-checkout-is-a-landing-pad.md), ownership is recorded, never inferred from mtime.

Recommended default: `lane` writes a release marker under the lane's Git admin directory recording "open", and a successful `land` rewrites it as "released". `lane-rm` requires "released". An explicit `release <name>` op covers lanes that were merged another way.

## Acceptance

- [ ] A freshly created clean lane whose HEAD equals the trunk is refused by `lane-rm` with a message naming `release`. The worktree and branch remain.
- [ ] `lane`, commit, `land`, `lane-rm` still removes the lane and keeps `.agents/local` (the existing case).
- [ ] A released lane that later gains a commit, dirty file, lock or nested repository is still refused. Other worktrees are untouched.
- [ ] A lane created before this change, with no marker, is refused until `release` is run. Nothing is deleted implicitly.

## Proof and recovery

First add the fresh-lane case to [lane.test.ts](../../../../../../tools.ctg/.cartridge/tests/integration/lane.test.ts) and watch it fail. Gates, cwd `/Users/feb/dev/cartridge`: `just test tools`, `just check tools`. Not run. Rollback: drop the marker check. Markers live in `.git/worktrees/<name>/` and disappear with the worktree.

## Dependencies and review

No hard prerequisites. Shared footprint with `improve-tools-preflight` and `improve-tools-worktree-resume` (same `lane` function), so land them one after another. The implementation lives in tools.ctg ([tui-and-tools-are-cartridges](../../../../../../.cartridge/memos/decision/tui-and-tools-are-cartridges.md)). [Review](review.md): inherits 2 rounds.

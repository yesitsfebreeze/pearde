---
repo: /Users/feb/dev/cartridge/tools.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one.md` (status open, estimate 2h). The PRD state above is authoritative.

> a lane opened seconds ago is clean and its HEAD is an ancestor of main, exactly like a lane landed and abandoned a week ago, so the only test `lane-rm` applies would take a running session's worktree — the sweep needs a discriminator ancestry cannot give it

Found 2026-09-08 while [landed-lanes-are-never-closed](../../../memory/prds/landed-lanes-are-never-closed/prd.md) closed eight worktrees
and pruned 37 merged branches. Six landed-and-present lanes that memo never
named were left alone, and three of them — `compose-services-provide-and-inject`,
`the-exit-flag-tests-race-each-other`, `workstation-layout-contract` — sat on
`main`'s own commit because live sessions had opened them minutes before.

`lane-rm` (`justfile:270-273`) opens with
`git merge-base --is-ancestor {{name}} main`. A lane a session opened seconds
ago passes that test perfectly: `just lane` branches from `main`, so its HEAD
*is* `main` until the first commit, and its worktree is clean because nothing
has been written yet. A lane landed and abandoned a week ago passes the same
test for the opposite reason. The two are indistinguishable to ancestry, so any
sweep that closes on the test alone eventually deletes the tree a session is
working in — the sharpest possible failure for a routine whose whole point is
that nobody loses committed work ([[lanes-not-a-shared-tree]], [[git-policy]]).

### Do

Give the sweep a discriminator that separates the two cases, and use it only to
*refuse*, never to authorise: `lane-rm` keeps its ancestry test and gains one
more. The cheap candidates, in order of how little they assume — the worktree
directory's mtime against a threshold; a `git reflog` entry on the branch; an
owner recorded when `just lane` opens the lane (the session that would then be
asked before it is closed). Pick one, state in the recipe's comment what it
cannot see, and leave the six refusals of the sweep above passing untouched.

Not in scope: closing the two `agent-*` worktrees, which fail one step earlier
for a different reason ([lane-rm-cannot-address-an-agent-worktree](../../../memory/prds/lane-rm-cannot-address-an-agent-worktree/prd.md)).

### Check

A lane opened by `just lane` in the last minute is refused by `lane-rm` with a
line naming why, and a worktree whose HEAD is an ancestor of `main` and whose
discriminator is stale is still removed. Both cases run in one session; `just
memos-check` green.

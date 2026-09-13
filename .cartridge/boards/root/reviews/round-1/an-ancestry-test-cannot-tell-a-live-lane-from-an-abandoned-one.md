---
kind: work
level: 10
status: open
estimate: 2h
description: a lane opened seconds ago is clean and its HEAD is an ancestor of main, exactly like a lane landed and abandoned a week ago, so the only test `lane-rm` applies would take a running session's worktree — the sweep needs a discriminator ancestry cannot give it
read_when: "sweeping .claude/worktrees, or writing a gate that closes a lane automatically"
---

# an ancestry test cannot tell a live lane from an abandoned one

Found 2026-09-08 while [[landed-lanes-are-never-closed]] closed eight worktrees
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

## Do

Give the sweep a discriminator that separates the two cases, and use it only to
*refuse*, never to authorise: `lane-rm` keeps its ancestry test and gains one
more. The cheap candidates, in order of how little they assume — the worktree
directory's mtime against a threshold; a `git reflog` entry on the branch; an
owner recorded when `just lane` opens the lane (the session that would then be
asked before it is closed). Pick one, state in the recipe's comment what it
cannot see, and leave the six refusals of the sweep above passing untouched.

Not in scope: closing the two `agent-*` worktrees, which fail one step earlier
for a different reason ([[lane-rm-cannot-address-an-agent-worktree]]).

## Check

A lane opened by `just lane` in the last minute is refused by `lane-rm` with a
line naming why, and a worktree whose HEAD is an ancestor of `main` and whose
discriminator is stale is still removed. Both cases run in one session; `just
memos-check` green.

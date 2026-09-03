---
complexity: 5
footprint:
  - references/parts/loop.md
  - references/parts/handles.md
  - references/files.md
---

# spec03 — the three files that say a session's tree is not resolved

Three documents describe `session.py` as it was before this PRD, and one of
them says so in as many words. A reader who follows them will run a pass that
takes a tree and then work in the checkout anyway, because the loop never tells
them the tree is now where everything happens.

**`references/parts/loop.md`** carries, under *Before step 0*: *"Board commands
do not yet resolve the taken tree as the code repo; that is a separate unit."*
That sentence is this PRD, and it is now false. Replace it with what a session
actually gets: from `take` onward every board command resolves the session's
own worktree as the code repo, lanes are cut off the session's branch, collect
merges and commits there, and each collect puts the result on the branch the
checkout is on — printing `landed on <branch>`, or naming the refusal when the
checkout is dirty. Say the last part plainly: a refused land loses nothing and
`pearde session land` retries it.

**`references/parts/handles.md`** has the `a worktree per run session` row
listing `take/list/reap/owns`. Add `land` to the verb list and to the row's
description — what it does, that it is a rebase then a fast-forward, and that
`merge --ff-only` is the whole of what it runs in a tree the session does not
own. The row's closing *"Both writers run before step 0"* now has three
writers and one of them runs after a collect, not before step 0; say which is
which.

**`references/files.md`** has the `@resources/board/session.py` row. It names
the four verbs and the ledger. It must also name `land`, and name the module as
what every board command asks before it resolves a code repo — otherwise the
map says `session.py` is a worktree manager and a reader has no reason to open
it while chasing `collect.repo_of`.

Nothing else in `references/` claims the old behaviour: the sentence in
`loop.md` is the only outright statement of it, and the other two are
incomplete rather than wrong.

## Acceptance

- [x] `references/parts/loop.md` no longer says board commands do not resolve the taken tree
- [x] `references/parts/loop.md` says what a session gets from `take` onward — the code repo, the lane's base, where collect commits, and the land at the end of a collect
- [x] `references/parts/loop.md` says a refused land loses nothing and names the verb that retries it
- [x] `references/parts/handles.md` lists `land` among the session verbs and describes it as a rebase then a fast-forward
- [x] `references/parts/handles.md` no longer says two writers run before step 0 without saying which runs after a collect
- [x] `references/files.md` names `land` in the `session.py` row and says the module answers what a board command means by the code repo
- [x] `python3 resources/index.py check` reports no new unresolved reference from these three files

## Verify and Proof

```sh
# The claim that must be GONE. `grep -v` is not this check — it exits 0 on
# any file with a second line, so it can never fail; the exit code of the
# positive grep is the only thing that answers.
grep -q 'do not yet resolve the taken tree' references/parts/loop.md && rc=0 || rc=$?
[ "$rc" != "0" ]

# the claims that must be there
grep -q 'session land' references/parts/loop.md
grep -q 'landed on' references/parts/loop.md
grep -q 'session take/list/reap/land/owns' references/parts/handles.md
grep -q 'land' references/files.md

# the map still resolves every reference these three files make. `check`
# reports the whole tree, so only lines naming these files can fail it.
out=$(python3 resources/index.py check 2>&1 || true)
printf '%s\n' "$out" | grep -E '^(references/parts/loop\.md|references/parts/handles\.md|references/files\.md) ' && rc=0 || rc=$?
[ "$rc" != "0" ]
```

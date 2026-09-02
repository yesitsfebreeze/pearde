---
complexity: 9
footprint:
  - references/files.md
  - references/parts/handles.md
  - references/parts/loop.md
  - index.md
---

# spec02 — a session takes its tree at step 0, and the map says so

`session.py` is a command nothing calls and no map names. This unit gives it
its row in the manifest, its row in the handles table, its keyword in the
index, and its place in the loop: a pass reaps what is gone and takes a tree
of its own before it does anything else.

**The manifest row already stands** — `references/files.md` carries the
`@resources/board/session.py` row, and `python3 resources/index.py check` no
longer reports the file as on disk with no row. Three index problems remain
and none of them is this file's; they are named in this PRD's report as
findings and are not this spec's to fix. What is left is the handles row, the
index keyword and the loop text.

**The loop.** Reaping comes before taking and both come before step 0's ramp,
because a reap that runs after a take would have to reason about a tree the
running session just made, and the whole point of the reaper is that it never
touches a live session's work. The two lines a pass runs, in order:

    pearde session reap --apply
    pearde session take

`reap --apply` is safe to run while other sessions are alive — that is
spec01's measured property and the reason it can sit unconditionally at the
head of every pass. `take` is idempotent, so a pass resumed in the same
session takes nothing new.

**What this spec does not do.** It does not make the board's commands resolve
the taken tree as the code repo — that is the sibling
`board-commands-run-in-the-session-s-tree-not-the-checkout`, and until it
lands the loop text says the session takes a tree and works in it, not that
every command follows it there. Writing more than that here would put a claim
in the prose that the code does not yet keep.

## Acceptance

- [x] `references/files.md` carries a row for `@resources/board/session.py`
- [x] `python3 resources/index.py check` reports no problem naming `session.py`
- [x] `references/parts/handles.md` carries a row for `session`, naming the four verbs and `@resources/board/session.py`
- [x] `index.md` names `@resources/board/session.py` under the keyword that covers the board's commands
- [x] `references/parts/loop.md` says a pass runs `pearde session reap --apply` then `pearde session take` before step 0
- [x] the loop text says a live session's worktree is never reaped and a dead one's work is in `refs/pearde/reaped/<id>`
- [x] the loop text does not claim board commands resolve the session's tree — that is the sibling PRD
- [x] `python3 resources/index.py check` reports no new problem against the tree before this spec

## Verify and Proof

```sh
# `grep -c` exits 1 on its passing result — nothing matched — so the
# producer is guarded and the count is asserted, never the pipeline.
n=$( { python3 resources/index.py check 2>&1 || true; } | grep -c session || true )
[ "$n" = 0 ]
grep -q 'session take/list/reap/owns' references/parts/handles.md
grep -q '@resources/board/session.py' references/parts/handles.md
grep -q '@resources/board/session.py' index.md
grep -q 'pearde session take' references/parts/loop.md
grep -q 'pearde session reap --apply' references/parts/loop.md
grep -q 'refs/pearde/reaped' references/parts/loop.md
grep -q '@resources/board/session.py' references/files.md
# doctor reads the whole checkout, so its row is printed and decides nothing.
out=$(bash resources/doctor.sh . 2>&1 || true)
[ -n "$out" ]
printf '%s\n' "$out" | grep -E '^  index' || true
```

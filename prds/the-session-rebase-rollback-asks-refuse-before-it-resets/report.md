# report — the session rebase rollback asks refuse before it resets

Verdict: BLOCKED

The wall in one line: **the contract is already satisfied on `main`, by a
different change than the spec describes, and implementing the spec verbatim
would undo it.** No file was written. `main` is green; the lane is not the
tree the invariant reads any more.

## The wall

The PRD opens "**RED on main**: one FAIL against six PASS". That is no longer
true. Commit `cc624b3` — *a-session-lands-with-reset-keep — land() refuses
rather than discards, and the destructive-git invariant is green again* —
landed on `main` after this lane branched, and fixed the same FAIL a different
way: it did not gate the `reset --hard`, it **removed** it, spelling the
rollback `reset --keep` instead.

```
$ bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
PASS  the reader sees an ungated `reset --hard`, a `clean` spelled with a concatenated pathspec, and a real `stash`, in a synthetic module
PASS  and reads `reset --keep`, `stash create` and a plain `checkout` as discarding nothing
PASS  resources/board/collect.py:750 — git stash in `_park`, exempt while its recorded reason ('stash-then-POP') stands
PASS  resources/board/collect.py:1142 — git stash in `guarded_run`, exempt while its recorded reason ('stash-then-POP') stands
PASS  resources/board/lanes.py:257 — git reset in `merge`, gated
PASS  38 Python file(s) under resources/ hold no ungated destructive git
EXIT=0
```

Six PASS, no FAIL, exit 0 — the PRD's first acceptance box, word for word,
on `main` today with nothing of this PRD's in it.

The lane (`lane/the-session-rebase-rollback-asks-refuse-before-it-resets`)
sits on `dca5ce2`, two PRDs behind `main`, and carries `a903f85`
*wip: session refuse-before-reset — worker died at 11:18:04 before reporting*:
the `_may_discard` gate on a kept `reset --hard`. It is not uncommitted, as
spec01 says — the previous worker's pass committed it before it died.

## Why the spec cannot simply be run

spec01's boxes 2 and 5 require the invariant to print a new PASS line
`resources/board/session.py:<line> — git reset in ...land..., gated`, and the
probe's `mine` case to report `"reset_hard_ran": true`. Both are only reachable
by putting a `reset --hard` **back** into `land`. That is a regression against
`main` on the invariant's own terms: gating a destructive command leaves a
destructive command in the tree behind a guard, while `reset --keep` leaves
none at all — the invariant's second self-test PASS is exactly the reader
"reads `reset --keep` … as discarding nothing".

The probe agrees, measured both ways:

| case | tree | `reset_hard_ran` | `restored` | `names_the_file` | `dirt_kept` |
|---|---|---|---|---|---|
| mine | main (`reset --keep`) | false | true | true | true |
| theirs | main (`reset --keep`) | false | true | true | true |
| mine | lane (gated `reset --hard`) | true | true | true | true |
| theirs | lane (gated `reset --hard`) | false | true | true | true |

Both restore the branch and name the conflicting file. `main` reaches that with
no destructive command and no guard call on the path.

The gate approach also carries a defect `main`'s does not, and the probe's own
docstring names it. Run against the lane:

```
"case": "symlink",  "restored": true,  "gate_answer": false,
"gate_tree_is_the_ledger_s": false
```

Under an unresolved path (macOS `/var` → `/private/var`), `land` hands
`_may_discard` the path `git worktree list` prints — resolved — while the
ledger holds the path `session take` wrote, unresolved. The strings differ, the
owning session reads as a stranger, and the guard refuses a tree the session
does hold. Fail-closed, so nothing is lost; but it is the wrong answer, and
`main` never asks the question.

## What holds on main, box by box (PRD acceptance)

- [x] Invariant exits 0, FAIL gone, six PASS unchanged — output quoted above.
- [x] The rollback still restores on a conflicting rebase — probe `mine` and
      `theirs` against `main`: `"restored": true`, `"names_the_file": true`,
      `"error": "conflict: session/s58770 onto main — shared.txt"`, and
      `"dirt_kept": true` (the untracked file survives).
- [ ] "The gate is `refuse.py` … or the exemption carries a recorded reason" —
      **neither, and moot**: `main` has no destructive command in `land` to
      gate and adds no `EXEMPT` row. The box presupposes a `reset --hard` that
      is gone.

Also clean on `main`, for the two spec boxes that are implementation-neutral:

```
$ python3 -c "import ast; ast.parse(open('resources/board/session.py').read())"   # AST OK
$ python3 resources/board/session.py list --board /Users/feb/dev/infra/pearde/.pearde
* s9856      alive    pid 9856 running since Thu Sep  3 11:08:26 2026 · sock
$ python3 resources/index.py check      # four pre-existing rows, none about session.py
```

## The question for the orchestrator

One decision, and I will not guess it:

**Close this PRD as superseded by `cc624b3`, and drop
`lane/…rebase-rollback…` with its wip commit — or is the gate wanted on top of
`reset --keep` for a reason not on the board?**

My recommendation is the first. `main` satisfies the contract's intent (the
invariant is green, the rollback still restores), reaches it with a strictly
smaller surface, and avoids the symlink mis-answer. If the PRD is closed,
`a903f85` should go with the lane rather than be rebased — rebasing it onto
`main` would conflict on the same lines `cc624b3` rewrote, and resolving that
conflict is the regression, not a merge.

## Defects outside scope

- `python3 resources/index.py check` reports four rows unrelated to this
  footprint: `resources/common.py` on disk with no row in
  `references/files.md`; `references/files.md` and `@@view` both naming
  `@resources/board/hotreload-test.js`, deleted in `b1d3f5d`; and
  `references/parts/commits.md` referencing
  `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`, not on disk.
  Reported, not fixed.
- The `symlink` case above is a real defect in `lanes._may_discard`'s caller
  contract — `land` passes an already-resolved path, `refuse.holder` compares
  it against an unresolved ledger string. It is fail-closed and it does not
  bite `main`, since `main` no longer calls the guard from `land`; but
  `lanes.py:257` makes the same call and may take the same path. Reported, not
  fixed — outside this footprint.

## Footprint

Nothing written. `resources/board/session.py` is unchanged from `main`, and no
file under this PRD's directory was edited but this report.

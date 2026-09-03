---
complexity: 8
footprint:
  - resources/board/session.py
---

# spec01 — the rebase rollback in `session.land` asks `refuse.py` first

`land`'s rollback arm resets the branch hard to the SHA read before a failed
rebase. The reset is a restore rather than a discard, which is why it was
written ungated — but the tree it runs in is a worktree the running session
may not hold, and the invariant admits no exception without a recorded
reason. This unit puts `lanes.merge`'s gate on it, so the reset runs only
when `rebase --abort` reports a rebase it actually stopped **and** the guard
says this session may discard that tree.

**Already standing** — the whole change is in the lane, uncommitted, and
every box below passes against it:

- the rollback reads
  `if aborted.returncode == 0 and laneslib._may_discard(wt):`, with the
  reason written above it in the shape `lanes.merge` uses;
- `land`'s docstring says the rollback asks the guard, in place of the older
  claim that no destructive command runs in a tree this session does not own;
- the probe at `.pearde/prds/the-session-rebase-rollback-asks-refuse-before-it-resets/probe/rollback.py`
  measures all three arms.

**Left to finish** — nothing beyond re-running the checks below in the tree
the implementer holds, and committing.

## Acceptance

- [x] `bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` exits 0 and its `session.py … not gated` FAIL line is gone.
- [x] That run prints a PASS reading `resources/board/session.py:<line> — git reset in ...land..., gated` beside the `lanes.py:257` PASS, and the two `collect.py` exemption PASS lines and the two reader self-test PASS lines are unchanged.
- [x] The gate is `laneslib._may_discard(wt)`, the same call `lanes.py:257` makes, and no exemption row is added to the invariant's `EXEMPT` table.
- [x] The gate is the SECOND condition: `rebase --abort` returning 0 is still tested first, so a rebase that never started is left alone.
- [x] Probe case `mine` — this session holds the tree: the guard answers true, the `reset --hard` runs, the branch is back at the pre-rebase SHA, and the raised error names the conflicting file.
- [x] Probe case `theirs` — a live peer holds the tree on the ledger: the guard answers false, no `reset --hard` runs, and the branch is STILL back at the pre-rebase SHA with the conflicting file named.
- [x] `resources/board/session.py` parses, and `python3 resources/board/session.py list --board <this board>` still prints the ledger — the module loads and its other verbs are untouched.
- [x] `python3 resources/index.py check` reports nothing new about `resources/board/session.py`.

## Verify and Proof

```sh
bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
python3 .pearde/prds/the-session-rebase-rollback-asks-refuse-before-it-resets/probe/rollback.py mine theirs
python3 -c "import ast; ast.parse(open('resources/board/session.py').read())"
python3 resources/board/session.py list --board /Users/feb/dev/infra/pearde/.pearde
python3 resources/index.py check
```

The probe prints one JSON object per case. `mine` must carry
`"reset_hard_ran": true`, `"gate_answer": true`, `"restored": true`,
`"names_the_file": true`; `theirs` must carry `"reset_hard_ran": false`,
`"gate_answer": false`, and `"restored": true` and `"names_the_file": true`
unchanged — the rollback surviving the refusal is the point of the second
case, and a `theirs` run that lost the branch is a failure however green the
invariant reads.

Run the probe from the repo root with `PEARDE_TREE` pointing at the tree
under test when that tree is not the lane the probe was written beside.

---
complexity: 9
footprint:
  - resources/doctor.sh
  - references/parts/doctor.md
  - references/parts/ramp.md
  - references/parts/loop.md
  - references/parts/handles.md
  - references/settings.md
  - references/files.md
---

# spec02 — the reading moves to a doctor row, and the loop opens on the scan

The question the gate asked is real; the place it asked it was wrong. It
becomes one `doctor` row reading `ramp gap` — local, tracked paths against the
machine's skill directories, no network — and the loop's step 0 disappears, so
pass one on a fresh board reaches the scan.

**Stands** (built in the probe, uncommitted in the lane): a `ramp` row in
`doctor.sh` between `board` and `vault`, modelled on `plugins` — a reading of
the machine, so an unanswered job is `off`, never `broken`, with `pearde ramp`
as its fix line and a `note` saying nothing waits on it; `references/parts/loop.md`
loses its `0 ramp` table row and its `**0 · Ramp.**` paragraph, gaining one
paragraph saying the loop opens on the scan, and `before step 0` becomes
`before step 1`; `references/parts/ramp.md` opens on *It is a doctor row, not a
gate*; `references/settings.md` loses the `happiness` row and the yaml line;
`references/parts/doctor.md` gains the `ramp` row; `handles.md` and `files.md`
are re-worded off the gate.

**Left to finish**: nothing but the checks below and the commit.

## Acceptance

- [ ] `doctor` prints a `ramp` row on any board, between `board` and `vault`.
- [ ] With a gap standing the row reads `off`, names the missing jobs, and carries `fix: … pearde.py ramp <board>` plus a note that a gap is not a failure.
- [ ] With every job answered the row reads `ok · N jobs`; on a tree the jobs table recognises nothing in, it reads `off · the tree asks for nothing the jobs table recognises`.
- [ ] The `ramp` row never reads `broken` for a gap, and never contributes to doctor's exit code.
- [ ] The row costs no network call: it runs `ramp gap`, never `ramp find` or the bare verb.
- [ ] `grep -n 'happiness' references/settings.md` matches nothing, and the yaml block shows five keys plus `context-budget`.
- [ ] `references/parts/loop.md` holds no `0 ramp` row and no `**0 · Ramp.**` paragraph; its step table starts at `1 scan`.
- [ ] `references/parts/doctor.md`'s parts table holds a `ramp` row saying `off` is a reading and not a failure.
- [ ] `python3 resources/index.py check` reports no problem that was not already there before this PRD — the four standing ones are named in the report as out of scope.

## Verify and Proof

```sh
bash -n resources/doctor.sh
PEARDE_ROOT=$(pwd) bash .pearde/prds/the-tree-holds-only-what-a-board-uses/ramp-is-a-doctor-row-not-a-gate/probe/verify.sh
python3 resources/index.py check
grep -c happiness references/settings.md; grep -c '0 ramp' references/parts/loop.md
```

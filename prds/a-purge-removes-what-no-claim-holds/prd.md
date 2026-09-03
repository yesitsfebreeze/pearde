---
state: open
origin: requested
priority: 70
complexity: 0
blast-radius:
needs: the-board-reclaims-dead-work-by-itself
---

# a purge removes what no claim holds

A person-facing command that does, in one shot across every board on this
machine, what the pass does incrementally: drop every lane the board no
longer holds a claim on, and report what it kept and why. Measured
2026-09-03, one hand-run across three boards (pearde, mitosys, kern)
removed 35 clean lanes and ~10 GB; nothing on the board today does that
deliberately — the space came back because a person typed a loop.

## Done means

- `pearde purge [--apply]` walks every registered board's `.lanes/` and
  prints one row per lane: `PURGE` (no open claim, worktree clean) or
  `KEEP` (open claim on the board, or uncommitted changes in the tree —
  with the paths that made it dirty).
- `--apply` removes the PURGE rows: registered worktrees via
  `lanes.remove` (branch kept, `worktree prune` after), plain remnant
  dirs (no `.git`) with `rm -rf`. Never `--force` past the clean check —
  a dirty lane is a KEEP, not a force case.
- The branch is kept in every case, as `lanes.remove` does today; purge
  deletes no `lane/<slug>` ref.
- Without a claim on the PRD, a lane is kept — the check reads
  `plan.py scan`'s claim fields, not mtimes alone, so a worker that is
  merely thinking past `claim-ttl` survives.
- Boards with no `.lanes/` print nothing, not an error.

## What must not change

- `lanes.remove`'s contract: the branch stays, uncommitted dirt dies with
  the worktree only when a claim no longer holds it — the constraint the
  `the-board-reclaims-dead-work-by-itself` container states tree-wide.
- Shared stores (`one-copy-per-machine-of-what-every-lane-regenerates`)
  are never deleted by a purge; they outlive lanes.

## Needs

`the-board-reclaims-dead-work-by-itself` — a purge run between passes
must read the same claim truth the automatic reclaim acts on, or the two
disagree about which lanes are "not used anymore".
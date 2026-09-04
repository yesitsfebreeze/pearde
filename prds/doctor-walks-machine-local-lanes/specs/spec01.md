---
complexity: 12
footprint:
  - resources/board/lanes.py
  - resources/doctor.sh
---

# spec01 — doctor walks every machine-local lane and says which cannot find the board

`lanes.create` excludes the board's own path from a lane's checkout and
symlinks it back in (`link_board`, where the running lanes.py carries it) —
without that link a worker's `.pearde/prds/…` is `No such file or
directory` inside its own lane. Measured live on this machine: 7 of 45
lanes under `.pearde/.lanes/` have no such link — some cut before
`link_board` existed, at least one (`doctor-walks-machine-local-lanes`,
this PRD's own lane) cut while the claiming process's own repo was a
SESSION worktree nested inside the board, where `board_rel(board, repo)`
answers `None` (the board is `repo`'s ancestor, not the other way round)
and `link_board` silently no-ops. Nothing before this said so.

`lanes.py` gains `check(board)` — one `"<slug>: no link to the board"` line
per lane whose top level holds nothing that resolves (`os.path.realpath`)
to the live board, empty when every lane can reach it — and `relink(board,
slug)`, which places a plain symlink to the board, named after it, at the
lane's root, and refuses (returns `None`, touches nothing) when something
else already sits there. Both are already proven against a throwaway board
and against the 45 real lanes on this machine (see `## Report`).

`doctor.sh` gains a `lanes` row, board-scoped like `health`: `ok` with the
lane count when every lane resolves the board, `broken` with one line per
lane `check` names otherwise, and a `fix:` line pointing at `pearde doctor
--fix`. Under `--fix`, the row calls `relink` for every lane `check` named
and reports `relinked` or `refused — something else is already there` per
lane — never a silent overwrite, and never anything for a lane `check`
did not name.

Already stands, built and run against the real board and against a
fixture, in this lane's checkout:

- `lanes.check` / `lanes.relink` (`resources/board/lanes.py`, appended
  after `list_lanes`)
- the `lanes` row in `resources/doctor.sh` (appended after the `health`
  section)

## Acceptance

- [ ] `lanes.check(board)` returns one line per lane whose top level holds
      no path that resolves to `board`, and returns `[]` when every lane
      does
- [ ] `lanes.relink(board, slug)` places a working symlink to `board`
      named after it at the lane's root and returns that path
- [ ] `lanes.relink(board, slug)` returns `None` and leaves the tree
      unchanged when a non-matching file or directory already occupies
      that name
- [ ] `bash resources/doctor.sh <board>` prints a `lanes` row: `ok` with
      the lane count when `check` returns `[]`, else `broken` with one
      line per name `check` returned
- [ ] `bash resources/doctor.sh --fix <board>` calls `relink` for every
      name the `lanes` row found broken and prints `relinked` or `refused
      — something else is already there` for each, then a re-run of
      `doctor.sh` (no `--fix`) shows only the refused ones still broken

## Verify and Proof

```sh
# exercises resources/board/lanes.py check/relink and the resources/doctor.sh lanes row
bash .pearde/prds/doctor-walks-machine-local-lanes/probe/verify.sh
```

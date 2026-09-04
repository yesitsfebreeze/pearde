---
complexity: 6
footprint:
  - resources/doctor.sh
---

# spec02 — doctor's own walk, and its old-layout fix lines, name the current direction

`resources/doctor.sh`'s `board_named()` (the shell half `references/parts/board.md`
"written seven times" already credits) runs `for n in pearde .pearde`, the
reverse of the order every Python resolver holds since the 2026-09-03 revert.
Three surrounding comments describe the walk as "`pearde/` (or the legacy
`.pearde/`)" — backwards. And two fix lines still prescribe the reverted
2026-09-02 direction on a genuinely pre-migration board (a bare `prds/` with
no board directory at all): `mkdir -p $OFFROOT/pearde` and "no board — pearde
init creates pearde/" both name the undotted directory `pearde init` no
longer creates — `resources/board/boards.py` has made `BOARD_DIR = ".pearde"`
the one it writes since the revert.

Confirmed by `probe/order-and-duplication.sh`. This spec is the mechanical
half only: the `for n in` order and these two stale fix lines. It does not
touch the separate `vault` row (`board is $BOARD — a dot-segment ...`,
further down, `fix "... upgrade $PROJ — moves it to $PROJ/pearde ..."`) —
that row's own premise (a `.pearde` board is a vault defect `upgrade` should
fix by un-hiding it) is a design question the PRD this pass sits under does
not answer, and it is reported, not specced, in `report.md`.

## Acceptance

- [x] `board_named()`'s loop tests `.pearde` before `pearde`.
  - `grep -n 'for n in' resources/doctor.sh | grep -q 'for n in \.pearde pearde'` passed.
- [x] The three comments above `board_named()`, the guard-hook walk and the board row that name the walk order say `.pearde/` (current) and `pearde/` (legacy, read through its compat symlink) — not the reverse.
- [x] The "old layout" fix line creates `$OFFROOT/.pearde` (not `$OFFROOT/pearde`) and the `git mv` target is `$OFFROOT/.pearde/prds`.
  - `grep -n 'OFFROOT/pearde'` → no match (exit 1).
- [x] The "no board" row's fix text says `pearde init creates .pearde/`.
  - `grep -n 'creates pearde/'` → no match (exit 1).
- [x] The `vault` row and its fix line (the un-hiding one) are unchanged — out of this spec's footprint.
  - `doctor.sh:499` still holds `upgrade $PROJ — moves it to $PROJ/pearde and leaves a .pearde symlink`.
- [x] `resources/doctor.sh` still parses under `bash -n` and still reports `board ok` on this repo's own board.
  - `bash resources/doctor.sh` → `board  ok  /Users/feb/dev/infra/pearde/.pearde/prds · 229 PRDs · language English`.

## Verify and Proof

```sh
cd "$REPO"
bash -n resources/doctor.sh
grep -n 'for n in' resources/doctor.sh | grep -q 'for n in \.pearde pearde'
grep -n 'OFFROOT/pearde' resources/doctor.sh && exit 1
grep -n 'creates pearde/' resources/doctor.sh && exit 1
bash resources/doctor.sh 2>&1 | grep -E '^  board +ok'
# the vault row's un-hiding fix must survive untouched
grep -n 'moves it to .*pearde and leaves a \.pearde symlink' resources/doctor.sh
```

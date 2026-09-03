---
state: done
origin: derived
priority: 95
complexity: 20
blast-radius: high
workflow: probe-then-spec
actual: 12.51h
commit: 39c0cab 06743eb
---

# the daemon must not write into a board path it no longer owns

The view daemon creates a board directory in another project by writing its
watch marker to a path it captured before that board moved.

## What happens

`resources/board/serve.py`'s `entry_path()` builds `<board>/.state/serve.json`
through `planlib.state_dir()`, and `state_dir()` at `resources/board/plan.py:107`
runs `os.makedirs(d, exist_ok=True)` unconditionally. `os.makedirs` creates
every intermediate directory, so the call does not merely make `.state` inside
a board that exists — it brings `<board>` itself into being.

`save_entry()` writes that file for every watched board on the daemon's tick,
using `b.path` from the **in-memory** watch set — the path captured when the
board registered. A board that has since migrated on disk (`.pearde/` →
`pearde/`, this repo's own `92e318c`) is still held at its old path, so the
tick recreates `<repo>/.pearde/.state/serve.json` and, with it, a `.pearde/`
directory in a project that deliberately no longer has one.

`drop_entry()` has the same shape: `forget` calls `os.remove(entry_path(...))`,
so even un-watching a board creates its `.state/` directory first.

Observed live on 2026-09-02: this board's daemon `pearde-2` (port 8443,
started 18:32:30) holds `manola` in its watch set and polled it 1327 times,
every request answering 404 — the daemon cannot resolve the board it is still
writing a marker into.

## Why this is not the read-path bug it looked like

`plan.py`'s own read path was cleared. `board_at()` returns a non-existent
`<d>/pearde` as its fallback, but it is called only from `init.py` — the
create path, where that is correct. `machine.py`'s separate `board_at()`
returns `None` rather than a path and creates nothing (it is separately blind
to the legacy `.pearde` name, which is a different, smaller defect). `scan`
and `parse_cache_load` do reach `state_dir()` and so do create `.state/`
inside a board — but only one `find_board()` already resolved to a real board.
**The writer is the daemon's stale in-memory path, not a stale module.** Both
installed copies of `plan.py` read `BOARD_DIR = "pearde"`, so no stale
resolution exists on this machine.

## What exists when this is done

- `state_dir()` never conjures a board. It creates `.state` inside a directory
  that already carries a board (`is_board_dir`) and refuses otherwise.
- The daemon revalidates a watch entry's path before writing to it, and a
  board whose path no longer carries a board is dropped from the watch set
  rather than re-created at the old name.
- `drop_entry()` removes without creating.

## Consequence for requested work

`every-run-session-works-in-a-worktree-of-its-own` contracts that no command
runs destructively in a tree the running session does not own. This is the
same violation on the write side: a daemon started in one project creates
directories in six others. That PRD's `refuse` row is not satisfiable while
this stands.

## What must not change

The watch set stays the daemon's whole configuration — no machine-wide list
of boards. Dropping a stale entry must not add one.

## Verify

Register a board, move it on disk from `.pearde/` to `pearde/`, and let the
daemon tick. The old path must not come back into existence, and the board is
either re-resolved at its new path or dropped.

## Report

spec01: exit 0
  ok    state_dir does not conjure a board directory · declined with NotABoard
  ok    state_dir refuses a directory that carries no board · declined with NotABoard
  ok    state_dir declines with an OSError, not a SystemExit · raised NotABoard
  ok    save_entry does not re-create a board at a path it no longer owns · declined with nothing
  ok    save_entry declines without raising
  ok    drop_entry does not create the board directory · declined with nothing
  ok    the watch set drops a path that carries no board · 0 left, declined with nothing
  ok    state_dir still makes .state inside a real board · /Users/feb/dev/infra/pearde/.probe-daemon-path/proj-3qyxvbqz/pearde/.state
  ok    save_entry still records a real board
  ok    drop_entry still removes a real board's marker
10 checks · 10 pass · 0 fail
probe harness complete

spec02: exit 0
  ok    state_dir does not conjure a board directory · declined with NotABoard
  ok    state_dir refuses a directory that carries no board · declined with NotABoard
  ok    state_dir declines with an OSError, not a SystemExit · raised NotABoard
  ok    save_entry does not re-create a board at a path it no longer owns · declined with nothing
  ok    save_entry declines without raising
  ok    drop_entry does not create the board directory · declined with nothing
  ok    the watch set drops a path that carries no board · 0 left, declined with nothing
  ok    state_dir still makes .state inside a real board · /Users/feb/dev/infra/pearde/.probe-daemon-path/proj-ng_4sb8y/pearde/.state
  ok    save_entry still records a real board
  ok    drop_entry still removes a real board's marker
10 checks · 10 pass · 0 fail
probe harness complete

spec03: exit 0
  ok    state_dir does not conjure a board directory · declined with NotABoard
  ok    state_dir refuses a directory that carries no board · declined with NotABoard
  ok    state_dir declines with an OSError, not a SystemExit · raised NotABoard
  ok    save_entry does not re-create a board at a path it no longer owns · declined with nothing
  ok    save_entry declines without raising
  ok    drop_entry does not create the board directory · declined with nothing
  ok    the watch set drops a path that carries no board · 0 left, declined with nothing
  ok    state_dir still makes .state inside a real board · /Users/feb/dev/infra/pearde/.probe-daemon-path/proj-jddukcnc/pearde/.state
  ok    save_entry still records a real board
  ok    drop_entry still removes a real board's marker
10 checks · 10 pass · 0 fail
probe harness complete
the two guards removed in the copy
10 checks · 6 pass · 4 fail
probe harness complete

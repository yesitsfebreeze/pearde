---
complexity: 10
footprint:
  - resources/board/init.py
  - resources/board/example/
---
<!-- Add your own keys freely. Nothing outside complexity, footprint and
     workflow is read. -->

# spec01 — write_board() writes the .pearde/ shape, not the old prds/ one

`write_board()` in `resources/board/init.py` seeded a new board wrong on two
counts: `--example` landed the example PRDs at `<board>/<name>/` instead of
`<board>/prds/<name>/` (so `scan` found none of them), and neither branch
made the five directories a board has even when empty (`prds/`, `memos/`,
`wiki/`, `workflows/`, `.state/`).

**What already stands** (built and verified during analysis, uncommitted):

- `resources/board/example/` was restructured on disk to mirror the board
  layout: `settings.md`, `memos/`, `workflows/` moved up from
  `example/prds/` to sit beside `example/prds/` itself (which now holds only
  the six PRD directories — `asking`, `big` (with `first`, `second`),
  `building`, `finished`, `landed`, `next`). `example/README.md` stays where
  it is — a doc about the example, not board content.
- `init.py`'s `EXAMPLE` constant now points at `example/` (not
  `example/prds`), and `write_board()`'s single `shutil.copytree(EXAMPLE,
  board, dirs_exist_ok=True, …)` carries an `ignore=shutil.ignore_patterns(
  "README.md")` so that doc file is not copied onto the board.
- `write_board()` now ends with
  `for name in (planlib.PRDS_DIR, "memos", "wiki", "workflows", ".state"):
  os.makedirs(os.path.join(board, name), exist_ok=True)` — literal `".state"`,
  not `planlib.STATE_DIR` (see the PRD report: `plan.py` reassigns that name
  at module level later in the file, to an unrelated absolute path — using it
  here would have silently created nothing under the board).
- The module docstring's stale "`memos/` and `workflows/` are not made — a
  folder appears when its first file does" line was corrected to describe
  the new eager, idempotent five-directory creation.

**What is left**: nothing functional — every acceptance box below already
passed during the build. This spec exists to carry the change through
review and land it; an implementer re-runs the checks, confirms the diff
matches what is described above, and closes the boxes.

## Acceptance

- [x] `pearde init <empty-dir> --example` (via `resources/pearde.py`, the
      real CLI entrypoint) creates `<dir>/.pearde/prds/<name>/prd.md` for
      every example PRD (`asking`, `big`, `big/first`, `big/second`,
      `building`, `finished`, `landed`, `next`) — none of them at
      `<dir>/.pearde/<name>/`
- [x] `python3 resources/board/plan.py scan <dir>` on that board reports
      `8 PRDs` and lists each by its example-tree name, never `prds/`-prefixed
- [x] `<dir>/.pearde/README.md` does not exist — the example's own doc is
      excluded from the copy
- [x] a plain `pearde init <empty-dir>` (no `--example`) creates
      `<dir>/.pearde/{prds,memos,wiki,workflows,.state}` all five, empty
- [x] running `pearde init` twice on the same board is still a no-op the
      second time (idempotent — nothing raises, nothing is overwritten)

## Verify and Proof

```sh
bash prds/init-writes-a-board-on-the-pearde-layout/probe/check.sh
```

<!-- The probe script builds its own throwaway board(s) under mktemp -d,
     never under prds/, and exercises every box above. It already prints
     PASS as of this analysis round; rerun it to confirm before closing the
     boxes, and quote its output in the report. -->

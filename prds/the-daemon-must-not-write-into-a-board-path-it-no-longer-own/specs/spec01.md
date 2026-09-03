---
complexity: 8
footprint:
  - resources/board/plan.py
---

# spec01 — a read never creates a board

`state_dir()` is the one corner every writer on the board goes through, and it
ran `os.makedirs(<board>/.state)` unconditionally. `makedirs` creates every
intermediate directory, so the call did not merely make `.state` inside a board
that exists — it brought `<board>` itself into being at whatever path it was
handed. This unit makes that call refuse a path that carries no board, and
refuse in a shape the daemon already survives.

## What already stands

The orchestrator's checkout carries uncommitted work — a sibling's, spread over
seven board-finders — that adds `is_board_dir(p)` (a directory carrying
`settings.md` or `prds/`), points `board_at()` and `find_board()` at it, and
guards `state_dir()` with `if not os.path.isdir(board): die(...)`. That guard
already stops the plain case. It was copied into the lane and built on.

## What is left

Two things it does not do:

- It tests `os.path.isdir`, not `is_board_dir`, so it cannot heal a directory
  the defect has already made. Once `<project>/.pearde/.state/` exists, `isdir`
  is true for ever: the daemon keeps writing into the husk and it is never
  dropped. Observed live at `/Users/feb/dev/manola/.pearde`, which holds
  nothing but `.state/serve.json` and a 12.3 MB `.state/parse-cache.json`.
- It refuses with `die()`, which raises `SystemExit`. That is not an
  `Exception`, so it walks straight through `serve.py`'s `except Exception`
  watch-thread guard and through `save_entry`'s `except OSError` — one stale
  watch entry would stop every board the daemon holds.

## Acceptance

- [x] `plan.py` defines `NotABoard`, a subclass of `NotADirectoryError`, so every `except OSError` already on the board skips one board instead of dying.
- [x] `state_dir(board)` raises `NotABoard` when `is_board_dir(board)` is false, and creates nothing on that path — not `.state`, and not the board.
- [x] `state_dir(board)` still returns a created `<board>/.state` for a directory that carries a board.
- [x] A directory that exists but carries neither `settings.md` nor `prds/` is refused, so the husk the defect already left is not written into again.
- [x] `plan.py`'s CLI entry turns `NotABoard` into a one-line refusal through `die()`, not a traceback.
- [x] `migrate_legacy_state()` still skips a board that went away rather than raising — its `except (OSError, SystemExit)` covers the new type.

## Verify and Proof

```sh
bash pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh
python3 -m py_compile resources/board/plan.py
```

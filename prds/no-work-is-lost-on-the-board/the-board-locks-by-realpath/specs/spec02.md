---
complexity: 3
footprint:
  - resources/board/serve.py
---

# spec02 — the watch set is keyed by realpath, and the marker holds one name

`serve.register()` decides identity by `os.path.realpath`, so one physical
board reached two ways is ONE watch entry, under one name, with one
`.state/serve.json`. The second registration returns the FIRST holder
unchanged, so `ensure` prints the name and path the board is already watched
under rather than inventing `proj-2`.

**What already stands** (committed on the lane, probe claims A and B green as
of the second analyst pass 2026-09-03 21:34):
`register()` computes `real = os.path.realpath(path)` once and compares
`os.path.realpath(cur.path) == real` instead of `cur.path == path`, and the
docstring records why the SPELLING is still what is kept — `b.path` is the
caller's and is never rewritten, because `boards.board_link` needs
`os.path.dirname(board)` to keep matching the cwd every other check compares
it against. Realpath decides identity; it never rewrites a path. The
docstring now names the live case — a symlinked ancestor — and no longer the
retired compat symlink.

**What is left**: nothing in this spec. Verify the boxes against the lane and
return DONE.

## Acceptance

- [x] `register()` compares realpaths, not spellings, and computes the caller's realpath once — read: `real = os.path.realpath(path)` once, the loop compares `os.path.realpath(cur.path) == real`
- [x] Registering one board twice — by its own path and through a symlink to it — leaves exactly one entry in `BOARDS`, both calls answering to one name, the second returning `new=False` — probe claim A: `1: ['proj']`, `new=False, name=proj`, `'proj' vs 'proj'`
- [x] `b.path` is the caller's spelling, not the realpath: `register()` calls `os.path.abspath` and never assigns the realpath onto the Board — read: `b = Board(path)` from the abspath'd spelling; `real` is used for comparison only
- [x] `<board>/.state/serve.json` exists after the pair and records one name for the one realpath — probe claim B: file written at `…/proj/pearde/.state/serve.json`, records the realpath
- [x] The docstring names a symlinked ancestor, not the retired compat symlink, as the live case — read: docstring names `/tmp → /private/tmp on macOS` and says the spelling is kept because `boards.board_link` needs `os.path.dirname(board)` to keep matching the cwd
- [x] `python3 resources/memos.py verify` still reports every invariant `holds` — 6 holds; the 2 BROKEN lines (`no-harness-under-the-board-dispatches-it`, `a-pass-holds-its-turn-until-its-workers-are-in`) are inherited: both memos name scripts that exist nowhere on this tree, recorded by the analyst pass before my first edit, outside this footprint

## Verify and Proof

```sh
cd "$PEARDE_LANE"
python3 .pearde/prds/no-work-is-lost-on-the-board/the-board-locks-by-realpath/probe/probe.py --skill "$PWD"
python3 resources/memos.py verify
python3 resources/index.py check 2>&1 | grep 'board/serve.py' && exit 1 || true
```

---
complexity: 8
footprint:
  - resources/board/serve.py
---

# spec02 — the daemon revalidates a watch entry before it writes to it

The watch set is the daemon's whole configuration and it holds absolute paths
captured at registration. A board can move under one — `.pearde/` to `pearde/`,
this repo's own `92e318c` — and every writer keyed on `b.path` then aims at a
name the project has moved off. This unit makes the daemon check the ground
before it writes, and drop what no longer carries a board.

## What already stands

Nothing. `serve.py` is untouched in both the checkout and at HEAD.
`vanished()` drops a board on `not os.path.isdir(b.path)`, which the defect's
own write makes true for ever.

## What is left

- `entry_path()` built its path through `planlib.state_dir()`, so merely
  *naming* the marker created the board. It joins instead; `save_entry` makes
  the corner it is about to write into, and nothing else here needs it to exist.
- `save_entry()` checks `planlib.is_board_dir(b.path)` and returns without
  writing when the entry is stale.
- `drop_entry()` is a removal and only a removal — `forget` on a board that is
  gone must leave the ground where it stood untouched.
- `vanished()` drops on `not planlib.is_board_dir(b.path)`, so a husk goes too.

`parse_cache_save()` is the larger writer through the same stale path and is
**not** guarded here: spec01 puts the guard inside `state_dir()` itself, which
is what every one of these writers passes through. A fix that only guarded the
daemon's own two writers would have left the 12 MB one in place.

## Acceptance

- [x] `entry_path()` joins `<board>/.state/serve.json` and creates no directory — calling it on an absent board leaves the path absent.
- [x] `save_entry()` returns without writing when `b.path` no longer carries a board, and without raising, so one stale entry does not stop the tick.
- [x] `save_entry()` still records a board that is really there.
- [x] `drop_entry()` removes the marker without creating the directory it sits in.
- [x] `vanished()` drops a watch entry whose path carries no board, husk included, and says so on the log line.
- [x] The watch set is still the daemon's whole configuration — no machine-wide list of boards is added.

## Verify and Proof

```sh
bash pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh
python3 -m py_compile resources/board/serve.py
```

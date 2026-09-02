---
complexity: 10
footprint:
  - resources/board/machine.py
  - references/files.md
  - index.md
---

# spec01 — the machine frontier as one script, run from anywhere

`resources/board/machine.py` reads every board the daemon watches, merges their
PRDs into one dependency-ordered list, cuts it into waves of what could run at
once, and prints it. It writes nothing anywhere. `resources/pearde.py` finds it
through `COMMANDS`, so `pearde machine` works with no board above the cwd.

## What already stands

The probe at `.pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/machine.py`
is this file, working. It ran from `/tmp` and from `/`, discovered 10 watched
boards, merged 67 PRDs from 6 of them into 12 waves, and its `verify.sh`
passes 12 of 12. Discovery through `pearde.py` was proven in a scratch tree:
`pearde machine slots` ran from `/tmp` and `pearde machine` appeared in
`pearde help`.

## What is left

Move the probe to `resources/board/machine.py`; replace the hard-coded
`BOARD = "/Users/feb/dev/infra/pearde/resources/board"` with the file's own
directory; give it its row in `references/files.md` and a `@@machine` scope row
in `index.md`. Nothing else in the file changes.

## Acceptance

- [x] `resources/board/machine.py` exists and imports `plan` and `serve` from its own directory, not an absolute path
- [x] It defines `COMMANDS = {"machine": cmd_machine}` and `pearde machine` appears in `pearde help`
- [x] `cd / && python3 resources/board/machine.py machine` prints an order and exits 0 — no board above the cwd
- [x] The header reads `<n> of <m> board(s) · <k> PRDs on the frontier · <w> wave(s)`, and names the watched boards that contributed nothing
- [x] A row with no path in `/status` — the `all` page — is skipped with its reason printed, never counted as a board
- [x] A row already carrying a `board` is dropped, so a master's members are not counted twice
- [x] Every row is addressed `@<board>/<rel>` and carries its state, its mark, its priority and its weight
- [x] Only `open` and `specced` rows enter a wave; a `claimed`, `analyzing`, `question`, `blocked` or `deferred` row prints `waits` with its reason and appears in no wave
- [x] Two PRDs on different boards whose footprints `realpath` to one file never share a wave, and the later one prints `footprint clash with <addr>`
- [x] Footprints resolve from the board's parent directory, not `plan.prd_repo` — a board that is a git worktree otherwise resolves every path under `.pearde/`
- [x] `machine --json` emits `boards`, `rows`, `slots`, `reading`, `waves`, `skipped` and `notes`
- [x] `machine progress` prints exactly one line, in `@references/parts/progress.md`'s register
- [x] The ordering calls `plan.compute_plan` per board and adds no second arithmetic
- [x] A board that will not read is named in `notes` and the rest of the frontier still prints
- [x] `references/files.md` has a row for `resources/board/machine.py`; `index.md` has a `@@machine` scope row; `pearde index check` reports no new problem
- [x] The run leaves `git status --porcelain` unchanged

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
git status --porcelain > /tmp/before.txt
MACHINE_PY=resources/board/machine.py \
  bash .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh
python3 resources/pearde.py help | grep -q '^  pearde machine ' && echo "ok discovered"
(cd / && python3 /Users/feb/dev/infra/pearde/resources/board/machine.py machine >/dev/null) && echo "ok cold cwd"
python3 resources/index.py check
diff /tmp/before.txt <(git status --porcelain) && echo "ok moved nothing"
```

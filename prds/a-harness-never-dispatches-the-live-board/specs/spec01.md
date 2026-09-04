---
complexity: 9
footprint:
  - resources/board/run.py
  - resources/board/plan.py
---

# spec01 — the frontier has a read again, and the bare scope refuses

`run.py all` dispatched every board the daemon watches. It read to everyone who
wrote one as "print the frontier", because since the plan.py split that was the
only spelling left that printed one: `_merged_plan` — the branch routing
`plan all`, `plan <group>` and the four windows to `run.read_main` — was
dropped, leaving `read_main` with no caller anywhere in the tree, and
`pearde plan all` resolving `all` as a board path (`pearde: no .pearde/ board
at all`). Two of the three shipped skill files document `pearde plan all` and
`pearde plan work` as commands; they were not.

This unit puts the read back and closes the move behind its verb. Both halves
are needed: a refusal pointing at a command that does not exist is not a
repair, and it is what made the fan-out reasonable to write.

**Already stands**, uncommitted in the lane: `_merged_plan` and its `if cmd ==
"plan"` hook in `plan.py`, restored from 60f49d1 and adapted to the split
module (`find_board` now comes from `boards`); `script_main` in `run.py` and
the `__main__` line calling it. **Left:** review the two hunks, and check
nothing else in the tree invokes `run.py` as a script — `resources/` does not,
proved by grep; the three harnesses that do are spec03.

## Acceptance

- [x] `cd "$(git rev-parse --show-toplevel)" && python3 resources/board/plan.py plan slots` prints the slot count and its reading, and exits 0
- [x] `cd "$(git rev-parse --show-toplevel)" && python3 resources/board/plan.py plan all` prints `N of M board(s) · … PRDs on the frontier · … wave(s)`, a `wave 1:` line and rows addressed `@<board>/<rel>`
- [x] `plan groups`, `plan boards`, `plan progress` and `plan --json` each print their window; `plan progress` is exactly one line
- [x] `plan.py` names `read_main`, so the merged read has one implementation and not a second arithmetic
- [x] a bare `plan` with no scope and no window is still the cwd board's own page — `_merged_plan` returns `(False, 0)` and is not loaded
- [x] `cd "$(git rev-parse --show-toplevel)" && python3 resources/board/run.py all` exits non-zero, prints `refused`, and names both `pearde plan all` and `run.py run all`
- [x] `run.py --json`, `run.py progress` and any other bare word are refused the same way
- [x] `run.py run all --dry` still reaches `dispatch.main`, and `cmd_run(["all"])` — the path `pearde run all` takes through `COMMANDS` — still reaches it with the same arguments as before
- [x] the string `argv[0] == "run"` is still in `run.py`; a harness on this board greps for it

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)" && python3 resources/board/plan.py plan slots | grep -qE '^[0-9]+ slots \(.*ceiling '
cd "$(git rev-parse --show-toplevel)" && python3 resources/board/plan.py plan all | grep -qE '^wave 1: @'
[ "$(cd "$(git rev-parse --show-toplevel)" && python3 resources/board/plan.py plan progress | grep -c .)" = 1 ]
grep -q read_main resources/board/plan.py
set +e
out="$(cd "$(git rev-parse --show-toplevel)" && python3 resources/board/run.py all 2>&1)"
rc=$?
set -e
grep -q refused <<<"$out"
[ "$rc" -ne 0 ]
grep -q 'argv\[0\] == "run"' resources/board/run.py
MDIR=$PWD/resources/board python3 - <<'PY'
import os, sys
sys.path.insert(0, os.environ["MDIR"])
import run as m, dispatch as d
calls = []
d.main = lambda rest, **kw: calls.append((rest, sorted(kw))) or 0
assert m.script_main(["run", "all", "--dry"]) == 0 and calls == [(["--dry"], ["entries"])]
calls.clear()
assert m.script_main(["all"]) == 2 and calls == []
calls.clear()
assert m.cmd_run(["all"]) == 0 and calls == [([], ["entries"])]
print("PASS the verb dispatches, the bare scope does not, pearde run is unchanged")
PY
```

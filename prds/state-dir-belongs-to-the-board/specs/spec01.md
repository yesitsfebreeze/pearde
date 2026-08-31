---
complexity: 18
footprint:
  - resources/board/plan.py
  - resources/board/serve.py
  - resources/board/init.py
---

# spec01 — unbind the board's `.state` name from the machine's own

`resources/board/plan.py` bound `STATE_DIR` twice: `.state` (board-relative,
correct) near `BOARD_DIR`/`PRDS_DIR`, then rebound at the old line ~1296 to
the code repo's own `resources/board/state` for the calibration constant.
Because `state_dir()` reads the module global at call time, every call after
import returned the code-repo path regardless of which board it was handed —
`load_map`/`save_map` (`plan.json`) landed in the wrong repo, silently
merging every board's schedule into one file.

This spec has already been built and verified in place — it is done, not
proposed. `plan.py` now binds `STATE_DIR` exactly once (`.state`, line 61).
The machine-scoped corner — calibration, the guard's session cache, the
daemon's board registry — now goes through one differently-named constant,
`MACHINE_DIR` (defined once, right after `state_dir()`), and `CALIB_PATH`,
`GUARD_DIR` and `serve.py`'s `APP_DIR` all derive from it instead of each
re-deriving `os.path.dirname(__file__)/state` on their own.
`resources/board/init.py`'s literal `".state"` workaround (with its comment
naming this exact bug) is gone — it now writes `planlib.STATE_DIR` like every
other directory in that tuple.

Non-goals honored: `calibration.json`, `serve.json`, `serve.log` and
`guard/` still land under the same machine-scoped directory as before (now
named `MACHINE_DIR` rather than the leaked `STATE_DIR`), never under a
board. `PEARDE_GUARD_STATE` still overrides `GUARD_DIR` first. Nothing under
`.state/round.md`, `history.jsonl` or `transitions.jsonl` changed — those
were never on the leaking global. `resources/board/state/` is still
gitignored and still where the machine-scoped files land; it was never dead,
so nothing moved out of it — only `plan.json` moved out, back under the
board, per the PRD's own "the one thing that must move" line.

## Acceptance

- [x] `resources/board/plan.py` binds the name `STATE_DIR` exactly once.
      `grep -n "^STATE_DIR" resources/board/plan.py` returns one line, `61:STATE_DIR = ".state"`.
- [x] Importing `plan.py` and calling `state_dir(d)` for a fresh temp dir `d`
      returns a path under `d` and creates it there.
- [x] `pearde plan` (`plan.py plan <board>`) writes that board's `plan.json`
      under its own `.state/`, and leaves no `plan.json` in
      `resources/board/state/`.
- [x] `resources/board/init.py` no longer carries a literal `".state"`
      workaround or the comment naming this bug; it writes
      `planlib.STATE_DIR`.
- [x] `calibration.json`, `serve.json`, `serve.log` and `guard/` still
      resolve under the same machine-scoped directory as before this spec,
      `PEARDE_GUARD_STATE` still overrides the guard directory, and
      `resources/board/state/` is still listed in `.gitignore`.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
grep -n "^STATE_DIR" resources/board/plan.py
python3 -c "
import sys, tempfile, os
sys.path.insert(0, 'resources/board'); sys.path.insert(0, 'resources')
import plan
d = tempfile.mkdtemp()
r = plan.state_dir(d)
assert r == os.path.join(d, '.state'), r
assert os.path.isdir(r), 'not created'
assert plan.MACHINE_DIR == os.path.join(os.path.dirname(os.path.abspath(plan.__file__)), 'state')
assert plan.CALIB_PATH.startswith(plan.MACHINE_DIR)
assert plan.GUARD_DIR.startswith(plan.MACHINE_DIR)
print('state_dir/MACHINE_DIR OK')
"
python3 -c "
import re, sys, os
sys.path.insert(0, 'resources/board'); sys.path.insert(0, 'resources')
src = open('resources/board/plan.py', encoding='utf-8').read()
hits = re.findall(r'os\.path\.join\(STATE_DIR, ([^)]+)\)', src)
names = sorted(h.strip().strip(chr(34)).strip(chr(39)) for h in hits)
assert names == ['history.jsonl', 'round.md', 'transitions.jsonl'], names
print('STATE_DIR joins are board files only:', names)
import plan, serve
assert serve.APP_DIR == plan.MACHINE_DIR, serve.APP_DIR
assert serve.REG_PATH == os.path.join(plan.MACHINE_DIR, 'serve.json'), serve.REG_PATH
assert serve.LOG_PATH == os.path.join(plan.MACHINE_DIR, 'serve.log'), serve.LOG_PATH
print('serve.json/serve.log machine-scoped OK')
"
grep -c '\".state\"' resources/board/init.py | grep -qx 0 && echo "init.py: no literal .state left"
grep -qx 'resources/board/state/' .gitignore && echo "machine dir still gitignored"
T=$(mktemp -d); PEARDE_GUARD_STATE=$T python3 -c "
import sys, os
sys.path.insert(0, 'resources/board'); sys.path.insert(0, 'resources')
import plan, guard
assert plan.GUARD_DIR == os.environ['PEARDE_GUARD_STATE'], plan.GUARD_DIR
assert guard.STATE == os.environ['PEARDE_GUARD_STATE'], guard.STATE
print('PEARDE_GUARD_STATE still overrides both')
"
python3 -m py_compile resources/board/plan.py resources/board/serve.py resources/board/init.py
echo verify-ok
```

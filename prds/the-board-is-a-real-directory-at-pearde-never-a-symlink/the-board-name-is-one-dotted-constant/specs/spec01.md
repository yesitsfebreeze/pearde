---
complexity: 12
footprint:
  - resources/common.py
  - resources/guard.py
  - resources/board/boards.py
---

# spec01 — one Python module holds the board's name, and both remaining copies import it

`resources/common.py` is the one place the board's directory name and the walk
that finds a board are written. `resources/guard.py` and
`resources/board/boards.py` each carried a full copy of that block; both import
it instead. The two copies had already disagreed: `guard.py` spelled
`BOARD_DIR = "pearde"` with `.pearde` as its legacy, the exact inverse of the
planner, so on a project holding both directories the guard counted a session's
blocks against one board while `pearde scan` reported the other.

`common.py` is the right module and not a new one: it is stdlib-only, imports
nothing from `resources/board/`, and is already the resolver five readers stand
on. The guard runs inside a PreToolUse hook on every tool call, so what it
imports must be a module a broken planner cannot break — `common.py` is that,
and its import costs nothing next to interpreter start.

**What already stands** (built in the analysis pass, uncommitted in the lane):
all of it. `common.py` gained `PRDS_DIR`, `SETTINGS`, `STATE_DIR` and
`two_boards`; `guard.py` and `boards.py` lost their copies and re-export the
names they import, so `plan.py`'s import list and every caller are unchanged.

**What is left to finish**: nothing but review. Each file keeps its own
refusal — `boards.py` still wraps `board_scanned` in `die` (exit 2, `pearde:`
prefix) and `guard.py` still returns `None` on two boards rather than exiting,
because the guard has no opinion about a project it cannot name one board in.
Do not fold those wrappers into `common.py`: their differences are deliberate
and each is two lines.

## Acceptance

- [ ] Exactly one file under `resources/` matching `*.py` defines `BOARD_DIR`, and it is `resources/common.py`, where `BOARD_DIR` is `.pearde` and `LEGACY_BOARD_DIR` is `pearde`.
- [ ] `resources/guard.py` and `resources/board/boards.py` define none of `is_board_dir`, `board_link`, `named_boards`, `board_named`, `walk_up`, `two_boards`; each imports them from `common`.
- [ ] On a project holding both a real `.pearde/` board and a real `pearde/` board, `plan.find_board` and `guard.board_of` both answer `.pearde`.
- [ ] `guard.py` keeps its own `board_scanned` returning `None` on two boards, and `boards.py` keeps its own refusing through `die`; `plan.py`'s existing import list resolves unchanged.
- [ ] `python3 resources/index.py check` reports no problem naming any file in this footprint.

## Verify and Proof

```sh
# Every resolver names the same board — fixtures made at run time, in a temp
# dir, so this runs from a lane worktree that carries no board of its own.
R=$PWD; T=$(mktemp -d)
mk() { mkdir -p "$T/$1/$2/prds"; echo "language: English" > "$T/$1/$2/settings.md"; }
mk both .pearde; mk both pearde; mk legacy pearde; mk linked theboard; ln -s theboard "$T/linked/.pearde"
for c in both:.pearde legacy:pearde linked:theboard; do
  fx=${c%%:*}; want=${c##*:}
  py=$(cd "$T/$fx" && python3 -c "import sys,os;sys.path[:0]=['$R/resources','$R/resources/board'];import plan;print(os.path.basename(plan.find_board(None)))")
  gd=$(python3 -c "import sys,os;sys.path.insert(0,'$R/resources');import guard;print(os.path.basename(guard.board_of('$T/$fx')))")
  sh=$(. "$R/resources/board-name.sh"; basename "$(pearde_board_above "$T/$fx")")
  echo "$fx py=$py guard=$gd sh=$sh want=$want"
  [ "$py$gd$sh" = "$want$want$want" ] || { rm -rf "$T"; exit 1; }
done
rm -rf "$T"; echo "every resolver agrees"
python3 -c "import sys;sys.path.insert(0,'resources');sys.path.insert(0,'resources/board');import plan;print(plan.BOARD_DIR,plan.BOARD_DIRS,plan.SETTINGS,plan.PRDS_DIR,plan.STATE_DIR)"
python3 -c "import sys;sys.path.insert(0,'resources');import guard;print(guard.BOARD_DIR,guard.BOARD_DIRS)"
python3 resources/pearde.py scan | head -1
test "$(grep -rl '^BOARD_DIR *=' resources --include='*.py' | grep -vc pycache)" = 1
```

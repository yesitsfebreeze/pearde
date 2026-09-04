---
complexity: 12
footprint:
  - resources/board-name.sh
  - resources/doctor.sh
  - resources/statusline.sh
  - resources/graph/graph.sh
---

# spec02 — one shell file holds the same walk, and every shell reader sources it

`resources/board-name.sh` is the shell peer of `resources/common.py`: sourced,
never run, defining `PEARDE_BOARD_DIR`, `PEARDE_LEGACY_BOARD_DIR`,
`PEARDE_SCAN_SKIP` and the functions `pearde_is_board`, `pearde_board_named`,
`pearde_board_scanned`, `pearde_walk_up`, `pearde_board_above`. Three shell
readers walked their own copy — `doctor.sh`, `statusline.sh` and
`graph/graph.sh` — and the copies had drifted three ways: all three tried the
legacy `pearde/` before `.pearde/`; `statusline.sh` took `settings.md` as the
only marker where `doctor.sh` took either marker; and `statusline.sh` carried a
bare `prds/` fallback the other readers dropped.

That fallback was not harmless. Standing anywhere inside a board,
`statusline.sh` resolved to `<board>/prds` rather than to the board, so it read
no `settings.md`, found no `members:` and silently dropped a master board's
members. On the fixture it reported `2/2 100%` where `pearde scan` reported one
open PRD.

No install change is needed: `install.sh` links `resources` as a whole
directory, so a new file under it is present in every install already —
measured, not assumed.

**What already stands** (built in the analysis pass, uncommitted in the lane):
all of it. `board-name.sh` written; `doctor.sh` keeps its four short local
aliases onto the shared functions so the rest of that 1000-line file reads as it
did; `statusline.sh`'s two hand-written climbs replaced by one
`pearde_board_above` call plus the `!two` guard; `graph.sh`'s two-line
preference replaced by `pearde_board_named` with `PEARDE_BOARD_DIR` as the
fallback for a folder holding no board.

**What is left to finish**: nothing but review. Keep the `!two …` sentinel
string: every caller reads these through `$(…)`, where a variable set inside the
subshell never comes back, so ambiguity has to travel on stdout. `statusline.sh`
renders no board segment on it, and `doctor.sh` reports it.

## Acceptance

- [ ] `resources/board-name.sh` exists, is sourced-only (defines no top-level command), passes `bash -n`, and sets `PEARDE_BOARD_DIR` to `.pearde` with `pearde` as the legacy name tried second.
- [ ] Exactly one file under `resources/` defines `pearde_board_named`; `doctor.sh`, `statusline.sh` and `graph/graph.sh` each source `board-name.sh` and define no walk of their own.
- [ ] On a project holding both a real `.pearde/` and a real `pearde/` board, the shell walk answers `.pearde`, and the status line's second line reports the same counts `pearde scan` reports.
- [ ] Standing inside the board directory itself, `statusline.sh` resolves to the board and not to `<board>/prds` — a master board's member counts appear where they previously did not.
- [ ] `bash resources/doctor.sh` prints no row that was green before this change and is broken after it.

## Verify and Proof

```sh
bash -n resources/board-name.sh && bash -n resources/doctor.sh && bash -n resources/statusline.sh && bash -n resources/graph/graph.sh
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
test "$(grep -rl '^pearde_board_named()' resources --include='*.sh' | wc -l | tr -d ' ')" = 1
for f in doctor.sh statusline.sh graph/graph.sh; do grep -q 'board-name\.sh' "resources/$f" || exit 1; done
echo '{"current_dir":"'"$PWD"'"}' | bash resources/statusline.sh
# doctor is a board-wide gate that was already red on rows outside this
# footprint before the first edit (index, vault, origin, health, knowledge —
# base-doctor.txt holds the same rows) — capture it, then gate only on the
# rows this unit's files feed, never on doctor's own exit, which pipefail
# would otherwise carry.
dout=$(bash resources/doctor.sh 2>&1) && drc=0 || drc=$?
[ -n "$dout" ] || exit 1
rows=$(printf '%s\n' "$dout" | grep -E '^  (statusline|board|guard) ')
printf '%s\n' "$rows"
n=$(printf '%s\n' "$rows" | { grep -cE 'broken|stale'; } || true)
if [ "$n" != 0 ]; then exit 1; fi
```

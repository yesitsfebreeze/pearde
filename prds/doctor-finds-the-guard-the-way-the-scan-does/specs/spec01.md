---
complexity: 8
footprint:
  - resources/doctor.sh
---

# spec01 — doctor's guard row walks for `.pearde/`, not a literal `prds/`

`doctor.sh`'s `guard` row locates the board's `.claude/settings.json` by
walking up from `$START` looking for a literal `d/prds` directory — the
pre-migration board layout. On a machine that keeps other projects'
old-layout boards as siblings of the current repo, that walk climbs past
this repo's own `.pearde/` and settles on the *other* project's
`.claude/settings.json`, so the guard probe runs with the wrong `cwd` and
never sees a deny — `doctor` then reports `guard broken` on a perfectly
wired install. This already stands fixed in the tree from the probe: the
walk now looks for `d/.pearde` (the same test `board_of` in
`resources/guard.py` and `find_board` in `resources/board/plan.py` use),
with the same dirname-fixpoint guard the `board` row below it already uses
— which also stops the walk hanging when `$START` is a relative path such
as `.` (`dirname` of `.` is `.` forever without the fixpoint check).

## Acceptance

- [x] `doctor.sh`'s guard-row walk finds `.pearde/`, not `prds/` — matches
      `resources/guard.py`'s `board_of` and `resources/board/plan.py`'s
      `find_board`.
- [x] Run from `/Users/feb/dev/infra/pearde`, where a sibling
      `/Users/feb/dev/infra/prds` (another project's old-layout board)
      previously hijacked the walk: `doctor` reports `guard ok`, not
      `guard broken`.
- [x] Run with a relative `$START` (e.g. `.`): the walk terminates (no
      hang) and still reports `guard ok`.

## Verify and Proof

```sh
# box 1 — the guard row's walk makes the same test as `board_of`
# (resources/guard.py) and `find_board` (resources/board/plan.py): the
# nearest ancestor holding `.pearde/`. Two occurrences in doctor.sh — the
# guard row and the `board` row below it, now walking alike.
n=$(grep -c '\[ -d "$d/\.pearde" \]' resources/doctor.sh || true)
[ "$n" = 2 ] || { echo "WALK_MISMATCH n=$n"; exit 1; }
grep -q 'BOARD_DIR = "\.pearde"' resources/guard.py || { echo NO_BOARD_DIR_GUARD; exit 1; }
grep -q 'BOARD_DIR = "\.pearde"' resources/board/plan.py || { echo NO_BOARD_DIR_PLAN; exit 1; }
f=$(grep -c 'p=$(dirname "$d"); \[ "$p" = "$d" \] && break; d="$p"' resources/doctor.sh || true)
[ "$f" = 2 ] || { echo "NO_FIXPOINT_GUARD f=$f"; exit 1; }
echo WALK_IS_PEARDE

# box 2 — absolute $START, with the sibling old-layout board a level up
out=$(bash resources/doctor.sh /Users/feb/dev/infra/pearde 2>&1 || true)
row=$(printf '%s\n' "$out" | grep -E '^  guard ' || true)
echo "abs: $row"
case "$row" in
  *"guard       ok"*) echo GUARD_ROW_OK_ABS ;;
  *) echo GUARD_ROW_FAIL_ABS; exit 1 ;;
esac

# box 3 — relative $START: terminates (a watchdog proves no hang) and is ok
t=$(mktemp); bash resources/doctor.sh . >"$t" 2>&1 & p=$!
# the watchdog is detached from this block's stdout: a `sleep` that outlives
# the kill must not hold the pipe `collect` reads, or the block stalls 120s
# after doing its work.
( sleep 120; kill -9 $p ) >/dev/null 2>&1 </dev/null & w=$!
wait $p || true
kill -9 $w >/dev/null 2>&1 || true
wait $w 2>/dev/null || true
row=$(grep -E '^  guard ' "$t" || true)
rm -f "$t"
echo "rel: $row"
case "$row" in
  *"guard       ok"*) echo GUARD_ROW_OK_REL ;;
  *) echo GUARD_ROW_FAIL_REL; exit 1 ;;
esac

echo VERIFY_DONE
```

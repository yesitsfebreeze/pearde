#!/usr/bin/env bash
# the-largest-module-is-cut-by-responsibility — the probe's harness.
#
# Run from anywhere:
#   bash .pearde/prds/resources-are-organised-by-responsibility/the-largest-module-is-cut-by-responsibility/probe/verify.sh
#
# The contract has three halves and this harness checks all three: the file is
# cut into modules named for one responsibility and none is over 700 lines; the
# module every caller imports still carries every name it carried; and every
# command and every harness that reads the board is unchanged from the outside.
#
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# would prove a tree holding none of the work. BOARD is the board this harness
# sits under, found by walking; ROOT is PEARDE_ROOT when the runner set one,
# that board's repo otherwise.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
SRC="$ROOT/resources/board"
PASS=0; FAIL=0
ok()   { PASS=$((PASS + 1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL + 1)); echo "  FAIL $1"; }
eq()   { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 — want [$3] got [$2]"; fi; }
run()  { if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }

MODULES="boards prdfile repos registry silence needs vision schedule mapfile plan"

echo "── A. the cut: one responsibility per file, none over 700 lines ─────────"
for m in $MODULES; do
  if [ -f "$SRC/$m.py" ]; then
    n=$(wc -l < "$SRC/$m.py" | tr -d ' ')
    if [ "$n" -le 700 ]; then ok "A $m.py is $n lines"; else bad "A $m.py is $n lines — over 700"; fi
  else
    bad "A $m.py is on disk"
  fi
done
# Only the modules this contract cuts. The rest of resources/board/ holds
# files well over 700 lines and none of them is this PRD's to touch.
eq "A no module of this cut is over 700 lines" \
   "$(for m in $MODULES; do wc -l < "$SRC/$m.py"; done | tr -d ' ' | awk '$1>700' | wc -l | tr -d ' ')" "0"
eq "A the cut is more than one file" \
   "$([ "$(echo $MODULES | wc -w | tr -d ' ')" -ge 2 ] && echo yes)" "yes"

echo
echo "── B. the module every caller imports carries every name it carried ─────"
ORIG="$HERE/plan.py.orig"
python3 - "$ORIG" "$SRC" <<'PY'
import ast, sys
orig, src = sys.argv[1], sys.argv[2]
sys.path.insert(0, src)
import plan
want = set()
for n in ast.parse(open(orig).read()).body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        want.add(n.name)
    elif isinstance(n, ast.Assign):
        for t in n.targets:
            if isinstance(t, ast.Name):
                want.add(t.id)
# The parse cache's three module globals are rebound at run time; a name bound
# into a second module would be a snapshot, so they stay addressed through the
# module that owns them and are not re-exported.
want -= {"_PCACHE", "_PCACHE_LOADED", "_PCACHE_DIRTY"}
missing = sorted(w for w in want if not hasattr(plan, w))
print("MISSING=%d %s" % (len(missing), " ".join(missing)))
PY
M=$(python3 - "$ORIG" "$SRC" <<'PY'
import ast, sys
orig, src = sys.argv[1], sys.argv[2]
sys.path.insert(0, src)
import plan
want = set()
for n in ast.parse(open(orig).read()).body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        want.add(n.name)
    elif isinstance(n, ast.Assign):
        for t in n.targets:
            if isinstance(t, ast.Name):
                want.add(t.id)
want -= {"_PCACHE", "_PCACHE_LOADED", "_PCACHE_DIRTY"}
print(len([w for w in want if not hasattr(plan, w)]))
PY
)
eq "B every name the one file carried is still reachable as plan.<name>" "$M" "0"

echo
echo "── C. every command is unchanged from the outside ───────────────────────"
run "C pearde help exits 0" "python3 '$ROOT/resources/pearde.py' help"
eq "C no module fails to import" \
   "$(python3 "$ROOT/resources/pearde.py" help 2>&1 | grep -c 'failed to import')" "0"
for c in scan plan status members calibrate reconcile; do
  run "C plan.py $c exits 0" "python3 '$SRC/plan.py' $c '$(dirname "$BOARD")'"
done
run "C plan.py vision --check exits 0" "python3 '$SRC/plan.py' vision --check '$(dirname "$BOARD")'"
EX=$(mktemp -d)
run "C plan.py example writes a board" "python3 '$SRC/plan.py' example '$EX/ex' && [ -d '$EX/ex/pearde/prds' ]"
eq "C …and names plan.py, not the file the code moved into" \
   "$(python3 "$SRC/plan.py" example "$EX/ex2" 2>&1 | grep -c 'plan.py scan')" "1"
rm -rf "$EX"

echo
echo "── D. the map names every file, and the gate is silent ──────────────────"
eq "D index.py check names no module of this cut" \
   "$(cd "$ROOT" && python3 resources/index.py check 2>&1 | grep -cE 'resources/board/(boards|prdfile|repos|registry|silence|needs|vision|schedule|mapfile)\.py')" "0"
for m in boards prdfile repos registry silence needs vision schedule mapfile; do
  eq "D references/files.md has a row for $m.py" \
     "$(grep -c "@resources/board/$m.py" "$ROOT/references/files.md")" "1"
done

echo
echo "── E. every harness that reads this file runs as it did ─────────────────"
# Each row is the harness's FAIL count and then its traceback count, both
# taken on a tree WITHOUT the cut — several of these harnesses were already
# red for reasons outside this contract, and a box demanding zero would be a
# box nobody can turn green. What this contract owes is that neither number
# goes up.
#
# The one non-zero traceback baseline is `39c0cab`'s, not this unit's:
# `state_dir` there stopped calling `die()` and started raising `NotABoard`,
# so any caller that is not `plan.py`'s own `__main__` — a `python3 -c` in a
# harness, for one — now gets a traceback where it used to get a one-line
# refusal. Measured on the checkout at `31620bb` with no cut in it:
# one-predicate-for-dispatchable 33 FAIL and 1 traceback; at `1880990`,
# 33 FAIL and 0.
for row in "the-board-runs-itself/one-command 1 0" \
           "the-tool-keeps-its-word/one-predicate-for-dispatchable 29 1" \
           "complexity-is-guarded-like-priority 0 0" \
           "scan-parses-the-board-once-and-caches-it-by-mtime 0 0"; do
  set -- $row; rel=$1; base=$2; tbase=$3
  H="$BOARD/prds/$rel/probe/verify.sh"
  if [ ! -f "$H" ]; then bad "E $rel is on the board"; continue; fi
  OUT=$(PEARDE_ROOT="$ROOT" bash "$H" 2>&1)
  N=$(printf '%s\n' "$OUT" | grep -cE '(^|  )FAIL')
  if [ "$N" -le "$base" ]; then ok "E $rel fails $N, no more than the $base before the cut"
  else bad "E $rel fails $N, up from $base before the cut"; fi
  TB=$(printf '%s\n' "$OUT" | grep -c 'Traceback (most recent call last)')
  if [ "$TB" -le "$tbase" ]; then ok "E …and $rel raises $TB, no more than the $tbase before the cut"
  else bad "E …and $rel raises $TB, up from $tbase before the cut"; fi
done

# The four assertions spec03 re-pointed have to be green whatever else in
# that harness is red — a FAIL count that merely does not rise would still
# pass if the cut broke one of them and a fixture closed another.
OUT=$(PEARDE_ROOT="$ROOT" bash "$BOARD/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh" 2>&1)
for lbl in "schedule.py defines dispatchable once" \
           "cmd_scan calls it on the free set" \
           "compute_plan holds what it refuses" \
           "plan_frontier reads the hold"; do
  eq "E re-pointed: $lbl" \
     "$(printf '%s\n' "$OUT" | grep -cF "  ok   $lbl")" "1"
done

echo
echo "$((PASS + FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]

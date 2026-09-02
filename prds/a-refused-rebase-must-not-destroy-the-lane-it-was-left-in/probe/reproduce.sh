#!/usr/bin/env bash
# Reproduces the refused-rebase-destroys-the-lane bug and proves the fix in
# resources/board/lanes.py's merge(). Builds two clean-room repos (never
# under .pearde/prds/) and calls the SAME lanes.merge() against both:
#   1. the lane is ahead by a real commit, but ALSO carries an uncommitted
#      change on a path the rebase never touches — the `land_lane` shape,
#      where footprint files are committed and outside-footprint dirt is
#      left standing. `git rebase` refuses to even start on a dirty tree,
#      so this is never a real conflict.
#   2. a genuine mid-rebase conflict, to prove the reset that restores the
#      branch/tree still runs when a rebase actually gets under way.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
# The tree under test is the runner's when it names one. A worker builds in
# a lane worktree that carries no board of its own, so a walk up from $0
# always lands in the orchestrator's checkout and a green run would prove a
# tree holding none of the work. ROOT is PEARDE_ROOT when the runner set
# one, the repo above this board otherwise — probe -> <prd> -> prds ->
# board -> repo. LANES_PY names one file directly, overriding both.
ROOT="${PEARDE_ROOT:-$(cd "$HERE/../../../.." && pwd)}"
LANES="${LANES_PY:-$ROOT/resources/board/lanes.py}"
PASSED=0; FAILED=0
pass() { PASSED=$((PASSED + 1)); echo "PASS: $1"; }
fail() { FAILED=$((FAILED + 1)); echo "FAIL: $1"; }
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

run_merge() {  # $1 repo path  $2 slug
  python3 - "$LANES" "$1" "$2" <<'PY'
import sys, importlib.util
spec = importlib.util.spec_from_file_location("lanes", sys.argv[1])
lanes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lanes)
repo, slug = sys.argv[2], sys.argv[3]
try:
    lanes.merge(repo, slug)
    print("merge() returned without raising")
except lanes.LaneError as e:
    print("merge() raised:", e)
PY
}

echo "== case 1: refused rebase (dirty tree, no real conflict) =="
cd "$WORK"
git init -q repo
cd repo
git config user.email t@t.com; git config user.name t
git config rebase.autostash false
echo base > tracked.txt; echo other > other.txt
git add -A; git commit -qm base
git branch lane/x
git worktree add -q ../lane_wt lane/x
cd ../lane_wt
git config rebase.autostash false
echo lanechange >> tracked.txt
git add tracked.txt
git commit -qm "lane commit (footprint)"
echo "dirty-uncommitted-outside-footprint" >> other.txt   # land_lane leaves this standing
cd ../repo
echo mainchange >> other.txt        # advance HEAD on a path the lane never committed
git add -A; git commit -qm advance
cd "$WORK"

run_merge "$WORK/repo" x

echo "-- lane_wt state after the refusal --"
cd lane_wt
git status --porcelain
if grep -q "dirty-uncommitted-outside-footprint" other.txt; then
  pass "the lane's uncommitted dirt survived the refused rebase"
else
  fail "the lane's uncommitted dirt was destroyed"
fi
cd "$WORK"

echo
echo "== case 2: a genuine mid-rebase conflict still resolves cleanly =="
git init -q repo2
cd repo2
git config user.email t@t.com; git config user.name t
git config rebase.autostash false
echo base > f.txt
git add -A; git commit -qm base
git branch lane/y
git worktree add -q ../lane_wt2 lane/y
cd ../lane_wt2
git config rebase.autostash false
echo lane-change > f.txt
git add -A; git commit -qm "lane change"
cd ../repo2
echo main-change > f.txt
git add -A; git commit -qm "main change (conflicting)"
cd "$WORK"

run_merge "$WORK/repo2" y

cd lane_wt2
echo "-- lane_wt2 state after the conflict --"
git status --porcelain
WAS="$(cd ../repo2 && git rev-parse lane/y)"
NOW="$(git rev-parse HEAD)"
if [ "$WAS" = "$NOW" ]; then
  pass "branch/tree restored to the pre-rebase tip"
else
  fail "branch left at $NOW, expected $WAS"
fi

# The tally is printed, never a total a spec can lock shut; the exit is the
# assertion, so a FAIL line cannot be printed into a green run.
echo
echo "$((PASSED + FAILED)) cases · $PASSED pass · $FAILED fail"
[ "$FAILED" = 0 ]

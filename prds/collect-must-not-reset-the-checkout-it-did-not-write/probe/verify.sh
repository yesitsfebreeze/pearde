#!/usr/bin/env bash
# collect-must-not-reset-the-checkout-it-did-not-write — the probe's harness.
#
# The failure: `collect`'s rollback ran `git reset --hard` in the
# orchestrator's own checkout, so a red verify block destroyed every
# uncommitted change standing there — including work no PRD on the board
# had claimed. It ran even when `land_lane` merged nothing.
#
# Each fixture is a copy of `resources/board/example` under its own
# `git init`, with a lane cut by `lanes.create` exactly as `claim` cuts
# one. Section A reproduces both faults on the code as it stood at
# $PINNED (`git show` into scratch — the tree is never checked out);
# sections B and C measure the tree's own `resources/board/collect.py`.
# One line per assertion, a count at the end.
set -u
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
COLLECT="$ROOT/resources/board/collect.py"
EXAMPLE="$ROOT/resources/board/example"
PINNED=3587817                # the last commit before this probe's edits
PASS=0; FAIL=0
export PEARDE_PORT=1          # nothing listens there — the daemon is "down"
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@x \
       GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@x

ok()   { PASS=$((PASS+1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL $1"; [ -n "${2:-}" ] && echo "       got:  $2"; [ -n "${3:-}" ] && echo "       want: $3"; return 0; }
eq()   { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "$2" "$3"; fi; }
has()  { if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1" "$2" "contains: $3"; fi; }
lacks(){ if printf '%s' "$2" | grep -qF -- "$3"; then bad "$1" "$2" "without: $3"; else ok "$1"; fi; }

TOP="$(mktemp -d)"; W="$(mktemp -d)"
trap 'for d in "$TOP"/*/; do [ -d "$d/.git" ] && git -C "$d" worktree prune >/dev/null 2>&1; done; rm -rf "$TOP" "$W"' EXIT

# ── the pinned collect, in its own resources/ layout ─────────────────────────
OLD="$W/old/resources"; mkdir -p "$OLD/board"
for f in $(git -C "$ROOT" ls-tree -r --name-only "$PINNED" resources/ \
           | grep '^resources/\(board/\)\?[^/]*\.py$'); do
  git -C "$ROOT" show "$PINNED:$f" > "$OLD/${f#resources/}"
done

run()     { ( cd "$D" && PEARDE_AS=engineer python3 "$COLLECT" --board "$D/.pearde" "$@" ) 2>&1; }
run_old() { ( cd "$D" && PEARDE_AS=engineer python3 "$OLD/board/collect.py" --board "$D/.pearde" "$@" ) 2>&1; }
head_of() { ( cd "$D" && git rev-parse HEAD ); }
short()   { ( cd "$D" && git rev-parse --short "${1:-HEAD}" ); }
dirt()    { ( cd "$D" && git status --porcelain -- "$1" ); }
fm()      { grep -m1 "^$2:" "$D/.pearde/prds/$1/prd.md" | sed "s/^$2: *//"; }

# ── the fixture: the example board, its own repo, a lane, and a neighbour ────
# `verify` is the spec's verify block — `false` is the red this PRD is about.
# `landed` says whether the lane holds a commit to merge: "yes" writes the
# worker's file into the lane, "no" leaves the lane empty so `land_lane`
# merges nothing.
fixture() {   # fixture <name> <verify> <landed>
  D="$TOP/$1"; mkdir -p "$D/.pearde"; cp -R "$EXAMPLE/." "$D/.pearde/"
  mkdir -p "$D/.pearde/.state"
  python3 - "$D/.pearde/prds/finished/specs/spec01.md" "$2" <<'EOF'
import re, sys
p, cmd = sys.argv[1], sys.argv[2]
t = open(p).read()
open(p, "w").write(re.sub(r"```sh\n.*?```", "```sh\n%s\n```" % cmd, t, flags=re.S))
EOF
  # the neighbour: a tracked file NO PRD on this board names, committed
  # clean and then edited. `reset --hard` destroys it; nothing else does.
  mkdir -p "$D/other"; echo "committed" > "$D/other/neighbour.txt"
  # `finished`'s footprint, tracked and empty — so the lane's edit to it
  # reads as ` M src/util.py` and `land_lane` sees it inside the footprint
  mkdir -p "$D/src"; echo "# empty" > "$D/src/util.py"
  find "$D" -type f -exec touch {} +
  ( cd "$D" && git init -q -b main && git add -A && git commit -q -m fixture )
  python3 - "$D" "$ROOT" "$3" <<'EOF'
import os, sys
d, root, landed = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(root, "resources", "board"))
import lanes
lane = lanes.create(os.path.join(d, ".pearde"), d, "finished")
if landed == "yes":
    os.makedirs(os.path.join(lane, "src"), exist_ok=True)
    open(os.path.join(lane, "src", "util.py"), "w").write(
        "def helper():\n    return 1\n")
EOF
  echo "the neighbour's uncommitted work" > "$D/other/neighbour.txt"
}

# ═══ A. reproduced at $PINNED ════════════════════════════════════════════════
echo "A. reproduced at $PINNED: a red verify block deletes the checkout's own work"
fixture a1 false yes
BEFORE="$(head_of)"
OUT="$(run_old finished)"; RC=$?
eq  "A1 the old collect exits 1 on the red" "$RC" "1"
has "A1 ...and says the checkout went back" "$OUT" "lane unmerged — checkout back at"
eq  "A1 the neighbour's uncommitted work is GONE" \
    "$(cat "$D/other/neighbour.txt")" "committed"
eq  "A1 ...and nothing said what was being discarded" \
    "$(printf '%s' "$OUT" | grep -c 'other/neighbour.txt')" "0"

echo "A. reproduced at $PINNED: it resets even when the merge merged nothing"
fixture a2 false no
BEFORE="$(head_of)"
OUT="$(run_old finished)"; RC=$?
eq  "A2 the old collect exits 1" "$RC" "1"
has "A2 ...and still says the checkout went back" "$OUT" "lane unmerged — checkout back at"
eq  "A2 nothing had been merged" "$(head_of)" "$BEFORE"
eq  "A2 the neighbour's work is GONE for a merge that never happened" \
    "$(cat "$D/other/neighbour.txt")" "committed"

# ═══ B. the tree: the rollback keeps what it did not write ═══════════════════
echo "B. a red verify block leaves the checkout's own work standing"
fixture b1 false yes
BEFORE="$(head_of)"
OUT="$(run finished)"; RC=$?
eq  "B1 exit 1 on the red — the gate still refuses" "$RC" "1"
eq  "B1 the neighbour's uncommitted work is still there" \
    "$(cat "$D/other/neighbour.txt")" "the neighbour's uncommitted work"
eq  "B1 the checkout is back on the commit before the merge" "$(head_of)" "$BEFORE"
lacks "B1 the lane's code does not stand in the checkout" \
    "$( [ -f "$D/src/util.py" ] && cat "$D/src/util.py" )" "def helper"
has "B1 the line names what it discarded" "$OUT" "1 commit(s)"
eq  "B1 the lane branch still holds the worker's commit" \
    "$( cd "$D" && git rev-list --count HEAD..lane/finished )" "1"
eq  "B1 the PRD is still claimed" "$(fm finished state)" "claimed"

echo "B. nothing merged: nothing is rolled back"
fixture b2 false no
BEFORE="$(head_of)"
OUT="$(run finished)"; RC=$?
eq  "B2 exit 1 on the red" "$RC" "1"
lacks "B2 no rollback line — there was no merge to undo" "$OUT" "lane unmerged"
eq  "B2 the checkout never moved" "$(head_of)" "$BEFORE"
eq  "B2 the neighbour's work is untouched" \
    "$(cat "$D/other/neighbour.txt")" "the neighbour's uncommitted work"

echo "B. a green verify block is unaffected"
fixture b3 true yes
OUT="$(run finished)"; RC=$?
eq  "B3 exit 0" "$RC" "0"
eq  "B3 done" "$(fm finished state)" "done"
eq  "B3 the worker's code landed" \
    "$( cd "$D" && git show HEAD~1:src/util.py | head -1 )" "def helper():"
eq  "B3 the neighbour's work is still uncommitted, and still there" \
    "$(dirt other/neighbour.txt)" " M other/neighbour.txt"

# ═══ C. dirt the rollback cannot keep is refused, never discarded ════════════
echo "C. a rollback that cannot keep the work refuses, and says so"
# the verify block writes into the merged file before it goes red — real,
# and the one way a merged path is dirty by the time the rollback runs.
# `--keep` refuses rather than discarding it, and collect obeys.
fixture c1 'printf "half-written output\n" >> src/util.py
false' yes
OUT="$(run finished)"; RC=$?
eq  "C1 exit 1" "$RC" "1"
has "C1 the verify block's half-written output survives" \
    "$(cat "$D/src/util.py")" "half-written output"
has "C1 collect named the refusal" "$OUT" "not rolled back"
has "C1 ...and gave the command that finishes it" "$OUT" "reset --keep"
eq  "C1 the neighbour's work survives too" \
    "$(cat "$D/other/neighbour.txt")" "the neighbour's uncommitted work"
eq  "C1 the lane branch still holds the worker's commit" \
    "$( cd "$D" && git rev-parse lane/finished )" "$(head_of)"
eq  "C1 the PRD is still claimed" "$(fm finished state)" "claimed"

# ═══ Z. hygiene ══════════════════════════════════════════════════════════════
echo "Z. hygiene"
eq  "Z no fixture committed a lane worktree dir" \
    "$(for d in "$TOP"/*/; do [ -d "$d/.git" ] && ( cd "$d" && git log --name-only --format= ); done | grep -c '\.pearde/\.lanes/')" "0"

echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" -eq 0 ]

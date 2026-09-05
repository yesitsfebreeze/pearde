#!/usr/bin/env bash
# looptest — the loop's flow, measured in real git. Section 1–3: red is a
# queue, not a wall — `collect` (conflict) → `failed` → `retry` → `claim` →
# `brief`:
#
#   1  a lane whose rebase conflicts lands `failed`, `## Failure` names the
#      lane branch, the branch it would not land on and git's files;
#   2  `next` prints `retry` above `spec ahead` / `implement`;
#   3  `retry` lands `specced` (the specs stand), `claim` re-uses the lane,
#      and the brief carries the failure verbatim and the rebase to do.
#
# Fixture: a copy of resources/board/example under its own `git init`, the
# lane cut by `lanes.create` exactly as `claim` cuts one, and both the lane
# and the checkout committing the same line of src/util.py. Real git, no
# faked state. Run: bash resources/board/looptest.sh — exit 0 is green.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"
PY="$ROOT/resources/board"
export PEARDE_PORT=1 PEARDE_AS=engineer
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@x \
       GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@x
FAIL=0
ok()  { echo "  ok   $1"; }
bad() { FAIL=1; echo "  FAIL $1"; [ -n "${2:-}" ] && printf '       got: %s\n' "$2"; return 0; }
eq()  { [ "$2" = "$3" ] && ok "$1" || bad "$1 (want: $3)" "$2"; }
has() { printf '%s' "$2" | grep -qF -- "$3" && ok "$1" || bad "$1 (want: $3)" "$2"; }

TOP="$(mktemp -d)"
D="$TOP/board"
trap 'git -C "$D" worktree prune >/dev/null 2>&1; rm -rf "$TOP"' EXIT

mkdir -p "$D/.pearde/.state" "$D/src"
cp -R "$DIR/example/." "$D/.pearde/"
python3 - "$D/.pearde/prds/finished/specs/spec01.md" <<'PY'
import re, sys
p = sys.argv[1]; t = open(p).read()          # a green verify that CAN fail: only the merge goes red
open(p, "w").write(re.sub(r"```sh\n.*?```", "```sh\ntest -f src/util.py\n```", t, flags=re.S))
PY
printf 'base\n' > "$D/src/util.py"
( cd "$D" && git init -q -b main && git add -A && git commit -q -m fixture )
python3 - "$D" "$PY" <<'PY'
import os, sys
d, py = sys.argv[1], sys.argv[2]
sys.path.insert(0, py)
import lanes
lane = lanes.create(os.path.join(d, ".pearde"), d, "finished")
open(os.path.join(lane, "src", "util.py"), "w").write("the worker's line\n")
PY
printf 'main moved on\n' > "$D/src/util.py"
( cd "$D" && git add -- src/util.py && git commit -q -m "main moves src/util.py" )
PRD="$D/.pearde/prds/finished/prd.md"
fm() { grep -m1 "^$1:" "$PRD" | sed "s/^$1: *//"; }

echo "1. a conflicting lane lands failed"
OUT="$( cd "$D" && python3 "$PY/collect.py" --board "$D/.pearde" finished 2>&1 )"; RC=$?
eq  "collect exits 1" "$RC" 1
eq  "state is failed" "$(fm state)" failed
FAILURE="$(sed -n '/^## Failure/,/^## /p' "$PRD")"
has "## Failure names the file" "$FAILURE" "src/util.py"
has "## Failure names the lane" "$FAILURE" "lane/finished"
has "## Failure names the branch it would not land on" "$FAILURE" "on \`main\`"
eq  "no claim left" "$(fm claim)" ""
eq  "no ## Blocked written" "$(grep -c '^## Blocked' "$PRD")" 0

echo "2. next puts retry before new work"
NEXT="$( cd "$D" && python3 "$PY/plan.py" next "$D/.pearde" 2>&1 )"
R=$(printf '%s\n' "$NEXT" | grep -n 'retry — ' | head -1 | cut -d: -f1)
S=$(printf '%s\n' "$NEXT" | grep -n 'spec ahead\|implement — ' | head -1 | cut -d: -f1)
[ -n "$R" ] && ok "next prints a retry step" || bad "next prints a retry step" "$NEXT"
[ -n "$S" ] && ok "next prints spec ahead" || bad "next prints spec ahead" "$NEXT"
[ -n "$R" ] && [ -n "$S" ] && [ "$R" -lt "$S" ] && ok "retry (line $R) before spec ahead (line $S)" \
  || bad "retry before spec ahead" "$NEXT"
has "next says the retry is an implementer" "$NEXT" "pearde brief finished --worker <worker> → dispatch as pearde-implementer"
SCAN="$( cd "$D" && python3 "$PY/plan.py" scan --board "$D/.pearde" 2>&1 )"
has "scan lists it red" "$(printf '%s\n' "$SCAN" | sed -n '/^red — /,/^$/p')" "finished"

echo "3. retry, claim, brief put a worker back on the lane"
OUT="$( cd "$D" && python3 "$PY/transitions.py" retry finished --board "$D/.pearde" 2>&1 )"
eq  "retry lands specced" "$(fm state)" specced
eq  "the failure is history" "$(grep -c '^## History' "$PRD")" 1
OUT="$( cd "$D" && python3 "$PY/transitions.py" claim finished w1 --board "$D/.pearde" 2>&1 )"
eq  "claim lands claimed" "$(fm state)" claimed
eq  "the lane still holds the worker's commit" "$( cd "$D" && git rev-list --count main..lane/finished )" 1
BRIEF="$( cd "$D" && python3 "$PY/brief.py" finished --worker w1 --board "$D/.pearde" 2>&1 )"
has "the brief carries the failure verbatim" "$BRIEF" "does not land on \`main\`"
has "the brief names the file" "$BRIEF" "- \`src/util.py\`"
has "the brief says what to do" "$BRIEF" "rebase main"
has "the brief names the lane" "$BRIEF" "lane lane/finished"

echo
[ "$FAIL" = 0 ] && echo "looptest: green" || echo "looptest: red"
exit "$FAIL"

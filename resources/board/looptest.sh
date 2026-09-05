#!/usr/bin/env bash
# looptest — the loop's flow, measured in real git. Six sections, one
# fixture each: a copy of resources/board/example under its own `git init`,
# the lane on `finished` cut by `lanes.create` exactly as `claim` cuts one,
# the worker's edit standing in it. No faked git state.
#
#   1–3  red is a queue, not a wall — a lane whose rebase conflicts lands
#        `failed` with the files under `## Failure`; `next` prints the retry
#        above `spec ahead`; `retry` → `claim` → `brief` puts a worker back
#        on the same lane with the failure verbatim
#   4    a lane holding work outside the footprint does not merge: `failed`,
#        the paths named, the checkout never moved
#   5    waiting on you is questions: a `blocked` PRD waits on its `needs:`
#        under gated, and `next` says `unblock` once they are done
#   6    one lane per file per round: a ready PRD sharing a file with a
#        claimed one is gated `after <prd> (footprint)` until it lands
#
# Run: bash resources/board/looptest.sh — exit 0 is green.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PY="$DIR"
export PEARDE_PORT=1 PEARDE_AS=engineer
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@x \
       GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@x
FAIL=0
ok()  { echo "  ok   $1"; }
bad() { FAIL=1; echo "  FAIL $1"; [ -n "${2:-}" ] && printf '       got: %s\n' "$2"; return 0; }
eq()  { [ "$2" = "$3" ] && ok "$1" || bad "$1 (want: $3)" "$2"; }
has() { printf '%s' "$2" | grep -qF -- "$3" && ok "$1" || bad "$1 (want: $3)" "$2"; }
lacks() { printf '%s' "$2" | grep -qF -- "$3" && bad "$1 (without: $3)" "$2" || ok "$1"; }

TOP="$(mktemp -d)"
cleanup() {
  for d in "$TOP"/*/; do [ -d "$d/.git" ] && git -C "$d" worktree prune >/dev/null 2>&1; done
  rm -r "$TOP"
}
trap cleanup EXIT

# fixture <name> <conflict:yes|no> — sets D, B (the board) and PRD (finished)
fixture() {
  D="$TOP/$1"; B="$D/.pearde"; PRD="$B/prds/finished/prd.md"
  mkdir -p "$B/.state" "$D/src"
  cp -R "$DIR/example/." "$B/"
  python3 - "$B/prds/finished/specs/spec01.md" <<'PY'
import re, sys
p = sys.argv[1]; t = open(p).read()          # a green verify that CAN fail: only the lane goes red
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
  if [ "$2" = yes ]; then
    printf 'main moved on\n' > "$D/src/util.py"
    ( cd "$D" && git add -- src/util.py && git commit -q -m "main moves src/util.py" )
  fi
}
fm()      { grep -m1 "^$2:" "$B/prds/$1/prd.md" | sed "s/^$2: *//"; }
collect() { ( cd "$D" && python3 "$PY/collect.py" --board "$B" "$@" 2>&1 ); }
scan()    { ( cd "$D" && python3 "$PY/plan.py" scan --board "$B" 2>&1 ); }
nxt()     { ( cd "$D" && python3 "$PY/plan.py" next "$B" 2>&1 ); }
trans()   { ( cd "$D" && python3 "$PY/transitions.py" "$@" --board "$B" 2>&1 ); }
band()    { printf '%s\n' "$2" | sed -n "/^$1/,/^\$/p"; }   # one scan section

echo "1. a conflicting lane lands failed"
fixture a yes
BEFORE="$(git -C "$D" rev-parse HEAD)"
OUT="$(collect finished)"; RC=$?
eq  "collect exits 1" "$RC" 1
eq  "state is failed" "$(fm finished state)" failed
FAILURE="$(sed -n '/^## Failure/,/^## /p' "$PRD")"
has "## Failure names the file" "$FAILURE" "src/util.py"
has "## Failure names the lane" "$FAILURE" "lane/finished"
has "## Failure names the branch it would not land on" "$FAILURE" "on \`main\`"
eq  "no claim left" "$(fm finished claim)" ""
eq  "no ## Blocked written" "$(grep -c '^## Blocked' "$PRD")" 0
eq  "the checkout never moved" "$(git -C "$D" rev-parse HEAD)" "$BEFORE"

echo "2. next puts retry before new work"
NEXT="$(nxt)"
R=$(printf '%s\n' "$NEXT" | grep -n 'retry — ' | head -1 | cut -d: -f1)
S=$(printf '%s\n' "$NEXT" | grep -n 'spec ahead\|implement — ' | head -1 | cut -d: -f1)
[ -n "$R" ] && ok "next prints a retry step" || bad "next prints a retry step" "$NEXT"
[ -n "$S" ] && ok "next prints spec ahead" || bad "next prints spec ahead" "$NEXT"
[ -n "$R" ] && [ -n "$S" ] && [ "$R" -lt "$S" ] && ok "retry (line $R) before spec ahead (line $S)" \
  || bad "retry before spec ahead" "$NEXT"
has "next says the retry is an implementer" "$NEXT" "pearde brief finished --worker <worker> → dispatch as pearde-implementer"
SCAN="$(scan)"
has "scan lists it red" "$(band 'red — ' "$SCAN")" "finished"
lacks "…and not as waiting on you" "$(band 'waiting on you' "$SCAN")" "finished"

echo "3. retry, claim, brief put a worker back on the lane"
trans retry finished >/dev/null
eq  "retry lands specced" "$(fm finished state)" specced
eq  "the failure is history" "$(grep -c '^## History' "$PRD")" 1
trans claim finished w1 >/dev/null
eq  "claim lands claimed" "$(fm finished state)" claimed
eq  "the lane still holds the worker's commit" "$(git -C "$D" rev-list --count main..lane/finished)" 1
BRIEF="$( cd "$D" && python3 "$PY/brief.py" finished --worker w1 --board "$B" 2>&1 )"
has "the brief carries the failure verbatim" "$BRIEF" "does not land on \`main\`"
has "the brief names the file" "$BRIEF" "- \`src/util.py\`"
has "the brief says what to do" "$BRIEF" "rebase main"
has "the brief names the lane" "$BRIEF" "lane lane/finished"

echo "4. a lane holding work outside the footprint does not merge"
fixture b no
mkdir -p "$B/.lanes/finished/src/extra"
printf 'x\n' > "$B/.lanes/finished/src/extra/new.py"
BEFORE="$(git -C "$D" rev-parse HEAD)"
OUT="$(collect finished)"; RC=$?
eq  "collect exits 1" "$RC" 1
eq  "state is failed" "$(fm finished state)" failed
FAILURE="$(sed -n '/^## Failure/,/^## /p' "$PRD")"
has "## Failure names the unclaimed path" "$FAILURE" "src/extra/"
has "## Failure says what to do" "$FAILURE" "Widen the footprint in the spec or drop the files"
eq  "the checkout never moved" "$(git -C "$D" rev-parse HEAD)" "$BEFORE"
eq  "the lane's work still stands" "$(git -C "$B/.lanes/finished" status --porcelain | wc -l | tr -d ' ')" 2
rm -r "$B/.lanes/finished/src/extra"
trans retry finished >/dev/null; trans claim finished w1 >/dev/null
OUT="$(collect finished)"; RC=$?
eq  "with the files dropped the same lane collects" "$RC" 0
eq  "…done" "$(fm finished state)" done

echo "5. waiting on you is questions"
fixture c no
sed -i '' -e 's/^state: open$/state: blocked/' -e 's|^  - building$|  - big/first|' "$B/prds/next/prd.md"
SCAN="$(scan)"
has "the scan's waiting on you is the question" "$(band 'waiting on you' "$SCAN")" "asking"
lacks "…and not the blocked PRD" "$(band 'waiting on you' "$SCAN")" "next"
has "the blocked PRD is gated" "$(band 'gated — ' "$SCAN")" "blocked   · next"
has "…with its need done, unblock is the line" "$(band 'gated — ' "$SCAN")" "pearde unblock next"
has "next prints the unblock" "$(nxt)" "  pearde unblock next"

echo "6. one lane per file per round"
fixture d no
printf 'footprint:\n  - src/util.py\n' > "$TOP/foot"
sed -i '' -e "/^blast-radius: low\$/r $TOP/foot" "$B/prds/big/second/prd.md"
SCAN="$(scan)"
has "a ready PRD sharing a file with a claimed one is gated" "$(band 'gated — ' "$SCAN")" "big/second"
has "…after the lane that holds the file" "$(band 'gated — ' "$SCAN")" "after finished (footprint)"
lacks "…and next does not offer it" "$(nxt)" "pearde claim big/second"
collect finished >/dev/null
eq  "the lane landed" "$(fm finished state)" done
has "…and the PRD is ready" "$(band 'ready — ' "$(scan)")" "big/second"

echo
[ "$FAIL" = 0 ] && echo "looptest: green" || echo "looptest: red"
exit "$FAIL"

#!/usr/bin/env bash
# the-guard-and-the-planner-name-the-same-board — run from the repo root:
#
#     bash resources/invariants/the-guard-and-the-planner-name-the-same-board.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: every copy of `BOARD_DIR` / `LEGACY_BOARD_DIR` under
# `resources/` spells the same pair, in the same order, and `board_named`
# prefers the live name over the legacy one.
#
# The duplication is deliberate and must stay — @resources/guard.py says why:
# the guard imports nothing from the planner, so a broken planner never blocks
# a tool call. What must not stay is a copy that disagrees. `d0a8da0` moved
# this repo to the dotted board name and flipped the planner's pair but not the
# guard's, and for a day the guard called the live board the legacy one: the
# names are found either way, because `BOARD_DIRS` holds both, so nothing was
# red — a project carrying `.pearde/` beside a stale `pearde/` simply had the
# guard count a session's blocks against a different board than `scan` did.
# Silent by construction, which is what this file is for.
#
# The copies are discovered, never listed: a fourth file spelling the pair is
# held to it the day it is written, and one that moves is followed.
#
# It can fail, and the way to prove that is not to trust this comment:
#
#     D=$(mktemp -d); git archive HEAD | tar -x -C "$D"
#     sed -i '' 's/^BOARD_DIR = ".pearde"/BOARD_DIR = "pearde"/' "$D/resources/guard.py"
#     RESOURCES="$D/resources" bash resources/invariants/<this>.sh
#
# — two rows red: the pair no longer agrees, and `board_named` answers with
# the legacy directory when a project holds both.
set -u
RESOURCES=${RESOURCES:-$(cd "$(dirname "$0")/.." && pwd -P)}
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }
say() { if [ "$1" = 0 ]; then okr "$2"; else no "$2"; fi; }

# ── 1. every copy spells the same pair, in the same order ────────────────────
FILES=$(grep -rl '^BOARD_DIR = ' "$RESOURCES" 2>/dev/null | sort)
N=$(printf '%s\n' "$FILES" | grep -c . || true)
[ "$N" -ge 2 ]
say $? "at least two copies of the pair to compare (found $N)"

pair() { sed -n -e 's/^BOARD_DIR = //p' -e 's/^LEGACY_BOARD_DIR = //p' \
                -e 's/^BOARD_DIRS = //p' "$1" | tr '\n' ' '; }

REF=""; REFF=""
for f in $FILES; do
  p=$(pair "$f")
  if [ -z "$REF" ]; then REF=$p; REFF=$f; continue; fi
  [ "$p" = "$REF" ]
  say $? "${f#"$RESOURCES"/} spells the pair the way ${REFF#"$RESOURCES"/} does (got: ${p:-nothing})"
done

# The pair is a pair, not one name twice, and `BOARD_DIRS` is built from it.
case "$REF" in
  *'(BOARD_DIR, LEGACY_BOARD_DIR)'*) r=0;; *) r=1;;
esac
say $r "BOARD_DIRS is (BOARD_DIR, LEGACY_BOARD_DIR) — the live name first"

LIVE=$(sed -n 's/^BOARD_DIR = "\(.*\)"/\1/p' "$REFF" | head -1)
LEG=$(sed -n 's/^LEGACY_BOARD_DIR = "\(.*\)"/\1/p' "$REFF" | head -1)
{ [ -n "$LIVE" ] && [ -n "$LEG" ] && [ "$LIVE" != "$LEG" ]; }
say $? "the live and legacy names differ: '$LIVE' and '$LEG'"

# ── 2. the guard answers with the live name when a project holds both ────────
# The constants agreeing is not the behaviour; this is. A project mid-migration
# carries a board under both names, and the guard must name the one `scan`
# names — otherwise every rule it keys off the board (the budget block, the
# pass file, the write into another board's tree) is kept against the wrong one.
T=$(mktemp -d) || exit 1
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/both/$LIVE/prds" "$T/both/$LEG/prds"
GOT=$(python3 - "$RESOURCES/guard.py" "$T/both" <<'PY' 2>&1
import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("guard_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(os.path.basename(m.board_of(sys.argv[2]) or ""))
PY
)
[ "$GOT" = "$LIVE" ]
say $? "the guard names '$LIVE' in a project holding both (got: ${GOT:-nothing})"

[ "$FAIL" = 0 ] || printf '\n%s check(s) failed — the invariant is broken.\n' "$FAIL"
[ "$FAIL" = 0 ]

#!/usr/bin/env bash
# The flip for the re-aimed scan-parses harness, on the same HEAD: green on
# the code as it stands, RED on each input it must catch. Every tree here is
# built from `git archive HEAD`, so nothing in the live working tree — and no
# neighbouring session's uncommitted file — can move the answer.
#
#   good    the cache as it stands
#   never   the store never serves a hit: every warm walk re-reads the board
#   stale   the store ignores mtime: a changed file is served from the cache
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
H=".pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT

for d in good never stale; do
  mkdir -p "$T/$d"
  ( cd "$ROOT" && git archive HEAD | tar -x -C "$T/$d" )
  mkdir -p "$T/$d/$(dirname "$H")"
  cp "$ROOT/$H" "$T/$d/$H"
done

PLAN=resources/board/plan.py
# never — the lookup always misses. The cache file is still written, so the
# earlier checks in the harness stay green and only the work count moves.
python3 - "$T/never/$PLAN" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
n = s.replace("    e = _PCACHE.get(apath)", "    e = None", 1)
assert n != s, "never: patch site not found"
open(p, "w").write(n)
PY
# stale — the mtime half of the freshness test is dropped.
python3 - "$T/stale/$PLAN" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
n = s.replace('e.get("mtime") == st.st_mtime_ns', "True", 1)
assert n != s, "stale: patch site not found"
open(p, "w").write(n)
PY

RC=0
for d in good never stale; do
  out="$(bash "$T/$d/$H" 2>&1)"; rc=$?
  echo "--- $d: exit $rc"
  printf '%s\n' "$out" | grep -E "^(ok|FAIL|parse-cache)" | sed 's/^/    /'
  case "$d:$rc" in
    good:0|never:1|stale:1) ;;
    *) echo "    UNEXPECTED"; RC=1 ;;
  esac
done
exit $RC

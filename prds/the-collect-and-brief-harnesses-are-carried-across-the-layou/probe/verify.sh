#!/bin/bash
# the-collect-and-brief-harnesses-are-carried-across-the-layou — the probe.
# Asserts the three collect/brief harnesses named in the parent report measure
# the pearde layout: they run from the code repo root and by absolute path
# from /, each prints its own full denominator with zero failures, and no file
# passes a pre-move board (a `<dir>/prds` board) to the tools. Fixtures live
# where the harnesses build them — temp dirs, removed at exit; nothing is
# written under prds/ here.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
while [ ! -f "$ROOT/resources/guard.py" ]; do ROOT="$(dirname "$ROOT")"; done
KEEPS="$ROOT/.pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh"
ISACMD="$ROOT/.pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh"
BRIEFS="$ROOT/.pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ok   $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; }

# the count a suite printed

suite() { # suite <label> <file> <want-pass> <want-total>
  local out tot pass line
  out=$(bash "$2" </dev/null 2>&1) || true
  line=$(printf '%s' "$out" | tail -1)
  tot=$(printf '%s' "$out" | grep -m1 -oE '[0-9]+ checks' | grep -oE '[0-9]+')
  pass=$(printf '%s' "$out" | grep -m1 -oE '[0-9]+ pass|verify: [0-9]+' | grep -oE '[0-9]+' | head -1)
  if [ "${tot:-0}" = "$4" ] && [ "${pass:-0}" = "$3" ]; then
    ok "$1 — $line"
  else
    bad "$1 — got: $line, want $3/$4"
  fi
}

echo "── the three suites, from the code repo root"
suite "collect-keeps-its-word" "$KEEPS" 101 101
suite "collect-is-a-command"   "$ISACMD" 133 133
suite "brief-is-printed"       "$BRIEFS" 104 104

echo "── the same three by absolute path from /"
cd /
suite "collect-keeps-its-word from /" "$KEEPS" 101 101
suite "collect-is-a-command from /"   "$ISACMD" 133 133
suite "brief-is-printed from /"       "$BRIEFS" 104 104

echo "── the census"
# the one standing exception is collect-keeps-its-word's run_old line, which
# passes "$D/.pearde/prds" to a pinned pre-move collect.py — it matches the
# pattern but reads the pearde board; count only bare `<dir>/prds` boards:
BAD=$(grep -E -- '--board "[^"]*"' "$KEEPS" "$ISACMD" "$BRIEFS" \
      | grep -v '\.pearde/prds' | grep -c -- '--board' || true)
if [ "${BAD:-0}" = "0" ]; then ok "no suite hands a pre-move board to a tool"; else
  bad "a suite passes a pre-move board ($BAD lines)"; fi

echo "verify: $((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]; RC=$?
echo "probe: $((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
exit $RC
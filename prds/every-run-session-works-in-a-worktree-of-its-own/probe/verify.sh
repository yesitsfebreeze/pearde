#!/usr/bin/env bash
# The PRD's Verify, in a clean room. Two sessions with uncommitted edits to
# the same file; then one is killed and a third reaps it.
#
#   bash verify.sh            measures the tree the runner names
#   PEARDE_ROOT=<tree> bash …  measures that tree instead
#   SESSIONS=<path> bash …    points it at one module copy
#
# PEARDE_ROOT names the tree to measure; it defaults to the repo above the
# board this file sits in. BOARD is found by walking up to the board dir
# rather than counting `..`, so the nesting depth of this PRD does not matter.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
LANE="${LANE:-$ROOT}"
SESSIONS="${SESSIONS:-$LANE/resources/board/sessions.py}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
fail=0
ok()   { echo "  ok   $1"; }
bad()  { echo "  FAIL $1"; fail=$((fail+1)); }

# a repo with a machine-local board dir under it, the pearde layout
R="$T/repo"; mkdir -p "$R/board/.state"; cd "$R"
git init -q .; git config user.email t@t; git config user.name t
echo "printf hello" > shared.py; echo "board/" > .gitignore
git add -A; git commit -qm base

# two fake sessions: a live one (a real sleeping pid + its socket) and one
# that will be killed. `alive()` wants the pid AND the socket, so the socket
# is a plain file here — `os.path.exists` is all it reads.
mkdir -p "$T/socks"
sleep 300 & LIVE=$!
sleep 300 & DEAD=$!
touch "$T/socks/$LIVE.sock" "$T/socks/$DEAD.sock"

take() { # $1 = id, $2 = pid
  CLAUDE_CODE_SESSION_ID="$1" CLAUDE_PID="$2" \
  CLAUDE_CODE_MESSAGING_SOCKET="$T/socks/$2.sock" \
  python3 -c "
import sys; sys.path.insert(0, '$(dirname "$SESSIONS")')
import sessions
sessions.GRACE_S = 0.0
print(sessions.take('$R/board', '$R'))"
}
run() { # $1 = id, $2 = pid, rest = python
  local id=$1 pid=$2; shift 2
  CLAUDE_CODE_SESSION_ID="$id" CLAUDE_PID="$pid" \
  CLAUDE_CODE_MESSAGING_SOCKET="$T/socks/$pid.sock" \
  python3 -c "
import sys; sys.path.insert(0, '$(dirname "$SESSIONS")')
import sessions
sessions.GRACE_S = 0.0
$*"
}

echo "1 · take"
A="$(take sess-alpha "$LIVE")"; B="$(take sess-bravo "$DEAD")"
[ -d "$A" ] && [ -d "$B" ] && [ "$A" != "$B" ] && ok "two sessions, two trees" \
  || bad "two sessions did not get two trees ($A / $B)"
[ -f "$R/board/.state/sessions.json" ] && ok "the ledger names both" \
  || bad "no ledger written"
grep -q sess-alpha "$R/board/.state/sessions.json" && grep -q sess-bravo "$R/board/.state/sessions.json" \
  || bad "the ledger is missing a row"
# the board is excluded from every session tree — a board command run from
# inside one must resolve the real board, never a phantom copy
[ ! -e "$A/board" ] && ok "the board is not copied into a session tree" \
  || bad "a session tree carries a copy of the board"

echo "2 · each holds uncommitted work on the same file"
echo "alpha's edit" >> "$A/shared.py"; echo "alpha only" > "$A/new-alpha.py"
echo "bravo's edit" >> "$B/shared.py"; echo "bravo only" > "$B/new-bravo.py"
ASUM="$(shasum "$A/shared.py" | cut -d' ' -f1)"
BSUM="$(shasum "$B/shared.py" | cut -d' ' -f1)"
[ "$ASUM" != "$BSUM" ] && ok "the two trees hold different content" || bad "the trees are the same file"

echo "3 · owns — the refuse rule's predicate"
run sess-alpha "$LIVE" "
assert sessions.owns('$R/board', '$A'), 'alpha does not own its own tree'
assert not sessions.owns('$R/board', '$B'), 'alpha owns bravo\'s tree'
assert not sessions.owns('$R/board', '$R'), 'alpha owns the main checkout'
print('  ok   a session owns its own tree and neither of the other two')
" || bad "owns() let a session through to a tree that is not its own"

echo "4 · a reap with both alive touches nothing"
run sess-alpha "$LIVE" "
print('\n'.join(sessions.reap('$R/board', '$R', apply=True)))"
[ -d "$B" ] && ok "a live session's tree is untouched" || bad "a live session's tree was reaped"

echo "5 · kill bravo, then alpha reaps"
kill "$DEAD" 2>/dev/null; rm -f "$T/socks/$DEAD.sock"; wait "$DEAD" 2>/dev/null
run sess-alpha "$LIVE" "
print('\n'.join(sessions.reap('$R/board', '$R', apply=True)))"
[ ! -d "$B" ] && ok "the dead session's tree is gone" || bad "the dead session's tree survived the reap"
[ -d "$A" ] && ok "the live session's tree is untouched" || bad "the live session's tree was reaped"
NOW="$(shasum "$A/shared.py" | cut -d' ' -f1)"
[ "$NOW" = "$ASUM" ] && ok "the live tree is byte-identical" || bad "the live tree changed under the reap"
grep -q sess-bravo "$R/board/.state/sessions.json" && bad "the reaped row is still on the ledger" \
  || ok "the reaped row is off the ledger"

echo "6 · the reaped session's uncommitted work is in the object store"
git -C "$R" stash list | grep -q . && ok "a stash ref stands" || bad "nothing was stashed"
if git -C "$R" show "stash@{0}:shared.py" 2>/dev/null | grep -q "bravo's edit"; then
  ok "the tracked edit is recoverable"
else
  bad "the tracked edit is NOT recoverable"
fi
if git -C "$R" show "stash@{0}^3:new-bravo.py" 2>/dev/null | grep -q "bravo only"; then
  ok "the untracked file is recoverable"
else
  bad "the untracked file is NOT recoverable — git stash create drops untracked files"
fi

kill "$LIVE" 2>/dev/null; wait "$LIVE" 2>/dev/null
echo
[ "$fail" -eq 0 ] && echo "verify: green" || echo "verify: $fail FAIL"
exit "$fail"

#!/usr/bin/env bash
# a-session-start-brings-the-board-up — the SessionStart hook that brings the
# board's view up. Every check runs against a throwaway repo made here, on a
# port of its own: this repo's own .claude/settings.json and the machine's
# real daemon on 8443 are never touched.
#
#   bash .pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh
#
# A `live` section needs the `claude` CLI and costs one model call; it is
# skipped without it. Everything else is offline.
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
G="python3 $ROOT/resources/guard.py"
SERVE="$ROOT/resources/board/serve.py"
PORT=8457
N=0; P=0; F=0; S=0
ok()   { N=$((N+1)); P=$((P+1)); printf '  ok   %s\n' "$1"; }
bad()  { N=$((N+1)); F=$((F+1)); printf '  FAIL %s\n' "$1"; }
skip() { S=$((S+1)); printf '  skip %s\n' "$1"; }
has()  { printf '%s' "$2" | grep -qF -- "$3" && ok "$1" || bad "$1 — missing '$3'"; }
no()   { printf '%s' "$2" | grep -qF -- "$3" && bad "$1 — has '$3'" || ok "$1"; }
eq()   { [ "$2" = "$3" ] && ok "$1" || bad "$1 — got '$2', want '$3'"; }
jq_()  { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(eval(sys.argv[2]))' "$1" "$2" 2>&1; }

W="$(mktemp -d)"
board() {  # board <dir> — a repo with a board in it
  mkdir -p "$1/.pearde/prds/hello"
  printf -- '---\nname: %s\nlanguage: English\n---\n# board\n' "$(basename "$1")" > "$1/.pearde/settings.md"
  printf -- '---\nstate: open\norigin: requested\npriority: 10\ncomplexity: 0\nblast-radius:\n---\n# hello\n' \
    > "$1/.pearde/prds/hello/prd.md"
}
cleanup() { PEARDE_PORT=$PORT python3 "$SERVE" stop >/dev/null 2>&1; rm -rf "$W"; }
trap cleanup EXIT

echo "── A. guard on writes the SessionStart entry"
R="$W/a"; board "$R"
OUT="$($G on "$R" 2>&1)"; SA="$R/.claude/settings.json"
has "A on names SessionStart" "$OUT" "SessionStart"
has "A on names serve.py ensure" "$OUT" "serve.py ensure"
eq  "A five + lines — the env cap and four hooks" "$(printf '%s\n' "$OUT" | grep -c '^  + ')" 5
eq  "A four of them are hooks" "$(printf '%s\n' "$OUT" | grep -c '^  + [A-Za-z]*Tool\|^  + SessionStart')" 4
eq  "A one SessionStart entry" "$(jq_ "$SA" 'len(d["hooks"]["SessionStart"])')" 1
eq  "A the entry carries no matcher" "$(jq_ "$SA" '"matcher" in d["hooks"]["SessionStart"][0]')" False
CMD="$(jq_ "$SA" 'd["hooks"]["SessionStart"][0]["hooks"][0]["command"]')"
eq  "A the command" "$CMD" "python3 $(python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$SERVE") ensure >/dev/null 2>&1 || true"
eq  "A hook type command" "$(jq_ "$SA" 'd["hooks"]["SessionStart"][0]["hooks"][0]["type"]')" command
eq  "A the three guard hooks are still there" \
    "$(jq_ "$SA" '" ".join(e["matcher"] for e in d["hooks"]["PreToolUse"]) + " " + " ".join(e["matcher"] for e in d["hooks"]["PostToolUse"])')" \
    "Bash|Read Edit|Write Edit|Write"
eq  "A indent 2, trailing newline" \
    "$(python3 -c 'import json,sys; t=open(sys.argv[1]).read(); print(t==json.dumps(json.loads(t),indent=2,ensure_ascii=False)+"\n")' "$SA")" True

echo "── B. on is idempotent, off takes exactly it out"
OUT="$($G on "$R" 2>&1)"
has "B a second on changes nothing" "$OUT" "already wired, nothing changed"
OUT="$($G off "$R" 2>&1)"
eq  "B four - lines" "$(printf '%s\n' "$OUT" | grep -c '^  - ')" 4
has "B off names SessionStart" "$OUT" "SessionStart"
eq  "B off empties hooks" "$(jq_ "$SA" 'd["hooks"]')" "{}"
eq  "B off leaves the env key" "$(jq_ "$SA" 'd["env"]["MAX_THINKING_TOKENS"]')" 8000

echo "── C. a foreign SessionStart entry is kept"
R2="$W/c"; board "$R2"; mkdir -p "$R2/.claude"
cat > "$R2/.claude/settings.json" <<'EOF'
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup", "hooks": [{ "type": "command", "command": "echo mine" }] }
    ]
  }
}
EOF
$G on "$R2" >/dev/null 2>&1
S2="$R2/.claude/settings.json"
eq  "C the foreign entry stays first" "$(jq_ "$S2" 'd["hooks"]["SessionStart"][0]["hooks"][0]["command"]')" "echo mine"
eq  "C ours is appended" "$(jq_ "$S2" 'len(d["hooks"]["SessionStart"])')" 2
$G off "$R2" >/dev/null 2>&1
eq  "C off leaves the foreign entry" "$(jq_ "$S2" 'd["hooks"]["SessionStart"][0]["hooks"][0]["command"]')" "echo mine"
eq  "C off leaves it alone" "$(jq_ "$S2" 'len(d["hooks"]["SessionStart"])')" 1

echo "── D. guard status notes a missing SessionStart hook"
R3="$W/d"; board "$R3"; $G on "$R3" >/dev/null 2>&1
OUT="$($G status "$R3" 2>&1)"
no  "D wired: no note" "$OUT" "no SessionStart hook"
python3 - "$R3/.claude/settings.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); del d["hooks"]["SessionStart"]
open(p, "w").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
PY
OUT="$($G status "$R3" 2>&1)"
has "D unwired: guard row still ok" "$OUT" "skill tree guarded"
has "D unwired: the note" "$OUT" "no SessionStart hook"
has "D unwired: the note says the fix" "$OUT" "pearde guard on writes it"
eq  "D unwired: still exit 0" "$($G status "$R3" >/dev/null 2>&1; echo $?)" 0

echo "── E. doctor carries the same note"
DOUT="$(PEARDE_PORT=$PORT bash "$ROOT/resources/doctor.sh" "$R3" 2>&1)"
has "E doctor notes the missing hook" "$DOUT" "no SessionStart hook"
$G on "$R3" >/dev/null 2>&1
DOUT="$(PEARDE_PORT=$PORT bash "$ROOT/resources/doctor.sh" "$R3" 2>&1)"
no  "E wired: doctor is quiet about it" "$DOUT" "no SessionStart hook"

echo "── F. the command itself: quiet, cheap, exit 0 anywhere"
R4="$W/f"; board "$R4"; $G on "$R4" >/dev/null 2>&1
HOOK="$(jq_ "$R4/.claude/settings.json" 'd["hooks"]["SessionStart"][0]["hooks"][0]["command"]')"
PEARDE_PORT=$PORT python3 "$SERVE" stop >/dev/null 2>&1
OUT="$(cd "$R4" && PEARDE_PORT=$PORT sh -c "$HOOK" 2>&1)"; RC=$?
eq  "F cold: exit 0" "$RC" 0
eq  "F cold: silent" "$OUT" ""
eq  "F cold: the board is registered" \
    "$(PEARDE_PORT=$PORT python3 "$SERVE" status 2>/dev/null | grep -c "$(cd "$R4" && pwd -P)/.pearde")" 1
T0=$(python3 -c 'import time;print(time.time())')
OUT="$(cd "$R4" && PEARDE_PORT=$PORT sh -c "$HOOK" 2>&1)"; RC=$?
T1=$(python3 -c 'import time,sys;print(time.time()-float(sys.argv[1]))' "$T0")
eq  "F warm: exit 0" "$RC" 0
eq  "F warm: silent" "$OUT" ""
eq  "F warm: under a second ($T1 s)" "$(python3 -c 'import sys;print(float(sys.argv[1])<1.0)' "$T1")" True
NB="$W/noboard"; mkdir -p "$NB"
OUT="$(cd "$NB" && PEARDE_PORT=$PORT sh -c "$HOOK" 2>&1)"; RC=$?
eq  "F outside a board: exit 0" "$RC" 0
eq  "F outside a board: silent" "$OUT" ""
OUT="$(cd "$R4" && PEARDE_PORT=1 sh -c "$HOOK" 2>&1)"; RC=$?
eq  "F unusable port: exit 0" "$RC" 0
eq  "F unusable port: silent" "$OUT" ""
PEARDE_PORT=$PORT python3 "$SERVE" stop >/dev/null 2>&1

echo "── G. doctor's view row flips on one session start"
R5="$W/g"; board "$R5"; $G on "$R5" >/dev/null 2>&1
HOOK="$(jq_ "$R5/.claude/settings.json" 'd["hooks"]["SessionStart"][0]["hooks"][0]["command"]')"
DOUT="$(PEARDE_PORT=$PORT bash "$ROOT/resources/doctor.sh" "$R5" 2>&1 | grep '^  view')"
has "G before: view is off" "$DOUT" "off"
(cd "$R5" && PEARDE_PORT=$PORT sh -c "$HOOK")
DOUT="$(PEARDE_PORT=$PORT bash "$ROOT/resources/doctor.sh" "$R5" 2>&1 | grep '^  view')"
has "G after one hook run: view is ok" "$DOUT" "ok"
no  "G and no --fix was needed" "$DOUT" "fix:"
PEARDE_PORT=$PORT python3 "$SERVE" stop >/dev/null 2>&1

echo "── H. the docs say it"
has "H guard.md holds the SessionStart block" "$(cat "$ROOT/references/parts/guard.md")" '"SessionStart": [{'
has "H guard.md says why || true" "$(cat "$ROOT/references/parts/guard.md")" 'reserves exit 2'
has "H install.md names the hook" "$(cat "$ROOT/references/install.md")" 'as a `SessionStart` hook'
has "H install.md no longer only aspires" "$(cat "$ROOT/references/install.md")" 'the `SessionStart` hook `pearde guard on` writes'

echo "── I. live: a real session start brings the board up"
# Under a board-wide sweep this section is stood down rather than asserted.
# `doctor.sh --harnesses` sets PEARDE_HARNESSES and now ends the sweep with
# `serve.py reap`, which stops any daemon "watching no board" — exactly what a
# daemon looks like in the window between `ensure` binding its port and the
# board's first `/register`. A live session start inside that sweep is decided
# by the sweep's scheduling, not by this PRD's wiring, so it is skipped there
# and measured on its own. It also costs a model call, which a 53-harness
# parallel sweep should not pay 53 times.
if [ -n "${PEARDE_HARNESSES:-}" ]; then
  skip "I under a harness sweep — a live session start races the sweep's serve.py reap"
elif ! command -v claude >/dev/null 2>&1; then
  skip "I no claude CLI on PATH"
else
  R6="$W/i"; board "$R6"; $G on "$R6" >/dev/null 2>&1
  python3 - "$R6/.claude/settings.json" "$PORT" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d["env"]["PEARDE_PORT"] = sys.argv[2]
open(p, "w").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
PY
  PEARDE_PORT=$PORT python3 "$SERVE" stop >/dev/null 2>&1
  OUT="$(cd "$R6" && claude -p "reply with exactly: OK" --permission-mode plan --model haiku </dev/null 2>&1)"
  has "I the session answered" "$OUT" "OK"
  no  "I the session start printed nothing extra" "$OUT" "serve:"
  # the daemon the hook started answers /status within a moment of binding;
  # one immediate read races it, so poll for five seconds. Measured: the hit
  # lands on the first poll every time the daemon survives at all — the longer
  # window buys nothing against a reap, only against a loaded machine.
  WANT="$(cd "$R6" && pwd -P)/.pearde"; HIT=0
  for _ in $(seq 1 25); do
    PEARDE_PORT=$PORT python3 "$SERVE" status 2>/dev/null | grep -qF "$WANT" \
      && { HIT=1; break; }
    sleep 0.2
  done
  eq  "I the board is registered" "$HIT" 1
  PEARDE_PORT=$PORT python3 "$SERVE" stop >/dev/null 2>&1
fi

echo
echo "$N checks · $P pass · $F fail · $S skip"
[ "$F" = 0 ]

#!/usr/bin/env bash
# the-round-runs-in-a-window-that-ends — the budget is measured from the
# window's own floor, the stamps are per window, and the ceiling leaves a way
# on. Every call is hook JSON on stdin; PEARDE_GUARD_STATE points at a temp
# dir, so nothing under resources/board/state/ is touched.
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd -P)"
GUARD="$ROOT/resources/guard.py"
D="$(mktemp -d)"; S="$(mktemp -d)"
trap 'rm -rf "$D" "$S"' EXIT
export PEARDE_GUARD_STATE="$S/state"
pass=0; fail=0
ok()   { if [ "$2" -eq 0 ]; then pass=$((pass+1)); echo "  ok   $1"; else fail=$((fail+1)); echo "  FAIL $1${3:+ — $3}"; fi; }
is()   { if [ "$2" = "$3" ]; then ok "$1" 0; else ok "$1" 1 "got [$2] want [$3]"; fi; }
has()  { case "$2" in *"$3"*) ok "$1" 0 ;; *) ok "$1" 1 "missing: $3" ;; esac; }

# a board, and a file outside it to write
mkdir -p "$D/proj/.pearde/prds/x" "$D/proj/.pearde/.state"
printf -- '---\nlanguage: English\ncontext-budget: 100k\n---\n' > "$D/proj/.pearde/settings.md"
echo hi > "$D/proj/notes.md"; echo spec > "$D/proj/spec.md"
TR="$D/t.jsonl"; MAIN="win$$"
win() { printf '{"type":"assistant","message":{"usage":{"input_tokens":%s}}}\n' "$1" > "$TR"; }

hook() { # tool file [agent] [session] → the guard's decision
  local tool="$1" file="$2" agent="${3:-}" sess="${4:-$MAIN}" inp extra=""
  case "$tool" in
    Read)             inp='{"file_path":"'"$file"'"}' ;;
    Agent|Task)       inp='{"prompt":"work the board"}' ;;
    AskUserQuestion)  inp='{}' ;;
    *)                inp='{"file_path":"'"$file"'","content":"x"}' ;;
  esac
  [ -n "$agent" ] && extra=',"agent_id":"'"$agent"'"'
  printf '{"tool_name":"%s","session_id":"%s","cwd":"%s","transcript_path":"%s","tool_input":%s%s}' \
    "$tool" "$sess" "$D/proj" "$TR" "$inp" "$extra" | python3 "$GUARD" pre 2>"$S/err" \
    | python3 -c 'import json,sys;d=sys.stdin.read().strip();print(json.loads(d)["hookSpecificOutput"].get("permissionDecision","allow") if d else "allow")'
}
reason() { # the same refusal, but printed rather than decided
  printf '{"tool_name":"Write","session_id":"%s","cwd":"%s","transcript_path":"%s","tool_input":{"file_path":"%s","content":"x"}}' \
    "$MAIN" "$D/proj" "$TR" "$D/proj/notes.md" | python3 "$GUARD" pre 2>/dev/null \
    | python3 -c 'import json,sys;d=sys.stdin.read().strip();print(json.loads(d)["hookSpecificOutput"].get("permissionDecisionReason","") if d else "")'
}

echo "— the budget is measured from the floor"
win 60000;  is "A1 the first turn sets the floor and passes" "$(hook Write "$D/proj/notes.md")" "allow"
win 150000; is "A2 90k of growth over a 60k floor passes" "$(hook Write "$D/proj/notes.md")" "allow"
win 170000; is "A3 110k of growth is refused" "$(hook Write "$D/proj/notes.md")" "deny"
win 99000
SESS2="floor$$"
is "A4 a 99k window whose floor is 99k is not over budget" "$(hook Write "$D/proj/notes.md" "" "$SESS2")" "allow"

echo "— the ceiling leaves a way on"
win 170000
is "B1 the round file stays writable" "$(hook Write "$D/proj/.pearde/.state/round.md")" "allow"
is "B2 dispatching a worker stays allowed" "$(hook Agent "")" "allow"
is "B3 asking the user stays allowed" "$(hook AskUserQuestion "")" "allow"
is "B4 a worker is never judged by the dispatcher's window" "$(hook Write "$D/proj/notes.md" agent-1)" "allow"
R="$(reason)"
has "B5 the refusal names the handover, not a stop" "$R" "Hand the rest over rather than stopping"
has "B6 ...and the worker that carries on" "$R" "pearde-round"
has "B7 ...and reports the growth over the floor" "$R" "over its floor"

echo "— a stamp belongs to one window"
win 60000
SESS3="stamp$$"
hook Read "$D/proj/spec.md" A "$SESS3" >/dev/null; hook Read "$D/proj/spec.md" A "$SESS3" >/dev/null
is "C1 a third read by the same worker is refused" "$(hook Read "$D/proj/spec.md" A "$SESS3")" "deny"
is "C2 the next worker's first read passes" "$(hook Read "$D/proj/spec.md" B "$SESS3")" "allow"
is "C3 the dispatcher's own first read passes" "$(hook Read "$D/proj/spec.md" "" "$SESS3")" "allow"

echo "— the text says the same thing the code does"
G="$ROOT/references/parts/guard.md"; L="$ROOT/references/parts/loop.md"
D_="$ROOT/references/parts/dispatch.md"; A="$ROOT/references/agents/pearde-round.md"
K="$ROOT/references/skills/pearde.md"
[ -f "$D_" ]; ok "D1 references/parts/dispatch.md exists" $?
[ -f "$A" ];  ok "D2 references/agents/pearde-round.md exists" $?
has "D3 the skill sends the session to the dispatcher" "$(cat "$K")" "Read @references/parts/dispatch.md"
has "D4 dispatch.md names the four verdicts" "$(cat "$D_")" '`MORE`'
has "D5 ...and the prompt it sends" "$(cat "$D_")" "Resume from .pearde/.state/round.md"
has "D6 the round agent names its stop conditions" "$(cat "$A")" "transitions-per-round"
has "D7 loop.md says the ceiling is a handover" "$(cat "$L")" "The ceiling is a handover, never a stop"
has "D8 guard.md says the budget is measured from the floor" "$(cat "$G")" "measured from the floor"
has "D9 settings.md documents transitions-per-round" "$(cat "$ROOT/references/settings.md")" '`transitions-per-round`'
is "D10 loop.md is still one page" "$([ "$(wc -l < "$L" | tr -d ' ')" -le 170 ] && echo yes || echo no)" "yes"
has "D11 files.md lists the round worker" "$(cat "$ROOT/references/files.md")" "@references/agents/pearde-round.md"
has "D12 files.md lists the dispatcher" "$(cat "$ROOT/references/files.md")" "@references/parts/dispatch.md"

echo
echo "$((pass+fail)) checks · $pass pass · $fail fail"
[ "$((pass+fail))" = 26 ] || { echo "denominator moved: 26 expected"; exit 1; }
[ "$fail" -eq 0 ]

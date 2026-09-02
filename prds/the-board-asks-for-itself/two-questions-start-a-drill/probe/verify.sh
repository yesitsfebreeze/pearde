#!/usr/bin/env bash
# two-questions-start-a-drill — "## Done when", as a harness, for the gate that
# runs every verify.sh on this board (`doctor.sh --harnesses`).
#
# The contract: more than one unanswered question on the board and the scan
# opens on a drill section, the header says `asking N over M PRDs`, and nothing
# is claimed until the pass is out. One question is step 2's ordinary put;
# zero prints nothing; a closed PRD's old pass counts nothing.
#
# Every fixture is built under mktemp -d — never under prds/, where a directory
# holding prd.md is a PRD — and removed at exit. Nothing here writes to the
# real board; the two board reads it does are read-only checks.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../../../.." && pwd)"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
PASS=0; FAIL=0
ok()  { PASS=$((PASS + 1)); echo "  ok   $1"; }
no()  { FAIL=$((FAIL + 1)); echo "  FAIL $1"; }
has() { if printf '%s\n' "$2" | grep -qF -- "$3"; then ok "$1"; else no "$1 — want [$3]"; fi; }

echo "# the three modules the count, the section and the gate live in"
if python3 -m py_compile "$REPO/resources/questions.py" \
     "$REPO/resources/board/plan.py" "$REPO/resources/board/transitions.py" \
     2>"$TMP/pyc.txt"; then ok "questions.py, plan.py, transitions.py compile"
else no "a module does not compile"; cat "$TMP/pyc.txt"; fi

echo "# the fixture board — every leg of ## Done when"
CODE="$REPO" bash "$HERE/spec-fixture.sh" "$TMP/fx" > "$TMP/fx.txt" 2>&1
rc=$?
FX=$(cat "$TMP/fx.txt")
if [ "$rc" = 0 ]; then ok "spec-fixture.sh exits 0"
else no "spec-fixture.sh exits $rc"; grep -E '^FAIL' "$TMP/fx.txt"; fi
has "no leg failed" "$FX" "probe done · failures: 0"
has "two questions: the header count" "$FX" "OK: header says asking 2 over 2 PRDs"
has "two questions: the drill section stands first" "$FX" "OK: drill stands above every other section"
has "the claim is refused naming asking 2" "$FX" "OK: claim refused naming asking 2"
has "the pass out, the claim goes" "$FX" "OK: claim went through once the pass was out"
has "one question: no gate" "$FX" "OK: no gate at one: the claim goes through"
has "zero questions: nothing prints" "$FX" "OK: zero prints no count"
has "a closed PRD's old pass counts zero" "$FX" "OK: done + superseded passes count zero"
has "the list and the scan are one reader" "$FX" "OK: and the scan agrees — one reader"

echo "# the manual says where the drill starts"
LOOP=$(cat "$REPO/references/parts/loop.md")
has "loop.md step 1 names the count" "$LOOP" "asking N over M"
has "loop.md step 1: the section stands first" "$LOOP" "a **drill** section stands first, above"
# the three rows are spelled out — `| 1 |` would read as a ninth step in the
# loop's own step table, which @the-board-runs-itself/the-loop-is-commands pins
has "loop.md step 2 row: no question" "$LOOP" "| none | nothing |"
has "loop.md step 2 row: one question" "$LOOP" "| one | that question, put as today |"
has "loop.md step 2 row: two or more" "$LOOP" "| two or more | one drill pass over all of them"
has "loop.md: nothing is dispatched while it is unput" "$LOOP" "dispatched: \`pearde claim\` refuses \`asking N — drill first\`"
has "loop.md step 8 is the same drill" "$LOOP" "same drill the scan count starts"
DRILL=$(cat "$REPO/references/drill.md")
has "drill.md: the scan count is the second entry point" "$DRILL" "second entry point"
has "drill.md names the refusal" "$DRILL" "asking N — drill first"
ROUND=$(cat "$REPO/references/parts/pass.md")
has "pass.md: ## Asked is what the gate reads" "$ROUND" "what the drill gate"
has "pass.md: it matches by title" "$ROUND" "by title"
GUARD=$(cat "$REPO/references/parts/guard.md")
has "guard.md names the refusal" "$GUARD" "asking N — drill first"
has "guard.md: it lands in the refused count" "$GUARD" "refused\` count"

echo "# every pass already on the real board still passes the checker"
if python3 "$REPO/resources/questions.py" check "$REPO/.pearde" > "$TMP/q.txt" 2>&1
then ok "questions.py check is silent on this board"
else no "a pass on this board fails"; cat "$TMP/q.txt"; fi

echo
echo "$((PASS + FAIL)) checks · $PASS pass · $FAIL fail"
[ "$((PASS + FAIL))" = 25 ] || { printf '  FAIL expected 25 checks, ran %s\n' "$((PASS + FAIL))"; FAIL=$((FAIL + 1)); }
[ "$FAIL" -eq 0 ]

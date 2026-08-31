#!/usr/bin/env bash
# spec-fixture.sh <target-dir> — the verify legs for spec01..spec03, run
# against the CODE repo's plan.py / questions.py / transitions.py (CODE env,
# default /Users/feb/dev/infra/pearde).
# Usage: CODE=/path/to/repo bash spec-fixture.sh <tmpdir-for-the-fixture-board>
#
# The spec verify blocks invoke this under `bash -e -o pipefail`, so the first
# line below takes -e back: a leg that does not hold has to print its FAIL and
# let the run finish, or the box it belongs to is never told apart from the
# box after it. The script counts its own failures and exits on the count.
set +e
set -u
CODE="${CODE:-/Users/feb/dev/infra/pearde}"
T="${1:?usage: spec-fixture.sh <tmp-dir>}"
D="$T/.pearde"
PLAN="python3 $CODE/resources/board/plan.py"
TRANS="python3 $CODE/resources/board/transitions.py"
QLIST="python3 $CODE/resources/questions.py list"
export PEARDE_AS=engineer

fails=0
ok()  { echo "OK: $1"; }
no()  { echo "FAIL: $1"; fails=$((fails + 1)); }
ck()  { if [ "$1" = 0 ]; then ok "$2"; else no "$2"; fi; }
has() { if printf '%s\n' "$2" | grep -q -- "$3"; then ok "$1"; else no "$1 — want [$3]"; fi; }
lacks() { if printf '%s\n' "$2" | grep -q -- "$3"; then no "$1 — has [$3]"; else ok "$1"; fi; }
# the first section heading the scan prints, in the order it prints them
first_section() { printf '%s\n' "$1" \
  | grep -E '^(drill|collect|waiting on you|in flight|ready|gated) ' | head -1; }
state_of() { grep -m1 '^state:' "$D/prds/$1/prd.md" | tr -d '\r'; }

rm -rf "$T"; mkdir -p "$D/prds"/{one,two,other,other2,old,sup} "$D/.state"

# a question PRD in drill.md's own format — the fork, three prepared answers,
# one recommended. `one` and `two` carry the same title on purpose: the round
# file matches by title, so one `## Asked` line carries both.
qprd() {
  { echo '---'; echo 'state: question'; echo 'priority: 50'; echo '---'
    echo "# f-$1"; echo; echo '## Questions'; echo
    echo '### Q1: What the board shows a session first'; echo
    echo 'A session sees either the questions it is being asked or the work'
    echo 'it could start; whichever the page opens on is what it acts on?'
    echo
    echo '1. **Questions first** — opens on what waits on you; work one click away. (recommended)'
    echo '2. **Work first** — opens on what is happening; questions one click away.'
    echo '3. **Ask each time** — remembers whichever you opened last.'
  } > "$D/prds/$1/prd.md"
}
for n in one two; do qprd "$n"; done
printf -- '---\nstate: open\npriority: 10\n---\n# f-other\n\nplain\n' > "$D/prds/other/prd.md"
printf -- '---\nstate: open\npriority: 10\n---\n# f-other2\n\nplain\n' > "$D/prds/other2/prd.md"
printf -- '---\nstate: done\npriority: 10\n---\n# f-old\n\n## Questions\n\n### Q1: What this closed on\n\nIt closed?\n\n1. **One** — so. (recommended)\n2. **Two** — so.\n3. **Three** — so.\n' > "$D/prds/old/prd.md"
printf -- '---\nstate: superseded\npriority: 10\n---\n# f-sup\n\n## Questions\n\n### Q1: What replaced this\n\nGone?\n\n1. **One** — so. (recommended)\n2. **Two** — so.\n3. **Three** — so.\n' > "$D/prds/sup/prd.md"

cd "$T" || { echo "FAIL: cannot cd $T"; exit 1; }

echo "== leg 1 (spec01 box 1): two questions standing"
OUT=$($PLAN scan 2>&1)
has "header says asking 2 over 2 PRDs" "$OUT" "asking 2 over 2 PRDs"
has "drill section printed" "$OUT" "^drill — asking 2 over 2 PRDs"
FS=$(first_section "$OUT")
case "$FS" in
  drill*) ok "drill stands above every other section (first is: $FS)" ;;
  *)      no "drill not first — first section is: ${FS:-<none>}" ;;
esac
has "each question listed by PRD, id and title" "$OUT" "^  one · Q1 What the board shows a session first$"
has "the second PRD's question too" "$OUT" "^  two · Q1 What the board shows a session first$"

echo "== leg 2 (spec02 box 1): claim refused while the drill is unput"
OUT=$($TRANS claim other w --as engineer 2>&1); RC=$?
ck "$([ $RC -eq 1 ] && echo 0 || echo 1)" "claim exits 1 (got $RC)"
has "claim refused naming asking 2" "$OUT" "asking 2"
has "the refusal says drill first" "$OUT" "drill first"
has "other is untouched: still open" "$(state_of other)" "^state: open"

echo "== leg 3 (spec01 box 2, spec02 box 2): round out — out marks, claim goes"
printf '# Round\n\n## Asked\n- What the board shows a session first · out\n' > "$D/.state/round.md"
OUT=$($PLAN scan 2>&1)
has "one's question marked · out" "$OUT" "^  one · Q1 What the board shows a session first · out$"
has "two's question marked · out" "$OUT" "^  two · Q1 What the board shows a session first · out$"
$TRANS claim other w --as engineer > /dev/null 2>&1; RC=$?
ck "$RC" "claim went through once the round was out (exit $RC)"
has "other moved open → analyzing" "$(state_of other)" "^state: analyzing"
has "other carries the claim line" "$(cat "$D/prds/other/prd.md")" "^claim: w "

echo "== leg 4 (spec01 box 3, spec02 box 3): one question — count, no section, claim goes"
# the round file goes: the one question left is UNPUT, which is the case the
# gate must still let through — one outstanding is step 2's ordinary put.
rm -f "$D/.state/round.md"
{ echo '---'; echo 'state: question'; echo 'priority: 50'; echo '---'
  echo '# f-two — answered'; echo; echo '## Questions'; echo
  echo '### Q1: What the board shows a session first'; echo
  echo 'A session sees the questions it is being asked first, or its work?'
  echo
  echo '1. **Questions first** — opens on what waits on you. (recommended)'
  echo '2. **Work first** — opens on what is happening.'
  echo '3. **Ask each time** — remembers the last.'
  echo
  echo '## Answers'
  echo
  echo '**Q1** — Questions first.'
} > "$D/prds/two/prd.md"
OUT=$($PLAN scan 2>&1)
has "one question prints the count" "$OUT" "asking 1 over 1 PRD"
lacks "no drill section at one question" "$OUT" "^drill"
$TRANS claim other2 w2 --as engineer > /dev/null 2>&1; RC=$?
ck "$RC" "no gate at one: the claim goes through (exit $RC)"
has "other2 moved open → analyzing" "$(state_of other2)" "^state: analyzing"

echo "== leg 5 (spec01 box 4): zero questions — nothing prints"
$TRANS answer one Q1 "Questions first." > /dev/null 2>&1; RC=$?
ck "$RC" "the last question is answered (exit $RC)"
OUT=$($PLAN scan 2>&1)
lacks "zero prints no count" "$OUT" "asking"
lacks "zero prints no section" "$OUT" "^drill"

echo "== leg 6 (spec01 box 5): closed states count zero, and only the state does it"
# `old` (done) and `sup` (superseded) each still hold an unanswered round.
# Flipping the state — and nothing else — is what makes the round count, so
# the exclusion is proved by the count moving, not by an empty board.
OUT=$($PLAN scan 2>&1)
lacks "done + superseded rounds count zero" "$OUT" "asking"
sed -i.bak 's/^state: superseded$/state: open/' "$D/prds/sup/prd.md"; rm -f "$D/prds/sup/prd.md.bak"
OUT=$($PLAN scan 2>&1)
has "the superseded round is real — open, it counts 1" "$OUT" "asking 1 over 1 PRD"
sed -i.bak 's/^state: open$/state: superseded/' "$D/prds/sup/prd.md"; rm -f "$D/prds/sup/prd.md.bak"
sed -i.bak 's/^state: done$/state: open/' "$D/prds/old/prd.md"; rm -f "$D/prds/old/prd.md.bak"
OUT=$($PLAN scan 2>&1)
has "the done round is real — open, it counts 1" "$OUT" "asking 1 over 1 PRD"
sed -i.bak 's/^state: open$/state: done/' "$D/prds/old/prd.md"; rm -f "$D/prds/old/prd.md.bak"
OUT=$($PLAN scan 2>&1)
lacks "both back in CLOSED — zero again" "$OUT" "asking"

echo "== leg 7: questions.py list carries the same count, one reader"
# legs 4-5 answered the frontier; the list check needs it standing again
for n in one two; do qprd "$n"; done
OUT=$($QLIST "$D")
echo "$OUT"
has "list prints one's unanswered count" "$OUT" "^one .* 1 open"
has "list prints two's unanswered count" "$OUT" "^two .* 1 open"
lacks "list does not print an answered PRD as open" "$OUT" "^old .* 1 open"
SCAN=$($PLAN scan 2>&1)
has "and the scan agrees — one reader" "$SCAN" "asking 2 over 2 PRDs"

echo
echo "probe done · failures: $fails"
exit "$fails"

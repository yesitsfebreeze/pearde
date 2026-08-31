#!/usr/bin/env bash
# drill-fixture.sh — the probe for two-questions-start-a-drill.
#
# Builds a four-PRD board in a run-time directory (never under a board's
# prds/) and walks the PRD's Done-when list against it. Every write is a
# heredoc inside this script; every check prints OK or fails the run.
set -euo pipefail
CODE=/Users/feb/dev/infra/pearde
BOARD=/tmp/drill-fg
PLAN="python3 $CODE/resources/board/plan.py"
TRANS="python3 $CODE/resources/board/transitions.py"
QLIST="python3 $CODE/resources/questions.py list"

rm -rf "$BOARD"; mkdir -p "$BOARD/.pearde/prds"/{one,two,other,old} "$BOARD/.pearde/.state"
fails=0

# question PRDs `one` and `two`, one question each, no Answers.
for n in one two; do
  mkdir -p "$BOARD/.pearde/prds/$n"
  { echo '---'
    echo 'state: question'
    echo 'priority: 50'
    echo '---'
    echo "# fixture-$n — question PRD"
    echo
    echo '## Questions'
    echo
    echo '### Q1: What the board shows a session first'
    echo
    echo 'A session opening on this board sees either the questions it is being asked'
    echo 'or the work it could start: which opens?'
    echo
    echo '1. **Questions first** — the page opens on what waits on you; work is one click away. (recommended)'
    echo '2. **Work first** — the page opens on what is happening; questions are one click away.'
    echo '3. **Ask each time** — the page remembers whichever was open last.'
  } > "$BOARD/.pearde/prds/$n/prd.md"
done

# other: the claim target, `open`.
cat > "$BOARD/.pearde/prds/other/prd.md" <<'EOF'
---
state: open
priority: 10
---
# fixture-other — nothing to ask

Plain open PRD, the claim target while a drill is standing.
EOF

# old: `done` with an old unanswered round — history, counts zero.
cat > "$BOARD/.pearde/prds/old/prd.md" <<'EOF'
---
state: done
priority: 10
---
# fixture-old — closed with an old round

## Questions

### Q1: What this closed on

Settled long ago, never carried into the answers?

1. **One** — it closed this way. (recommended)
2. **Two** — it settled the other way.
3. **Three** — a third shape nobody picked.
EOF

cd "$BOARD"

echo "== leg 1: two questions standing"
OUT=$($PLAN scan 2>&1)
echo "$OUT" | sed -n '1,10p'
echo "$OUT" | grep -q "asking 2 over 2 PRDs" && echo "OK: header says asking 2 over 2 PRDs" \
  || { echo "FAIL: header"; fails=$((fails+1)); }
echo "$OUT" | grep -q "^drill — asking 2 over 2 PRDs" && echo "OK: drill section printed" \
  || { echo "FAIL: no drill section"; fails=$((fails+1)); }
# drill stands first — before every other section head
echo "$OUT" | grep -n "^collect\|^drill\|^waiting on you\|^ready\|^gated" | head -1 | grep -q "drill" \
  && echo "OK: drill section stands first" || { echo "FAIL: drill not first"; fails=$((fails+1)); }

echo "== leg 2: claim refused while the drill is unput"
set +e
OUT=$($TRANS claim other w --as engineer 2>&1); RC=$?
set -e
echo "$OUT" | head -1
[ $RC -eq 1 ] && echo "$OUT" | grep -q "asking 2" \
  && echo "OK: claim refused naming asking 2" \
  || { echo "FAIL: claim was not refused with asking 2 (rc=$RC)"; fails=$((fails+1)); }

echo "== leg 3: the round put — ## Asked carries both titles, claim goes"
{ echo "# Round — drill out"
  echo
  echo "## Asked"
  echo "- What the board shows a session first · out"
  echo "- What the board shows a session first · answered"
} > "$BOARD/.pearde/.state/round.md"
OUT=$($PLAN scan 2>&1)
echo "$OUT" | grep -A3 "drill —" | sed -n '1,4p'
set +e
OUT=$($TRANS claim other w --as engineer 2>&1); RC=$?
set -e
[ $RC -eq 0 ] && echo "OK: claim went through once the round was out" \
  || { echo "FAIL: claim still refused: $OUT"; fails=$((fails+1)); }

echo "== leg 4: one question standing — no drill section, claim goes"
{ echo '---'
  echo 'state: question'
  echo 'priority: 50'
  echo '---'
  echo '# fixture-two — answered out'
  echo
  echo '## Questions'
  echo
  echo '### Q1: What the board shows a session first'
  echo
  echo 'A session sees either the questions it is being asked or the work it could'
  echo 'take; whichever the page opens on is what it does first?'
  echo
  echo '1. **Questions first** — the page opens on what waits on you; work is one click away. (recommended)'
  echo '2. **Work first** — the page opens on what is happening; questions are one click away.'
  echo '3. **Ask each time** — the page remembers whichever you opened last.'
  echo
  echo '## Answers'
  echo
  echo '**Q1** — Questions first.'
} > "$BOARD/.pearde/prds/two/prd.md"
OUT=$($PLAN scan 2>&1)
echo "$OUT" | head -1
if echo "$OUT" | grep -q "^drill"; then echo "FAIL: drill section at one question"; fails=$((fails+1));
else echo "OK: one question, no drill section"; fi
# claim must still be refused? other is now `analyzing` from leg 3 — use `one`
# instead: a question PRD cannot be claimed, so check only the gate absence
# on a fresh open PRD
mkdir -p "$BOARD/.pearde/prds/next"
cat > "$BOARD/.pearde/prds/next/prd.md" <<'EOF'
---
state: open
priority: 10
---
# fixture-next — second target

Open, nothing to ask.
EOF
set +e
OUT=$($TRANS claim next w --as engineer 2>&1); RC=$?
set -e
[ $RC -eq 0 ] && echo "OK: one question, claim goes" \
  || { echo "FAIL: one question still gates: $OUT"; fails=$((fails+1)); }

echo "== leg 5: zero questions — the count prints nothing"
PEARDE_AS=engineer $TRANS answer one Q1 "Questions first." > /dev/null 2>&1 || true
OUT=$($PLAN scan 2>&1)
echo "$OUT" | head -1
if echo "$OUT" | grep -q "asking"; then echo "FAIL: zero still prints the count"; fails=$((fails+1));
else echo "OK: zero prints nothing"; fi

echo "== leg 6: a done PRD with an old round counts zero"
OUT=$($PLAN scan 2>&1)
if echo "$OUT" | grep -q "asking"; then echo "FAIL: done PRD counted"; fails=$((fails+1));
else echo "OK: old done PRD excluded (from leg 5's board, old is done)"; fi

echo
echo "probe done · failures: $fails"
echo END
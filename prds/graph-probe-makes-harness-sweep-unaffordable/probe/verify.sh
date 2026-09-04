#!/usr/bin/env bash
# graph-probe-makes-harness-sweep-unaffordable — the probe's own harness.
#
# Run from anywhere:
#   bash .pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh
#
# The contract: the board's --harnesses sweep stays affordable. Its wall-clock
# design is "the slowest harness, not the sum of all of them", so no harness
# may pay for unbounded work — an LLM semantic pass above all. The offender
# was the-graph-lands-inside-the-board's probe: its step [3] ran a full
# `extract <repo> --force`, a doc-chunked LLM dispatch that ran past ten
# minutes before it was killed, every time the sweep ran.
#
# Two things are checked here:
#   A. no harness under the board dispatches graphify extract against a
#      corpus that can carry documents — extract is affordable only when the
#      corpus is code-only (a 0-doc dispatch is seconds) or run on a run-time
#      fixture, never `extract <repo> --force` bare;
#   B. the graph probe itself runs to green inside the sweep's own cost
#      envelope, measured, not assumed.
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

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf '  ok   %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf '  FAIL %s\n' "$1"; }

# ── A. the sweep's harnesses carry no unbounded extract ──────────────────────
# `extract <repo> --force` (or any extract whose target is the real repo and
# whose corpus can hold docs) is the one shape that cost minutes of LLM. A
# fixture extract reads its target from mktemp; --code-only caps the corpus.
HL=$(find "$BOARD/prds" -name verify.sh | sort)
HN=$(printf '%s\n' "$HL" | grep -c .)
# Matched per line, comments excluded: a harness's history comment may name
# the old offender shape ("extract \"$REPO\" --force") without committing it.
# The call may spell graph.sh directly or through $SH — the graph-lands probe
# sets SH=.../graph.sh and the file text never contains the literal.
REALEXTRACT=0; OFFENDERS=""
for h in $HL; do
  while IFS= read -r line; do
    case "$line" in *code-only*) continue ;; esac
    case "$line" in
      *'"$REPO"'*|*'"$ROOT"'*)
        REALEXTRACT=$((REALEXTRACT + 1))
        OFFENDERS="$OFFENDERS
${h#"$BOARD"/}: $line" ;;
    esac
  done < <(grep -E '(graph\.sh|\$SH)[" ]+extract' "$h")
done
if [ "$REALEXTRACT" = 0 ]; then
  ok "no harness runs a full-force extract against a real corpus ($HN harnesses read)"
else
  bad "harness(es) still run full-force extract on a real corpus:$OFFENDERS"
fi
# and the fixture discipline holds: an extract inside a probe builds its
# corpus in a run-time directory, never under the board.
# The matcher must be the SAME spelling check A uses. The one harness that
# calls the extractor spells it through its own SH variable, never as a literal
# script name, so a script-name-only matcher here examines zero files and
# prints ok unconditionally — a check that cannot fail.
# EXAMINED is the denominator that makes that failure visible instead of green.
FIXTUREOK=1; EXAMINED=0
for h in $HL; do
  if grep -qE '(graph\.sh|\$SH)[" ]+extract' "$h"; then
    EXAMINED=$((EXAMINED + 1))
    if ! grep -qE 'mktemp|--code-only' "$h"; then
      FIXTUREOK=0
      bad "extract without a run-time fixture or --code-only: ${h#"$BOARD"/}"
    fi
  fi
done
if [ "$EXAMINED" = 0 ]; then
  bad "the fixture-discipline check examined no harness — its matcher sees nothing"
elif [ "$FIXTUREOK" = 1 ]; then
  ok "every extract in a harness targets a run-time fixture or is code-only ($EXAMINED examined)"
fi

# ── B. the graph probe runs green inside the sweep's cost envelope ──────────
GRAPH_H="$BOARD/prds/the-graph-lands-inside-the-board/probe/verify.sh"
if [ -f "$GRAPH_H" ]; then
  SWEEP_OUT=$(mktemp "${TMPDIR:-/tmp}/graphprobe-sweep.XXXXXX")
  trap 'rm -rf "$SWEEP_OUT"' EXIT
  T0=$(python3 -c 'import time;print(time.time())')
  if bash "$GRAPH_H" >"$SWEEP_OUT" 2>&1; then
    T1=$(python3 -c 'import time;print(time.time())')
    ok "the graph probe runs green"
  else
    T1=$(python3 -c 'import time;print(time.time())')
    bad "the graph probe does not run green — read $SWEEP_OUT"
  fi
  SECS=$(python3 -c "print(f'{$T1-$T0:.1f}')")
  # The envelope: the harnesses row advertises itself as measured in tens of
  # seconds. One harness past 60s is the row's whole budget spent twice.
  if python3 -c "import sys;sys.exit(0 if float('$SECS') < 60 else 1)"; then
    ok "the graph probe finished in ${SECS}s — inside the tens-of-seconds envelope"
  else
    bad "the graph probe took ${SECS}s — past the tens-of-seconds envelope"
  fi
else
  bad "the graph probe harness is missing: $GRAPH_H"
fi

# The line below reports checks executed, not checks expected: drop one to a
# stray `continue` or a quoting slip and it prints a smaller total and exits 0,
# which is indistinguishable from success. Pin the denominator.
[ "$((PASS+FAIL))" = 4 ] || { FAIL=$((FAIL+1)); printf '  FAIL expected 4 checks, ran %s\n' "$((PASS+FAIL))"; }
echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]
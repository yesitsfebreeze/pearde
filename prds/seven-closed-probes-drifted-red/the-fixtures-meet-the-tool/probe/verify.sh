#!/usr/bin/env bash
# the-fixtures-meet-the-tool — every harness red only because its fixture
# predates the tool runs green, and each fixture edit is load-bearing.
#
# Four fixture edits are on trial. For each one this harness proves BOTH
# directions: the tool really does what the fixture did not expect (so the
# edit was owed), and the pre-edit fixture really would still be red (so the
# check can fail). A one-directional check here would pass on a tree where
# nothing had been fixed at all.
#
# Every fixture is built under `mktemp -d` at run time. Nothing here writes
# inside the repo, and no git write runs outside its own mktemp board — a
# runner with a relative `cd` is how an earlier sweep committed the real repo
# by accident, so ROOT is asserted before the first command.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../../.." && pwd)"
[ -f "$ROOT/resources/pearde.py" ] || { echo "refusing: ROOT=$ROOT is not the repo"; exit 2; }
PEARDE="$ROOT/resources/pearde.py"
PLAN="$ROOT/resources/board/plan.py"
TR="$ROOT/resources/board/transitions.py"
PRDS="$ROOT/.pearde/prds"
export PEARDE_AS=engineer
export PEARDE_PORT=1
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
cd "$W"

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ok   $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; [ -n "${2:-}" ] && echo "       $2"; }
eq()  { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "got [$2] want [$3]"; fi; }
has() { if grep -qF -- "$3" <<<"$2"; then ok "$1"; else bad "$1" "missing [$3] in [$2]"; fi; }
no()  { if grep -qF -- "$3" <<<"$2"; then bad "$1" "found [$3]"; else ok "$1"; fi; }
gitq() { ( cd "$1" && git status --porcelain ); }

echo "── A. the parse-cache write, and why clean() had to filter .state/ ──────"
# `scan` persists <board>/.state/parse-cache.json on a parse miss, and every
# harness runs commands that scan. A fixture board is a hand-rolled git repo
# whose .gitignore does not name the cache, so a "the refusal wrote nothing"
# check saw a file the tool was entitled to write. The real board's parent
# .gitignore does ignore `.pearde/.state/` — the product kept its contract.
D="$W/a"; mkdir -p "$D"
python3 "$PLAN" example "$D" >/dev/null 2>&1
( cd "$D" && git init -q && git add -A \
    && git -c user.name=t -c user.email=t@t commit -qm fixture ) >/dev/null
eq "A the fresh fixture board is clean before anything runs" "$(gitq "$D")" ""
python3 "$PEARDE" scan --board "$D/.pearde" >/dev/null 2>&1
eq "A scan wrote the machine-local parse cache" \
   "$( [ -f "$D/.pearde/.state/parse-cache.json" ] && echo yes || echo no )" "yes"
RAW="$(gitq "$D")"
has "A …and git sees it — this is the whole of why the fixtures went red" "$RAW" ".pearde/.state/"
eq "A a clean() that filters .state/ reads empty — the tool wrote nothing else" \
   "$(gitq "$D" | grep -v '\.pearde/\.state/')" ""
# both directions: without the filter the pre-edit fixture is still red.
if [ -n "$RAW" ]; then ok "A an unfiltered clean() would still fail here — the filter is load-bearing"
else bad "A an unfiltered clean() would still fail here — the filter is load-bearing" \
         "git status was empty; the cache write is gone and the edit is dead weight"; fi
# the filter is narrow: it hides .state/ and nothing above it.
touch "$D/.pearde/prds/stray.md"
has "A the filter cannot hide an edit outside .state/" \
    "$(gitq "$D" | grep -v '\.pearde/\.state/')" "prds/stray.md"
rm -f "$D/.pearde/prds/stray.md"
eq "A the two harnesses this contract names carry the filter" \
   "$(grep -l 'git status[^|]*| *grep -v' \
        "$PRDS/an-unknown-flag-refuses/probe/verify.sh" \
        "$PRDS/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh" \
      2>/dev/null | wc -l | tr -d ' ')" "2"

echo
echo "── B. the drill gate, and the pass file's ## Asked ─────────────────────"
# `claim` refuses while two or more unanswered questions have not been put to
# the user. The escape is by design: the pass file's `## Asked` lists the
# titles already put, by title, normalized. The transitions fixture was built
# before that gate existed, so its four questions blocked every claim in it.
FIX="$PRDS/the-board-runs-itself/transitions-are-commands/probe/fixture.py"
eq "B the transitions fixture is where the harness reads it" \
   "$( [ -f "$FIX" ] && echo yes || echo no )" "yes"
has "B …and it now writes the pass file's ## Asked" "$(cat "$FIX")" '## Asked'
# with `## Asked`: the gate is clear, and `claim next` gets through once its
# own needs gate is released.
B2="$W/b"; mkdir -p "$B2"; python3 "$FIX" "$B2" >/dev/null
BB="$B2/.pearde"
COUNT="$(python3 -c "
import sys; sys.path.insert(0, '$ROOT/resources/board')
import plan
q = plan.drill_questions('$BB')
print('%d %d' % (len(q), len([x for x in q if not x[3]])))")"
eq "B four questions stand, and none is still unput" "$COUNT" "4 0"
python3 "$TR" set building done --force --board "$BB" >/dev/null 2>&1
OUTB="$(python3 "$TR" claim next impl-1 --board "$BB" 2>&1)"; RC=$?
eq "B claim next is accepted with ## Asked in place" "$RC" "0"
no "B …and the drill gate never fires" "$OUTB" "drill first"
# without it: the same board, the same command, refused by the drill gate.
B3="$W/c"; mkdir -p "$B3"; python3 "$FIX" "$B3" >/dev/null
: > "$B3/.pearde/.state/pass.md"
CNT3="$(python3 -c "
import sys; sys.path.insert(0, '$ROOT/resources/board')
import plan
print(len([x for x in plan.drill_questions('$B3/.pearde') if not x[3]]))")"
eq "B stripping ## Asked puts all four back on the frontier" "$CNT3" "4"
python3 "$TR" set building done --force --board "$B3/.pearde" >/dev/null 2>&1
# the gate is scoped to what a question can reshape — asker, ancestors,
# descendants, what needs one of them — so `next` goes under the asker.
mv "$B3/.pearde/prds/next" "$B3/.pearde/prds/asking/next"
ERRC="$(python3 "$TR" claim next impl-1 --board "$B3/.pearde" 2>&1 >/dev/null)"; RC=$?
eq "B without ## Asked the same claim is refused — the edit is load-bearing" "$RC" "1"
has "B …in the gate's own words" "$ERRC" "asking 4 — drill first"

echo
echo "── C. every harness ends on a check that carries its exit code ──────────"
# census J in the-gate-runs-the-harnesses reads the last three lines of every
# verify.sh. A harness whose last statement only forwards a captured code
# carries no check, and the census is what notices.
CEN='^\[ .*(FAIL|fail).* \]|exit 1|exit "\$fail"|exit \$\(\( fail != 0 \)\)'
HL="$(find "$PRDS" -name verify.sh | sort)"
HN="$(printf '%s\n' "$HL" | grep -c .)"
NON=0
for h in $HL; do tail -3 "$h" | grep -qE "$CEN" && NON=$((NON+1)); done
eq "C every harness on the board ends on an exit-code-carrying check" "$NON" "$HN"
GP="$PRDS/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh"
eq "C the graph-probe harness is on the board" "$( [ -f "$GP" ] && echo yes || echo no )" "yes"
if tail -3 "$GP" | grep -qE "$CEN"; then ok "C …and its own tail satisfies the census"
else bad "C …and its own tail satisfies the census" "$(tail -3 "$GP")"; fi
# the census can fail: a tail that only forwards a captured code does not match.
if printf 'RC=$?\nexit $RC\n' | grep -qE "$CEN"
then bad "C the census would pass a bare 'exit \$RC' — it cannot fail"
else ok "C a bare 'exit \$RC' is not a check the census accepts"; fi
eq "C the-gate's census row is green" \
   "$(bash "$PRDS/the-gate-runs-the-harnesses/probe/verify.sh" 2>&1 | grep -c '^  FAIL J')" "0"

echo
echo "── D. the README's step table moved to two columns ─────────────────────"
# The pearde-next work re-aimed loop.md's pass table from `| step | command |`
# to `| step | the orchestrator decides |`, and the README mirrors it. The
# readme-in-three-rings harness anchored its awk on the retired header, so it
# read zero rows out of a table that was sitting right there.
RH="$PRDS/the-board-runs-itself/readme-in-three-rings/probe/verify.sh"
OLD='/^\| step \| command/{f=1} f&&/^\| [1-7] /{print} f&&/^$/{f=0}'
NEW='/^\| step \|/{f=1} f&&/^\| [1-7] /{print} f&&/^$/{f=0}'
eq "D the README carries the two-column header" \
   "$(grep -c '^| step | the orchestrator decides |' "$ROOT/README.md")" "1"
eq "D loop.md carries the same header" \
   "$(grep -c '^| step | the orchestrator decides |' "$ROOT/references/parts/loop.md")" "1"
eq "D the retired anchor reads zero rows — this is why the harness was red" \
   "$(awk "$OLD" "$ROOT/README.md" | wc -l | tr -d ' ')" "0"
eq "D the re-aimed anchor reads the seven rows" \
   "$(awk "$NEW" "$ROOT/README.md" | wc -l | tr -d ' ')" "7"
eq "D …and they are loop.md's, byte for byte" \
   "$(diff <(awk "$NEW" "$ROOT/README.md") <(awk "$NEW" "$ROOT/references/parts/loop.md") | wc -l | tr -d ' ')" "0"
no "D the harness no longer holds the retired anchor" "$(cat "$RH")" '| step | command'

echo
echo "── E. the harnesses this contract names run green ───────────────────────"
for rel in an-unknown-flag-refuses \
           the-tool-keeps-its-word/one-predicate-for-dispatchable \
           the-board-runs-itself/transitions-are-commands; do
  bash "$PRDS/$rel/probe/verify.sh" >"$W/log" 2>&1
  eq "E $rel exits 0" "$?" "0"
done
# readme-in-three-rings and the-gate carry rows this contract does not own:
# the quickstart's (init-seeds-a-board-doctor-calls-green) and `index.py
# check`'s silence, which any stray unmanifested file at the repo root breaks.
# What is asserted here is that no OTHER row is red in either.
bash "$PRDS/the-board-runs-itself/readme-in-three-rings/probe/verify.sh" >"$W/rlog" 2>&1
eq "E readme-in-three-rings has no D failure left" "$(grep -c '^FAIL: D' "$W/rlog")" "0"
eq "E …and every row it still fails is the quickstart's or the index's" \
   "$(grep -c '^FAIL: [^HG]' "$W/rlog")" "0"
bash "$PRDS/the-gate-runs-the-harnesses/probe/verify.sh" >"$W/glog" 2>&1
eq "E …and the-gate fails only the two rows that read index.py check" \
   "$(grep -cE '^  FAIL [B-KM]' "$W/glog")" "0"

echo
echo "── F. the contract's non-goal, and the root this fix did not touch ──────"
eq "F no file under resources/ carries any of this" \
   "$( cd "$ROOT" && git diff --name-only -- resources/board/plan.py \
        resources/board/init.py | grep -c . )" "0"
# Re-aimed. This pinned the ABSENCE of a fix: the cache was unignored, that was
# recorded as a finding this PRD would not act on, and the check froze it. The
# fix has since landed, so the non-goal is spent. What is worth guarding now is
# the fix itself — the cache is a rebuilt file and must stay out of the board's
# history — so the check asserts the ignore line is there, and fails if it goes.
eq "F .state/parse-cache.json is git-ignored on the board" \
   "$(grep -c '^\.state/parse-cache\.json$' "$ROOT/.pearde/.gitignore")" "1"
eq "F …and init.py does not seed it either" \
   "$(grep -c 'parse-cache' "$ROOT/resources/board/init.py")" "0"

echo
# reports checks executed, not checks expected: drop one to a quoting slip and
# a smaller total still exits 0. Pin the denominator.
[ "$((PASS+FAIL))" = 35 ] || { FAIL=$((FAIL+1)); printf '  FAIL expected 35 checks, ran %s\n' "$((PASS+FAIL))"; }
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]

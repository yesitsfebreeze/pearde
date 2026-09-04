#!/bin/bash
# the-brief-names-the-verdict-line-collect-requires — the probe's harness.
# One line per assertion, a count at the end. Fixtures are built in a temp dir
# at run time and removed at exit; nothing under .pearde/prds/ is written.
#
# What is under test: a worker that follows the brief verbatim must produce a
# report `pearde collect` accepts. That is two claims — the brief SAYS the
# `Verdict:` line (G1, G2), and the shape it names is the shape
# `collect.verdict_of` actually reads (G4) — plus the checker that keeps both
# true (G3) and the duplicated continuation the same pass deleted (G5).
set -u
# probe/ → the PRD dir → prds/ → .pearde/ → the repo root: four levels
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
BRIEF="${BRIEF_PY:-$ROOT/resources/board/brief.py}"
COLLECT="$ROOT/resources/board/collect.py"
WRK="$ROOT/references/parts/workers.md"
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ok   $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; }
has() { if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1 — missing: $3"; fi; }
eq()  { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 — got: $2 · want: $3"; fi; }

# the `every` block as a worker reads it — the blockquote prefix off
BLOCK=$(awk '/^<!-- brief:every -->$/{on=1;next} /^<!-- \/brief -->$/{if(on)exit} on' \
        "$WRK" | sed -e 's/^> \{0,1\}//')

echo "── G1 the source: brief:every names the line collect reads"
has "brief:every names \`Verdict:\`" "$BLOCK" 'Verdict:'
has "brief:every names the 40-line window" "$BLOCK" '40'
has "brief:every says a report without one is refused" "$BLOCK" 'refused'
# the constraint the PRD set: the tool did not loosen
eq "verdict_of still reads 40 lines only" \
   "$(grep -c 'splitlines()\[:40\]' "$COLLECT")" 1
has "collect still refuses a report naming none" \
    "$(cat "$COLLECT")" 'names no `Verdict:`'
# Scoped to the verdict mechanism, never the whole file: a sibling PRD is
# adding an `--also` guard to collect.py, so a whole-file diff would measure
# that session's work and go red for a reason that is not ours.
SPAN='/^VERDICT_RE/,/^def scores_of/p'
if diff <(git -C "$ROOT" show HEAD:resources/board/collect.py | sed -n "$SPAN") \
        <(sed -n "$SPAN" "$COLLECT") >/dev/null 2>&1
then ok "verdict_of is byte-identical to HEAD — the tool did not loosen"
else bad "verdict_of differs from HEAD — the PRD forbids loosening it"; fi

echo "── G2 the rendered brief, both roles"
python3 "$ROOT/resources/board/plan.py" example "$D/ex" >/dev/null 2>&1 \
  || { echo "  FAIL no example board"; exit 1; }
B="$D/ex/.pearde"; mkdir -p "$B/.state"
for role in analyst implementer; do
  python3 "$BRIEF" big/second --role "$role" --board "$B" --force >"$D/$role.txt" 2>/dev/null
  eq "$role brief carries a \`Verdict:\` line" \
     "$(grep -c 'Verdict:' "$D/$role.txt")" 1
done

echo "── G3 the checker fails on each defect (a check that can fail)"
eq "--check silent on the real file" "$(python3 "$BRIEF" --check 2>&1)" ""
python3 - "$D" "$WRK" <<'PY'
import sys, os, re
d, wrk = sys.argv[1], sys.argv[2]
src = open(wrk, encoding="utf-8").read()
# A: strip the Verdict: sentence out of brief:every — the tree as it was
a = os.path.join(d, "a.md")
blk = re.search(r"(?s)<!-- brief:every -->.*?<!-- /brief -->", src).group(0)
open(a, "w").write(src.replace(blk, re.sub(r"Verdict:", "vrdct", blk)))
# B: put the duplicated continuation back
b = os.path.join(d, "b.md")
dup = "> fits the build ahead, as you would one the PRD already carries. Then read\n"
open(b, "w").write(src.replace(
    dup, dup + "> build ahead, as you would one the PRD already carries. Then read\n"))
PY
for f in a b; do
  N=$(python3 -c "
import sys; sys.path.insert(0, '$ROOT/resources/board')
import brief; print(len(brief.check('$D/$f.md')))")
  if [ "$N" -ge 1 ]; then ok "defect $f is caught ($N problem(s))"
  else bad "defect $f slips past --check"; fi
done

echo "── G4 the shape the brief names is the shape collect reads"
G4=$(python3 - "$ROOT" <<'PY'
import sys
sys.path.insert(0, sys.argv[1] + "/resources/board")
import collect
bad = []
def chk(label, line, want):
    got = collect.verdict_of("# Report\n\n" + line + "\n\nbody\n")
    if got == want:
        print(f"  ok   {label}")
    else:
        bad.append(label)
        print(f"  FAIL {label} — got {got!r} want {want!r}")
# the shape brief:every names: the marker, then one word, alone on the line
for w in collect.VERDICTS:
    chk(f"`Verdict: {w}` reads as {w}", f"Verdict: {w}", w)
# the shapes brief:every warns off — they must stay refused, or the warning
# is stale and the brief is teaching a shape that would in fact be accepted
chk("a list item is read as no verdict", "- Verdict: SPECCED", "")
chk("a block quote is read as no verdict", "> Verdict: SPECCED", "")
chk("past the 40th line is no verdict",
    "\n".join(["x"] * 45) + "\nVerdict: SPECCED", "")
sys.exit(1 if bad else 0)
PY
)
G4RC=$?; echo "$G4"
if [ "$G4RC" -eq 0 ]; then ok "G4: every shape reads as the brief says"
else bad "G4: a shape read differently than the brief says"; fi

echo "── G5 the duplicated continuation is gone"
eq "the half-sentence appears once in workers.md" \
   "$(grep -c 'as you would one the PRD already carries' "$WRK")" 1
eq "no line repeats its predecessor's tail" \
   "$(python3 -c "
import sys; sys.path.insert(0, '$ROOT/resources/board')
import brief; print(len([p for p in brief.check() if 'repeats a line' in p]))")" 0

echo "── G6 the doctor row no longer overstates what it proved"
has "the briefs ok row names the verdict line" \
    "$(grep 'row briefs ok' "$ROOT/resources/doctor.sh")" 'verdict line named'

echo
echo "  $PASS ok · $FAIL FAIL"
[ "$FAIL" -eq 0 ]

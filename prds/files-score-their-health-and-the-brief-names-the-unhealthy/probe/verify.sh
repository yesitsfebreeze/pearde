#!/usr/bin/env bash
# files-score-their-health-and-the-brief-names-the-unhealthy — the scorer,
# the record, the check and the brief, on a synthetic repo.
#
# Run as:
#   bash .pearde/prds/files-score-their-health-and-the-brief-names-the-unhealthy/probe/verify.sh
#
# Every fixture lives under `mktemp -d`; the live daemon is never touched
# (PEARDE_PORT=1). The deep file is generated here, never checked in, so the
# nesting and the branch count are explicit in the loop that writes it.
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
[ -f "$ROOT/resources/pearde.py" ] || { echo "refusing: ROOT=$ROOT is not the repo"; exit 2; }
H="$ROOT/resources/health.py"
export PEARDE_AS=engineer
export PEARDE_PORT=1

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ok    $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL  $1${2:+ — $2}"; }
eq()  { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "got [$2] want [$3]"; fi; }
has() { if grep -qF -- "$3" <<<"$2"; then ok "$1"; else bad "$1" "missing [$3] in [$(printf '%s' "$2" | head -c 300)]"; fi; }
not() { if grep -qF -- "$3" <<<"$2"; then bad "$1" "found [$3]"; else ok "$1"; fi; }

W="$(mktemp -d /tmp/pearde-health.XXXXXX)"
trap 'rm -rf "$W"' EXIT INT TERM
D="$W/repo"
mkdir -p "$D/.pearde/prds" "$D/src"
printf -- '---\nname: health-fixture\nlanguage: English\n---\n' > "$D/.pearde/settings.md"

# src/deep.py — one function, nine nested ifs, sixty-odd branch points, ~900 lines
python3 - "$D/src/deep.py" <<'PY'
import sys
out = ["def deep(x):"]
for d in range(9):
    out.append("    " * (d + 1) + f"if x > {d}:")
body = "    " * 10
for i in range(60):
    out.append(body + f"x = x + 1 if x % {i + 2} else x - 1")
for i in range(820):
    out.append(body + f"x = x + {i}")
out.append(body + "return x")
open(sys.argv[1], "w").write("\n".join(out) + "\n")
PY
printf 'def f():\n    return 1\n' > "$D/src/tiny.py"
printf '# Fixture\n\ntwo lines of prose\n' > "$D/README.md"
head -c 512 /dev/urandom > "$D/blob.bin"
printf 'x' > "$D/lib.min.js"
( cd "$D" && git init -q -b main && git add -A && git -c user.name=t -c user.email=t@t commit -qm base ) || { echo "refusing: git init failed"; exit 2; }
( cd "$D/.pearde" && git init -q -b board && printf 'x\n' > .gitignore && git add -A && git -c user.name=t -c user.email=t@t commit -qm board ) >/dev/null 2>&1

run() { python3 "$H" "$@" --board "$D/.pearde" 2>&1; }
note() { cat "$D/.pearde/health/files/$1" 2>/dev/null; }
fm() { grep -m1 "^$2:" <<<"$(note "$1")" | awk '{print $2}'; }

# ── A. no graph: scored on three axes, ranking worst first, skips counted ────
OUT="$(run score)"; RC=$?
eq  "A1 score exits 0 without a graph" "$RC" "0"
has "A2 the summary says graph none" "$OUT" "graph none"
eq  "A3 deep.py's note says graph none" "$(fm src-deep.py.md graph)" "none"
eq  "A4 deep.py's fan_in is none" "$(fm src-deep.py.md fan_in)" "none"
DEEP="$(fm src-deep.py.md score)"; TINY="$(fm src-tiny.py.md score)"
if [ "${DEEP:-100}" -lt 40 ] && [ "${TINY:-0}" -ge 95 ]; then ok "A5 deep $DEEP < 40 <= 95 <= tiny $TINY"; else bad "A5 deep < 40 <= 95 <= tiny" "deep=$DEEP tiny=$TINY"; fi
FIRST="$(grep -m1 '^| \*\*' "$D/.pearde/health/ranking.md" | cut -d'|' -f3 | tr -d ' ')"
eq  "A6 the ranking's first row is deep.py" "$FIRST" "src/deep.py"
eq  "A7 README.md is scored as markdown" "$(fm README.md.md language)" "markdown"
[ ! -e "$D/.pearde/health/files/blob.bin.md" ] && [ ! -e "$D/.pearde/health/files/lib.min.js.md" ] && ok "A8 the binary and the minified file have no note" || bad "A8 the binary and the minified file have no note"
eq  "A9 the ranking counts two skipped" "$(grep -m1 '^skipped:' "$D/.pearde/health/ranking.md" | awk '{print $2}')" "2"
has "A10 health/ is ignored on the board" "$(cat "$D/.pearde/.gitignore")" "health/"

# ── B. every score is an integer 1-100 ───────────────────────────────────────
BAD=0
for f in "$D"/.pearde/health/files/*.md; do
  s="$(grep -m1 '^score:' "$f" | awk '{print $2}')"
  case "$s" in ''|*[!0-9]*) BAD=1;; *) [ "$s" -ge 1 ] && [ "$s" -le 100 ] || BAD=1;; esac
done
eq  "B1 every note's score is an integer 1-100" "$BAD" "0"

# ── C. check is silent on a clean record ─────────────────────────────────────
OUT="$(run check)"; RC=$?
eq  "C1 check exits 0" "$RC" "0"
eq  "C2 check prints nothing" "$OUT" ""

# ── D. check catches a bad key and an orphan note ────────────────────────────
N="$D/.pearde/health/files/src-tiny.py.md"
cp "$N" "$W/tiny.bak"
python3 - "$N" <<'PY'
import sys; p=sys.argv[1]; t=open(p).read().replace("graph: none\n", "graph: none\nbogus: 1\n", 1); open(p,"w").write(t)
PY
OUT="$(run check)"; RC=$?
eq  "D1 a note with an undeclared key exits 1" "$RC" "1"
has "D2 and names the key" "$OUT" "\`bogus\` is not in the closed set"
cp "$W/tiny.bak" "$N"
( cd "$D" && git rm -q src/tiny.py && git -c user.name=t -c user.email=t@t commit -qm drop )
OUT="$(run check)"; RC=$?
eq  "D3 a note for an untracked file exits 1" "$RC" "1"
has "D4 and names the file" "$OUT" "src/tiny.py is no longer tracked"
run score >/dev/null
[ ! -e "$N" ] && ok "D5 a full score drops the orphan note" || bad "D5 a full score drops the orphan note"
eq  "D6 and check is silent again" "$(run check)" ""
( cd "$D" && git checkout -q HEAD~1 -- src/tiny.py && git -c user.name=t -c user.email=t@t commit -qm back )

# ── E. a graph: fan_in, callers, the graph's commit on the note ──────────────
mkdir -p "$D/.pearde/graphify"
cat > "$D/.pearde/graphify/graph.json" <<'JSON'
{"directed": false, "nodes": [
  {"id": "src_deep", "label": "deep.py", "source_file": "src/deep.py", "metadata": {"kind": "file"}},
  {"id": "src_deep_deep", "label": "deep()", "source_file": "src/deep.py"},
  {"id": "src_tiny", "label": "tiny.py", "source_file": "src/tiny.py", "metadata": {"kind": "file"}},
  {"id": "src_tiny_f", "label": "f()", "source_file": "src/tiny.py"}],
 "links": [
  {"source": "src_tiny_f", "target": "src_deep_deep", "relation": "calls", "source_file": "src/tiny.py"},
  {"source": "src_tiny", "target": "src_tiny_f", "relation": "contains", "source_file": "src/tiny.py"}],
 "built_at_commit": "abc1234def"}
JSON
OUT="$(run score)"
has "E1 the summary names the graph" "$OUT" "graph abc1234"
eq  "E2 deep.py's fan_in is 1" "$(fm src-deep.py.md fan_in)" "1"
has "E3 deep.py's Callers list tiny.py" "$(note src-deep.py.md)" "- src/tiny.py"
eq  "E4 the note carries the graph's commit" "$(fm src-deep.py.md graph)" "abc1234"
eq  "E5 tiny.py's fan_out is 1" "$(fm src-tiny.py.md fan_out)" "1"

# ── F. a subset score rewrites one note and rebuilds the whole ranking ───────
DEEP_MT="$(stat -f %m "$D/.pearde/health/files/src-deep.py.md" 2>/dev/null || stat -c %Y "$D/.pearde/health/files/src-deep.py.md")"
sleep 1
run score "$D/src/tiny.py" >/dev/null
DEEP_MT2="$(stat -f %m "$D/.pearde/health/files/src-deep.py.md" 2>/dev/null || stat -c %Y "$D/.pearde/health/files/src-deep.py.md")"
eq  "F1 deep.py's note is untouched by a subset score" "$DEEP_MT" "$DEEP_MT2"
eq  "F2 the ranking still lists every note" "$(grep -c '^| [0-9*]' "$D/.pearde/health/ranking.md")" "3"

# ── G. the knobs: a weight moves the score, a bad one is one line and a 1 ────
printf -- '---\nname: health-fixture\nlanguage: English\nhealth-weights: lines=100 branching=0 longest=0\n---\n' > "$D/.pearde/settings.md"
run score >/dev/null
DEEP2="$(fm src-deep.py.md score)"
[ "$DEEP2" != "$DEEP" ] && ok "G1 lines alone gives deep.py a different score ($DEEP → $DEEP2)" || bad "G1 lines alone gives deep.py a different score" "still $DEEP"
printf -- '---\nname: health-fixture\nlanguage: English\nhealth-weights: lines=x\n---\n' > "$D/.pearde/settings.md"
OUT="$(run score)"; RC=$?
eq  "G2 an unreadable weight exits 1" "$RC" "1"
has "G3 and says which" "$OUT" "\`lines=x\` is not a number"
has "G4 and still writes the record" "$OUT" "scored"
printf -- '---\nname: health-fixture\nlanguage: English\n---\n' > "$D/.pearde/settings.md"

# ── H. a file the parser refuses is measured by the heuristic ────────────────
printf 'def (:\n    if x:\n        pass\n' > "$D/src/broken.py"
( cd "$D" && git add src/broken.py && git -c user.name=t -c user.email=t@t commit -qm broken )
run score >/dev/null
has "H1 the note says heuristic, and why" "$(note src-broken.py.md)" "measured by heuristic (ast: SyntaxError"

# ── I. usage, and the dispatcher's help ──────────────────────────────────────
run frob >/dev/null 2>&1; eq "I1 an unknown verb exits 2" "$?" "2"
has "I2 pearde help lists health" "$(python3 "$ROOT/resources/pearde.py" help 2>&1)" "health"
eq  "I3 health.py imports stdlib only" "$(grep -E '^(import|from) ' "$H" | awk '{print $2}' | grep -vxE 'ast|datetime|json|math|os|re|subprocess|sys' | wc -l | tr -d ' ')" "0"

# ── J. the brief names the unhealthy file in the footprint ───────────────────
mkdir -p "$D/.pearde/prds/touch-deep"
cat > "$D/.pearde/prds/touch-deep/prd.md" <<'MD'
---
state: specced
origin: requested
priority: 1
complexity: 5
footprint:
  - src/deep.py
---
# Touch deep

Edit deep.py.

## Acceptance

- [ ] one box
MD
BRIEF="$(cd "$D" && python3 "$ROOT/resources/board/brief.py" touch-deep --role implementer --force --board "$D/.pearde" 2>&1)"
has "J1 the brief names src/deep.py under the health floor" "$BRIEF" "src/deep.py  branching"
not "J2 and not tiny.py, which is healthy" "$BRIEF" "src/tiny.py"
rm -rf "$D/.pearde/health"
BRIEF="$(cd "$D" && python3 "$ROOT/resources/board/brief.py" touch-deep --role implementer --force --board "$D/.pearde" 2>&1)"
has "J3 with no record the brief says so" "$BRIEF" "no health record"

echo
[ "$((PASS+FAIL))" = 37 ] || echo "  FAIL  the probe ran $((PASS+FAIL)) checks, not the 37 it holds"
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]

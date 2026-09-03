#!/usr/bin/env bash
# probe — every module finds its siblings by one rule
#
# What this measures: whether a file under resources/ can move to another
# directory under resources/ with no second edit anywhere. Every assertion
# below was run for real before it was written down; none is a prediction.
#
# It copies the tree into a scratch dir made at run time and moves files
# there. The repo it is run from is never written to.
#
#   bash .pearde/prds/resources-are-organised-by-responsibility/\
# every-module-finds-its-siblings-by-one-rule/probe/verify.sh
#
# PEARDE_ROOT names the tree to copy; it defaults to the repo above the board.
set -u
P=0; F=0
ok()  { if [ "$2" = 0 ]; then P=$((P+1)); echo "  ok   $1"; else F=$((F+1)); echo "  FAIL $1 — $3"; fi; }
eq()  { [ "$2" = "$3" ]; ok "$1" $? "want '$3', got '$2'"; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"
# The runner names the tree to measure; with none named, the repo above the
# board this file sits in. BOARD is found by walking up to the board dir, so
# no count of `..` has to match how deep this PRD sits. This file used to
# prefer $PWD over both, which made a by-hand run resolve a different tree
# depending on where it was started from; the runner names the root instead.
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT

echo "probe: every module finds its siblings by one rule — tree $ROOT"

fresh() {   # a clean copy of resources/ in $D, no bytecode
  rm -rf "$D/resources"
  cp -R "$ROOT/resources" "$D/resources"
  find "$D" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
}

# ── 1. the one file exists and knows the whole of resources/ ─────────────────
[ -f "$ROOT/resources/pearde_path.py" ]
ok "resources/pearde_path.py is the one file the rule lives in" $? "not on disk"

DIRS=$(cd "$ROOT" && python3 -c '
import os, sys
sys.path.insert(0, "resources")
import pearde_path as p
print(" ".join(os.path.basename(d) for d in p.dirs()))')
case "$DIRS" in
  "resources board"*) R=0 ;; *) R=1 ;;
esac
ok "it names resources/ and every directory under it: $DIRS" $R "got: $DIRS"

SHADOW=$(cd "$ROOT" && python3 -c '
import os, sys
sys.path.insert(0, "resources")
import pearde_path as p
std = set(sys.stdlib_module_names)
print(len([n for d in p.dirs() for n in os.listdir(d)
           if n.endswith(".py") and n[:-3] in std]))')
eq "no file on that path shadows a stdlib module" "$SHADOW" "0"

# ── 2. the root probe is resources/pearde.py, the file that cannot move ──────
N_OLD=$(grep -rl '"resources", "board", "plan.py"' "$ROOT/resources" 2>/dev/null | wc -l | tr -d ' ')
eq "no entry point still probes for resources/board/plan.py" "$N_OLD" "0"
N_NEW=$(grep -rl '"resources", "pearde.py"' "$ROOT/resources" 2>/dev/null | wc -l | tr -d ' ')
eq "the probe is written out once, in pearde_path.py" "$N_NEW" "1"

# ── 3. renaming resources/board/ breaks nothing, with no code changed ────────
# This is assertion 1 of the parent PRD's probe, inverted. It used to print
# "pearde: no resources/board/plan.py above this file" and die.
BASE=$(cd "$ROOT" && python3 resources/pearde.py help 2>/dev/null)
fresh
mv "$D/resources/board" "$D/resources/core"
OUT=$(cd "$D" && python3 resources/pearde.py help 2>&1)
[ "$OUT" = "$BASE" ]
ok "renaming resources/board/ to core/ leaves 'pearde help' byte-identical" $? \
   "$(printf '%s' "$OUT" | head -1)"

# ── 4. the modules split four ways, with no code changed ─────────────────────
# read/ write/ draw/ run/ — the shape @.pearde/prds/resources-are-organised-by-
# responsibility/ asks for. plan.py stays put: it is the sibling PRD's file and
# is the one module this rule does not reach yet (see 7).
fresh
mkdir -p "$D/resources/read" "$D/resources/write" "$D/resources/draw" "$D/resources/run"
mv "$D/resources/board/specs.py"       "$D/resources/read/"
mv "$D/resources/board/orphans.py"     "$D/resources/read/"
mv "$D/resources/board/transitions.py" "$D/resources/write/"
mv "$D/resources/board/collect.py"     "$D/resources/write/"
mv "$D/resources/board/init.py"        "$D/resources/write/"
mv "$D/resources/board/machine.py"     "$D/resources/run/"
mv "$D/resources/board/dispatch.py"    "$D/resources/run/"
mv "$D/resources/board/ramp.py"        "$D/resources/run/"
mv "$D/resources/board/brief.py"       "$D/resources/run/"
mv "$D/resources/board/all.py"         "$D/resources/draw/"
mv "$D/resources/memos.py"             "$D/resources/read/"
mv "$D/resources/workflows.py"         "$D/resources/read/"
mv "$D/resources/questions.py"         "$D/resources/read/"
mv "$D/resources/health.py"            "$D/resources/read/"
mv "$D/resources/guard.py"             "$D/resources/run/"

OUT=$(cd "$D" && python3 resources/pearde.py help 2>&1)
[ "$OUT" = "$BASE" ]
ok "15 modules moved to four new directories — 'pearde help' byte-identical" $? \
   "$(diff <(printf '%s\n' "$BASE") <(printf '%s\n' "$OUT") | head -3 | tr '\n' ' ')"

for m in specs.py transitions.py machine.py brief.py memos.py guard.py; do
  OUT=$(cd "$D" && python3 -c "
import sys; sys.path.insert(0, 'resources')
import pearde_path, importlib.util as u
p = pearde_path.script('$m')
s = u.spec_from_file_location('probe_${m%.py}', p); m2 = u.module_from_spec(s)
s.loader.exec_module(m2); print('ok')" 2>&1 | tail -1)
  [ "$OUT" = ok ]; ok "$m imports its siblings from its new directory" $? "got: $OUT"
done

# ── 5. a sibling script launched as a subprocess is found, not spelled ───────
# sys.path does nothing for a subprocess addressed by path.
OUT=$(cd "$D" && python3 -c "
import sys; sys.path.insert(0, 'resources')
import pearde_path as p, os
for n in ('serve.py', 'health.py', 'memos.py', 'grammar.py', 'doctor.sh',
          'knowledge.py', 'plan.py'):
    q = p.script(n)
    assert q and os.path.isfile(q), n
print('ok')" 2>&1 | tail -1)
[ "$OUT" = ok ]; ok "pearde_path.script finds every launched sibling after the move" $? "got: $OUT"

N_SPELLED=$(grep -rnE 'os\.path\.join\((HERE|DIR|BOARD|SELF|RES)[^)]*\.(py|sh)"\)' \
            "$ROOT/resources" --include='*.py' 2>/dev/null | wc -l | tr -d ' ')
eq "no python file addresses a sibling script as a path it builds itself" "$N_SPELLED" "0"

# Only a launch counts. `@resources/board/plan.py` in a docstring is a map
# anchor and belongs to the child that moves the file, not to this one.
N_BOARDSTR=$(grep -rnE '(python3|sys\.executable)[^#]*board/[a-z-]+\.(py|js)|"board", "[a-z]+\.py"' \
             "$ROOT/resources" --include='*.py' --include='*.sh' 2>/dev/null \
             | wc -l | tr -d ' ')
eq "no launcher spells board/ any more" "$N_BOARDSTR" "0"

# ── 6. the shell half: doctor.sh finds what it launches ──────────────────────
grep -q '^res() {' "$ROOT/resources/doctor.sh"
ok "doctor.sh carries res() — the shell half of the same rule" $? "not found"
N_DOC=$(grep -c '\$DIR/board/' "$ROOT/resources/doctor.sh" || true)
eq "doctor.sh spells \$DIR/board/ nowhere" "$N_DOC" "0"
sed -n '/^res() {/,/^}/p' "$D/resources/doctor.sh" > "$D/res.sh"
OUT=$(DIR="$D/resources" bash -c '
  . "$1/res.sh"
  for n in plan.py serve.py brief.py; do
    q=$(res "$n") || { echo "miss $n"; exit 1; }
    [ -f "$q" ] || { echo "bad $n -> $q"; exit 1; }
  done
  echo ok' _ "$D" 2>&1 | tail -1)
[ "$OUT" = ok ]; ok "res() finds plan.py, serve.py and brief.py in the cut tree" $? "got: $OUT"

# ── 7. what the rule does not reach: plan.py, the sibling PRD's file ─────────
# plan.py keeps its own two-line preamble — resources/ and its own directory —
# because @.pearde/prds/resources-are-organised-by-responsibility/the-largest-
# module-is-cut-by-responsibility owns that file and the two run at once. That
# preamble reaches render.py and transitions.py only while they sit beside it.
grep -q 'import pearde_path' "$ROOT/resources/board/plan.py" 2>/dev/null; R=$?
[ "$R" != 0 ]
ok "plan.py is untouched — the sibling PRD owns it, so it is out of this footprint" $? \
   "plan.py now imports pearde_path, which collides with the sibling PRD"
fresh
mkdir -p "$D/resources/read" "$D/resources/draw"
mv "$D/resources/board/plan.py"   "$D/resources/read/"
mv "$D/resources/board/render.py" "$D/resources/draw/"
OUT=$(cd "$D" && python3 resources/read/plan.py scan 2>&1 | tail -1)
case "$OUT" in *"No module named 'render'"*) R=0 ;; *) R=1 ;; esac
ok "run as a script from a new directory, plan.py alone still cannot find render — the handoff" $R \
   "got: $OUT"

# ── 8. every other module carries the rule ───────────────────────────────────
N_BOOT=$(grep -rl 'import pearde_path' "$ROOT/resources" --include='*.py' 2>/dev/null | wc -l | tr -d ' ')
[ "$N_BOOT" -ge 14 ]; ok "$N_BOOT modules open with the one rule" $? "expected 14 or more"
MISSING=$(cd "$ROOT" && python3 -c '
import os, re, sys
sys.path.insert(0, "resources")
import pearde_path as p
sib = re.compile(r"^import (?!os|sys|re|json|time|glob|subprocess|shutil|hashlib|math|html|random|argparse|textwrap|tempfile|difflib|itertools|collections|datetime|urllib|importlib|webbrowser|socket|signal|threading|traceback|unicodedata|base64|struct|http|email|mimetypes|stat|errno|platform|getpass|uuid|csv|sqlite3|typing|functools|contextlib|copy|string|shlex|fnmatch|zipfile|gzip|io|pathlib|ast|inspect|logging|secrets|ssl|select|queue|pprint|difflib)([a-z_]+)", re.M)
bad = []
for d in p.dirs():
    for n in sorted(os.listdir(d)):
        if not n.endswith(".py") or n in ("pearde_path.py", "plan.py"):
            continue
        s = open(os.path.join(d, n), encoding="utf-8").read()
        if sib.search(s) and "import pearde_path" not in s:
            bad.append(n)
print(" ".join(bad))')
eq "no module imports a sibling without the rule (plan.py excepted)" "${MISSING:-none}" "none"

echo
echo "probe: $P passed, $F failed"
[ "$F" = 0 ]

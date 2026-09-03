#!/usr/bin/env bash
# probe — resources are organised by responsibility
#
# What this measures: what breaks when resources/ is cut into directories
# named for what the files in them are responsible for. Every assertion below
# was run for real before it was written down; none is a prediction.
#
# It copies the tree into a scratch dir made at run time and cuts it there.
# The repo it is run from is never written to.
#
#   bash prds/resources-are-organised-by-responsibility/probe/verify.sh
#
# PEARDE_ROOT names the tree to copy; it defaults to the repo above the board.
set -u
P=0; F=0
ok()  { if [ "$2" = 0 ]; then P=$((P+1)); echo "  ok   $1"; else F=$((F+1)); echo "  FAIL $1 — $3"; fi; }
eq()  { [ "$2" = "$3" ]; ok "$1" $? "want '$3', got '$2'"; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT

echo "probe: resources are organised by responsibility — tree $ROOT"

# ── what the tree looks like now ─────────────────────────────────────────────
N_LOOSE=$(ls "$ROOT/resources" | grep -cE '\.(py|sh)$')
N_BOARD=$(ls "$ROOT/resources/board" 2>/dev/null | grep -cE '\.py$')
[ "$N_LOOSE" -ge 10 ]; ok "resources/ holds $N_LOOSE loose scripts at one level" $? "expected 10 or more"
[ "$N_BOARD" -ge 15 ]; ok "resources/board/ holds $N_BOARD python modules in one directory" $? "expected 15 or more"

# ── 1. the skill-root probe is nailed to resources/board/plan.py ─────────────
# Every entry point walks up looking for that exact path. Rename the directory
# and the whole command surface dies, with no file moved and no code changed.
cp -R "$ROOT/resources" "$D/resources"
find "$D" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
mv "$D/resources/board" "$D/resources/core"
OUT=$(cd "$D" && python3 resources/pearde.py help 2>&1 | head -1)
case "$OUT" in *"no resources/board/plan.py"*) R=0 ;; *) R=1 ;; esac
ok "renaming resources/board/ alone breaks 'pearde help' at the root probe" $R "got: $OUT"

N_PROBE=$(grep -rl 'resources", "board", "plan.py"' "$ROOT/resources" 2>/dev/null | wc -l | tr -d ' ')
eq "the root probe is written out in $N_PROBE files, not one" "$N_PROBE" "2"

# ── 2. one module's module-level exit takes down every command ───────────────
# discover() wraps exec_module in `except Exception`. brief.py's root probe
# ends in sys.exit(2), which is SystemExit — a BaseException. So a single
# module that cannot find its root kills `scan`, `plan` and `help` alike.
grep -q 'except Exception' "$ROOT/resources/pearde.py"; ok "pearde.py discovery catches Exception" $? "not found"
grep -q 'sys.exit(2)' "$ROOT/resources/board/brief.py"; ok "brief.py's root probe exits with SystemExit, which that catch does not hold" $? "not found"

# ── 3. the split breaks every bare cross-import ──────────────────────────────
# The modules address each other by bare name — `import plan`, `import edit`.
# That works only while each one's own directory carries the others.
rm -rf "$D/resources"; cp -R "$ROOT/resources" "$D/resources"
find "$D" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
mkdir -p "$D/resources/read" "$D/resources/write"
mv "$D/resources/board/plan.py" "$D/resources/read/"
mv "$D/resources/board/transitions.py" "$D/resources/write/"
OUT=$(cd "$D" && python3 resources/write/transitions.py 2>&1 | tail -1)
case "$OUT" in *"No module named"*) R=0 ;; *) R=1 ;; esac
ok "a module moved away from its siblings cannot import them" $R "got: $OUT"

N_BARE=$(grep -hcE '^import [a-z]+ as [a-z]+lib|^import (plan|edit|memos|specs|transitions|serve|render|machine|lanes|collect|workflows|questions|all)\b' "$ROOT/resources/board"/*.py "$ROOT/resources"/*.py 2>/dev/null | paste -sd+ - | bc)
[ "$N_BARE" -ge 30 ]; ok "$N_BARE bare cross-imports would have to resolve from a new directory" $? "expected 30 or more"

# ── 4. one shared path rule makes the split work ─────────────────────────────
# Put every directory under resources/ on sys.path from one file, and the same
# move goes through untouched.
cat > "$D/resources/pearde_path.py" <<'PY'
import os
import sys
RES = os.path.dirname(os.path.abspath(__file__))
for _d in [RES] + [os.path.join(RES, n) for n in sorted(os.listdir(RES))]:
    if os.path.isdir(_d) and _d not in sys.path:
        sys.path.insert(0, _d)
PY
python3 - "$D" <<'PY'
import os, re, sys
d = sys.argv[1]
p = os.path.join(d, "resources", "write", "transitions.py")
s = open(p).read()
boot = ("sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
        "import pearde_path  # noqa: E402,F401\n")
lines, first, out = s.splitlines(keepends=True), True, []
for line in lines:
    if re.match(r'^sys\.path\.insert\(0, .*\)\s*$', line):
        if first:
            out.append(boot); first = False
        continue
    out.append(line)
open(p, "w").write("".join(out))
PY
OUT=$(cd "$D" && python3 resources/write/transitions.py 2>&1 | head -1)
case "$OUT" in *"transitions"*) R=0 ;; *) R=1 ;; esac
ok "one shared path file restores the cross-import after the move" $R "got: $OUT"

# ── 5. a sibling script addressed by path is not fixed by sys.path ───────────
# init.py launches serve.py as `os.path.join(HERE, "serve.py")`. sys.path does
# nothing for a subprocess spelled by path — these have to be found, not guessed.
grep -q 'SERVE = os.path.join(HERE, "serve.py")' "$ROOT/resources/board/init.py"
ok "init.py addresses serve.py as a file beside itself" $? "spelling changed"
N_SIB=$(grep -rnE 'os\.path\.join\((HERE|DIR|BOARD|SELF)[^)]*\.(py|sh)"\)' "$ROOT/resources"/*.py "$ROOT/resources/board"/*.py 2>/dev/null | wc -l | tr -d ' ')
[ "$N_SIB" -ge 3 ]; ok "$N_SIB sibling scripts are addressed by a path built from a directory" $? "expected 3 or more"

# ── 6. doctor.sh spells the directory itself ─────────────────────────────────
N_DOC=$(grep -cE '\$DIR/board/|resources/board/' "$ROOT/resources/doctor.sh")
[ "$N_DOC" -ge 8 ]; ok "doctor.sh spells resources/board/ in $N_DOC places — adapters, brief, plan, serve" $? "expected 8 or more"
grep -q 'if \[ -d "\$DIR/board/adapters" \]' "$ROOT/resources/doctor.sh"
ok "the plugins row is gated on \$DIR/board/adapters, so a move drops the row rather than reddening it" $? "spelling changed"

# ── 7. the map check names one problem per moved file ────────────────────────
N_ROWS=$(grep -c '^| @resources/board/' "$ROOT/references/files.md")
[ "$N_ROWS" -ge 25 ]; ok "$N_ROWS manifest rows in references/files.md name resources/board/" $? "expected 25 or more"
N_IDX=$(grep -o '@resources/board/' "$ROOT/index.md" | wc -l | tr -d ' ')
[ "$N_IDX" -ge 10 ]; ok "$N_IDX index.md scope anchors name resources/board/" $? "expected 10 or more"

# ── 8. the board's own harnesses spell the directory ─────────────────────────
BOARD="${PEARDE_BOARD:-$ROOT/pearde}"
if [ -d "$BOARD/prds" ]; then
  N_HAR=$(grep -rl 'resources/board/' --include='verify.sh' "$BOARD/prds" 2>/dev/null | wc -l | tr -d ' ')
  [ "$N_HAR" -ge 40 ]; ok "$N_HAR committed verify.sh harnesses spell resources/board/ — the doctor harnesses row" $? "expected 40 or more"
else
  echo "  --   board harness count skipped — no $BOARD/prds"
fi

# ── 9. node is needed by nothing a person runs by hand ───────────────────────
# lit-core.min.js is vendored and loaded from disk; the only downloaded package
# is playwright-core, and only the two page tests import it.
grep -q 'playwright' "$ROOT/resources/board/package.json" 2>/dev/null
ok "the one downloaded package is playwright-core, wanted by the page tests alone" $? "package.json changed or absent"
N_PW=$(grep -rl 'playwright' "$ROOT/resources/board"/*.js 2>/dev/null | wc -l | tr -d ' ')
eq "only the page tests import it" "$N_PW" "2"
grep -q 'LIT_FILE = "lit-core.min.js"' "$ROOT/resources/board/render.py"
ok "lit is vendored — render.py inlines the copy as an import map, nothing is downloaded to draw the page" $? "not found"
grep -q 'os.path.dirname(os.path.abspath(__file__)), name' "$ROOT/resources/board/render.py"
ok "render.py reads its assets from its own directory, so lit-core.min.js and view.css must land beside it" $? "spelling changed"
grep -q 'resources/board/node_modules/' "$ROOT/.gitignore"
ok "node_modules is already untracked — dropping it costs no tracked file" $? "not in .gitignore"

echo
echo "probe: $P passed, $F failed"
[ "$F" = 0 ]

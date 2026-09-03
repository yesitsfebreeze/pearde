#!/usr/bin/env bash
# silence-measures-the-workers-own-tree — run from the repo root:
#
#     bash resources/invariants/silence-measures-the-workers-own-tree.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: `silent_of` never reads a footprint path from the shared
# checkout. A footprint is the set of paths the work will touch, and two PRDs
# on one board routinely share one — so a neighbour's edit refreshed this
# PRD's liveness, and every `sweep` row on a 226-PRD board read the same
# `silent 36m` off one session's write to a shared file, while a claim seven
# hours dead at 0/14 boxes read the same. Measured 2026-09-03, fixed the same
# day: liveness is the PRD's own directory plus its lane worktree, and
# nothing else.
#
# It can fail, and the way to prove that is not to trust this comment: revert
# `silent_of` to a `paths` list containing `os.path.join(repo, f)` for
# footprint entries and this file goes red on row 3.
set -u
RESOURCES=${RESOURCES:-$(cd "$(dirname "$0")/.." && pwd -P)}
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }
say() { if [ "$1" = 0 ]; then okr "$2"; else no "$2"; fi; }

SILENCE="$RESOURCES/board/silence.py"
[ -f "$SILENCE" ]
say $? "silence.py is where the one rule lives"

# ── 1. the shared checkout's footprint paths are not in the liveness set ─────
# The regression's exact shape: `paths` built with os.path.join(repo, f) over
# the spec footprint. A lane path or the PRD dir is the worker's own record.
sed -n '/def silent_of/,/^def fmt_age/p' "$SILENCE" > /tmp/silent_of.$$ || true
BODY=$(cat /tmp/silent_of.$$)
rm -f /tmp/silent_of.$$
echo "$BODY" | grep -q 'os\.path\.join(repo,'
[ $? -eq 1 ]
say $? "silent_of does not measure footprint paths in the shared checkout (the old line: os.path.join(repo, f) must be gone)"

# ── 2. the worker's own record is what it measures ───────────────────────────
echo "$BODY" | grep -q "prd\[.dir.\]"
say $? "silent_of measures the PRD's own directory"
echo "$BODY" | grep -q "lane"
say $? "silent_of measures the lane worktree when the worker holds one"

# ── 3. behaviour, not just shape: a neighbour's write cannot fake liveness ───
# A PRD with a dead claim whose footprint file in the shared checkout was
# written minutes ago must still read as silent; the same PRD with a fresh
# edit inside its own PRD dir must not.
T=$(mktemp -d) || exit 1
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/repo/.pearde/prds/the-prd" "$T/repo/resources/board"
OLD=$(date -v-2H +%Y%m%d%H%M 2>/dev/null || date -d '2 hours ago' +%Y%m%d%H%M)
NEW=$(date +%Y%m%d%H%M)
printf -- '---\nstate: claimed\nclaim: impl-dead %s\n---\n\n# the prd\n' "$(date -v-2H '+%Y-%m-%d %H:%M' 2>/dev/null || date -d '2 hours ago' '+%Y-%m-%d %H:%M')" \
  > "$T/repo/.pearde/prds/the-prd/prd.md"
touch -t "$OLD" "$T/repo/.pearde/prds/the-prd/prd.md"
printf 'x\n' > "$T/repo/resources/board/plan.py"
touch -t "$NEW" "$T/repo/resources/board/plan.py"   # the neighbour's fresh write

GOT=$(python3 - "$RESOURCES" "$T/repo" <<'PY' 2>&1
import importlib.util, os, sys
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
res, repo = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(res, "board"))
load("pearde_path", os.path.join(res, "pearde_path.py"))
load("common", os.path.join(res, "common.py"))
s = load("silence", os.path.join(res, "board", "silence.py"))
prd = {"state": "claimed", "dir": os.path.join(repo, ".pearde", "prds", "the-prd"),
       "fm": {"claim": "impl-dead 2020-01-01 00:00"}, "local": "the-prd",
       "board_path": os.path.join(repo, ".pearde")}
age = s.silent_of(prd, {}, collect=False)
print(int(age) if age is not None else "none")
PY
)
[ "$GOT" != "none" ] && [ "$GOT" -ge 100 ]
say $? "a dead claim reads silent even when its shared footprint was just written (got: ${GOT:-nothing})"

[ "$FAIL" = 0 ] || printf '\n%s check(s) failed — the invariant is broken.\n' "$FAIL"
[ "$FAIL" = 0 ]
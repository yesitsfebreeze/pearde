#!/usr/bin/env bash
# list-the-collects-the-repo-bug-orphaned — the harness for the landed module
# @resources/board/orphans.py. Five checks on live data, four on throwaway
# fixtures built under `mktemp -d` and removed at exit — nothing is written
# under any board. No daemon is started, so it is safe inside `collect`.
# The total is pinned: a dropped check fails the run rather than shrinking it.
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
CODE="$ROOT"
ORPH="$CODE/resources/board/orphans.py"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ok   $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; }
has() { if printf '%s\n' "$2" | grep -F -- "$3" >/dev/null; then ok "$1";
        else bad "$1 — want [$3]"; fi; }
eq()  { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 — want [$3] got [$2]"; fi; }
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
G="git -c user.name=fixture -c user.email=fixture@example.com -c commit.gpgsign=false -c init.defaultBranch=main"

prd() {   # <dir> <frontmatter body, one string> — a done PRD, nothing else
  mkdir -p "$1"
  { echo "---"; echo "state: done"; printf '%s\n' "$2"; echo "---"; echo
    echo "# fixture"; } > "$1/prd.md"
}

echo "# the live boards"

OUT=$(python3 "$ORPH" 2>&1); RC=$?
eq  "the scan runs over every registered board" "$RC" 0
has "and prints the count line" "$OUT" "done PRDs: "
has "bug residue is empty — nothing left for a person to re-commit" \
    "$OUT" "branch-only (bug residue): 0"

# --json is the row output; it must carry the rows the blocks are printed from
JRC=$(python3 "$ORPH" --json 2>/dev/null | python3 -c \
  'import json,sys; d=json.load(sys.stdin); print(int(bool(d["rows"]) and d["done"] >= d["with_footprints"]))')
eq  "--json carries the same rows, and done >= with_footprints" "$JRC" "1"

# the premise the per-branch check rests on: one store, two worktrees
eq  "the board is a worktree of the code repo's store" \
    "$(git -C "$BOARD" rev-parse --git-dir)" "$CODE/.git/worktrees/-pearde"

echo "# a misdirected commit, on a fixture"

# a nested-worktree board whose footprint path landed on the board branch only
( mkdir -p "$TMP/a" && cd "$TMP/a" && $G init -q . \
  && echo ".pearde/" > .gitignore && echo hi > README.md \
  && $G add .gitignore README.md && $G commit -qm base \
  && $G branch board && $G worktree add -q .pearde board \
  && mkdir -p "$TMP/a/.pearde/src" && echo "print(1)" > "$TMP/a/.pearde/src/thing.py" \
  && cd "$TMP/a/.pearde" && $G add -A \
  && $G commit -qm "board-branch commit of src/thing.py" ) >/dev/null 2>&1 \
  || bad "fixture A did not build"
prd "$TMP/a/.pearde/prds/done-one" "$(printf 'footprint:\n  - src/thing.py')"
A=$(python3 "$ORPH" "$TMP/a/.pearde" 2>&1); ARC=$?
has "the path landed on the board branch only is named branch-only" \
    "$A" "branch-only: src/thing.py"
eq  "and the run exits 1" "$ARC" 1

echo "# the shapes that must NOT read as the bug"

# the same two branches, the board a plain directory inside the repo
( mkdir -p "$TMP/b" && cd "$TMP/b" && $G init -q . \
  && echo ".pearde/" > .gitignore && echo hi > README.md \
  && $G add .gitignore README.md && $G commit -qm base \
  && $G checkout -q -b board && mkdir -p src && echo "print(1)" > src/thing.py \
  && $G add -f src/thing.py && $G commit -qm "board-branch commit of src/thing.py" \
  && $G checkout -q main ) >/dev/null 2>&1 || bad "fixture B did not build"
prd "$TMP/b/.pearde/prds/done-one" "$(printf 'footprint:\n  - src/thing.py')"
B=$(python3 "$ORPH" "$TMP/b/.pearde" 2>&1); BRC=$?
if printf '%s\n' "$B" | grep -q "branch-only:"; then
  bad "a board that is not its own worktree read as the bug"
else
  ok "a plain-directory board reports no branch-only — exit $BRC"
fi

# a `repo:` key checks the named repo's own branch — `trunk` here, so the
# board's own branch name would find nothing
( mkdir -p "$TMP/other/lib" && cd "$TMP/other" && $G init -q -b trunk . \
  && echo "x = 1" > lib/other.py && $G add -A \
  && $G commit -qm "other repo holds lib/other.py" \
  && mkdir -p "$TMP/c" && cd "$TMP/c" && $G init -q . \
  && echo ".pearde/" > .gitignore && $G add -A && $G commit -qm base ) \
  >/dev/null 2>&1 || bad "fixture C did not build"
prd "$TMP/c/.pearde/prds/with-repo" \
    "$(printf 'repo: %s\nfootprint:\n  - lib/other.py' "$TMP/other")"
prd "$TMP/c/.pearde/prds/no-repo" "$(printf 'footprint:\n  - lib/other.py')"
C=$(python3 "$ORPH" "$TMP/c/.pearde" 2>&1)
if printf '%s\n' "$C" | grep -q "with-repo"; then
  bad "the repo: key was ignored — the footprint was checked against the board's repo"
else
  ok "the repo: key sends the check at that repo's branch"
fi
has "the same footprint without the key is flagged" "$C" "no-repo"

# an undeclared flag is refused before any board is read
python3 "$ORPH" --nonesuch >/dev/null 2>&1; ERC=$?
eq  "an undeclared flag is refused" "$ERC" 2

echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$((PASS+FAIL))" -eq 11 ] || { echo "FAIL the harness dropped a check — 11 expected"; exit 1; }
[ "$FAIL" -eq 0 ]

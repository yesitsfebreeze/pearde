#!/usr/bin/env bash
# verify.sh — the migration probe: three fixture boards (tracked, master with
# members, fully untracked), migrate them, then gate each with the moved
# code's own scan. Fixtures live in a mktemp -d made at run time, removed at
# exit; nothing is written under any real board's prds/.
set -u
PRD=the-other-boards-move-once-and-the-script-goes
PLAN=/Users/feb/dev/infra/pearde/resources/board/plan.py
MIG="/Users/feb/dev/infra/pearde/.pearde/prds/$PRD/probe/migrate.py"
D=$(mktemp -d)
trap 'rm -rf "$D"' EXIT

PASS=0; FAIL=0
ok() { if [ "$1" = 0 ]; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); echo "FAIL: $2"; fi; }
has() { if grep -q -- "$3" "$2" 2>/dev/null; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); echo "FAIL: $1 — no <$3> in $2"; fi; }
same() { if [ "$2" = "$3" ]; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); echo "FAIL: $1 — got [$2] want [$3]"; fi; }

# ── fixture A: a single board, mitosys-shaped ────────────────────────────────
A="$D/board-a"; mkdir -p "$A/prds/alpha" "$A/prds/.state"
git -C "$A" init -q
printf -- '---\nstate: done\n---\n\n# alpha\n' > "$A/prds/alpha/prd.md"
echo OLDLOOSE > "$A/prds/.history.jsonl"
echo MSTATE  > "$A/prds/.state/history.jsonl"
echo p > "$A/prds/.plan.json"
printf 'x\n' > "$A/prds/.round.md"; echo v > "$A/prds/.view.html"
mkdir -p "$A/prds/memos" "$A/prds/knowledge" "$A/prds/gamma" "$A/prds/.claims"
echo m > "$A/prds/memos/m.md"; echo k > "$A/prds/knowledge/k.md"
printf -- '---\nstate: open\n---\n\n# g\n' > "$A/prds/gamma/prd.md"
printf -- '---\nstate: open\n---\n\n# root\n' > "$A/prds/prd.md"
printf '# settings\n' > "$A/prds/settings.md"; printf '# vision\n' > "$A/prds/vision.md"
printf 'prds/.history.jsonl\nprds/.plan.json\nprds/.view.html\nprds/.transitions.jsonl\nprds/.round.md\n' > "$A/.gitignore"
git -C "$A" add prds >/dev/null
git -C "$A" -c user.email=p@p -c user.name=p commit -qm init

# ── fixture B: an infra-shaped master — its member repo board-a sits INSIDE
#    the master repo (mitosys/ sits inside infra/), and the members row names
#    it by the old prds/ spot, inside the frontmatter block ─────────────────
B="$D/board-master"; mkdir -p "$B/prds/solo" "$B/board-a/prds/alpha"
git -C "$B" init -q
printf -- '---\nstate: open\n---\n\n# s\n' > "$B/prds/solo/prd.md"
printf -- '---\nname: master\nmembers:\n  - ../board-a/prds\n---\n\n# settings\n' > "$B/prds/settings.md"
git -C "$B" add prds >/dev/null; git -C "$B" -c user.email=p@p -c user.name=p commit -qm init
git -C "$B/board-a" init -q
printf -- '---\nstate: open\n---\n\n# alpha\n' > "$B/board-a/prds/alpha/prd.md"
git -C "$B/board-a" add prds >/dev/null
git -C "$B/board-a" -c user.email=p@p -c user.name=p commit -qm init

# ── fixture C: a fully untracked board, racer-shaped ────────────────────────
C="$D/board-c"; mkdir -p "$C/prds/one"
printf -- '---\nstate: open\n---\n\n# one\n' > "$C/prds/one/prd.md"
git -C "$C" init -q; echo '.DS_Store' > "$C/.gitignore"

# ── pre-state: the moved code refuses every un-migrated board ───────────────
python3 "$PLAN" scan "$A" >/dev/null 2>&1; RC=$?
[ "$RC" -ne 0 ]; ok $? "pre: the moved code refuses an un-migrated board (exit $RC)"

# ── migrate all three, one registry beside them ─────────────────────────────
printf '[\n "%s",\n "%s",\n "%s"\n]\n' "$A/prds" "$B/prds" "$D/nowhere/prds" > "$D/serve.json"
python3 "$MIG" "$B/board-a" "$A" "$B" "$C" --serve "$D/serve.json" > "$D/migrate.out" 2>&1
ok $? "migrate.py exits 0 over three boards"

# gate 1: the moved code scans each fixture board clean
python3 "$PLAN" scan "$A" > "$D/scan-a.txt" 2>&1; ok $? "gate: scan single board clean"
python3 "$PLAN" scan "$B" > "$D/scan-b.txt" 2>&1; ok $? "gate: scan master clean"

# PRDs under the names they already had, not prefixed, not dropped
GOT_A=$(python3 - "$A" <<'PY'
import sys
sys.path.insert(0, "/Users/feb/dev/infra/pearde/resources/board")
import plan
print(" ".join(sorted(plan.scan(sys.argv[1] + "/.pearde"))))
PY
)
same "names unchanged on A" "$GOT_A" "alpha gamma"
has "master reports member PRD under the member sigil" "$D/scan-b.txt" "@board-a/alpha"
has "master still reports its own PRD" "$D/scan-b.txt" "solo"
has "members row rewritten to the board dir" "$B/.pearde/settings.md" "board-a/.pearde"
has "member board scans under the sigil" "$D/scan-b.txt" "master of 1: board-a"

# layout invariants on A
[ -f "$A/.pearde/prds/alpha/prd.md" ]; ok $? "PRD dir inside .pearde/prds/"
[ -f "$A/.pearde/prds/gamma/prd.md" ]; ok $? "untracked PRD came across"
[ -d "$A/.pearde/memos" ]; ok $? "memos a sibling of prds/"
[ -f "$A/.pearde/settings.md" ] && [ -f "$A/.pearde/vision.md" ]; ok $? "settings and vision at board root"
[ ! -e "$A/.pearde/.history.jsonl" ]; ok $? "loose state dotfile gone from board root"
[ "$(cat "$A/.pearde/.state/history.jsonl" 2>/dev/null)" = "OLDLOOSE" ]; ok $? "state collision: the loose history stands, not the fresh .state one"
[ -f "$A/.pearde/.state/history.jsonl.from-state-dir" ]; ok $? "the .state-dir loser kept aside, not deleted"
[ -f "$A/.pearde/.state/round.md" ] && [ -f "$A/.pearde/.state/plan.json" ]; ok $? "five state dotfiles inside .state/, dot dropped"
[ -f "$A/.pearde/prds/prd.md" ]; ok $? "root prd.md inside prds/, ignored by the scan as before"
[ -f "$A/.pearde/wiki/k.md" ]; ok $? "knowledge/ became wiki/"
[ ! -e "$A/prds" ]; ok $? "no prds/ left at the board root"
[ ! -e "$A/.pearde/.pearde" ]; ok $? "no .pearde nested inside .pearde"

# tracked content moved as renames; untracked rode along and stays untracked
GIT_ST=$(git -C "$A" status --short)
echo "$GIT_ST" | grep -q "^R  prds/alpha/prd.md -> .pearde/prds/alpha/prd.md$"
ok $? "git mv staged the tracked rename"
# gamma and .claims ride along untracked only if untracked pre-move: in
# fixture A everything under prds/ is committed, so assert the renames cover
# the whole board and nothing is left as untracked ?? at the repo root
echo "$GIT_ST" | grep -qE "^\?\? .pearde"; [ $? -ne 0 ]; ok $? "no untracked .pearde left behind (tracked board moved as renames)"
echo "$GIT_ST" | grep -qE "^\?\? .*memos"; [ $? -ne 0 ]; ok $? "memos tracked from the start, no untracked noise"

# gitignore rewritten
has "gitignore rewritten for the new paths" "$A/.gitignore" ".pearde/.state/history.jsonl"
if grep -qE "^prds/\." "$A/.gitignore"; then FAIL=$((FAIL+1)); echo "FAIL: old prds/ state line left"; else PASS=$((PASS+1)); fi

# registry rows follow the move
NEWROW=$(python3 -c "import json;print(json.load(open('$D/serve.json'))[0])")
same "serve.json row repoints at .pearde" "$NEWROW" "$A/.pearde"

# a second run is a no-op
python3 "$MIG" "$A" --quiet > "$D/second.out" 2>&1
ok $? "re-run on a migrated board exits 0"
grep -q "already" "$D/second.out"; ok $? "re-run reports the board already migrated"

# fixture C: the untracked whole-board move never touches the index
C_ST=$(git -C "$C" status --short)
echo "$C_ST" | grep -q "?? prds/"; [ $? -ne 0 ]; ok $? "untracked board moved without touching its index"
[ -f "$C/.pearde/prds/one/prd.md" ]; ok $? "untracked board's PRD inside .pearde/prds/"

echo "verify: $((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]
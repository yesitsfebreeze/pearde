#!/usr/bin/env bash
# Verify harness for a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re.
#
# Run from anywhere: bash pearde/prds/a-lane-s-wiki-.../probe/verify.sh
# A worker building in a lane runs it as
#   PEARDE_ROOT=<lane> bash pearde/prds/a-lane-s-wiki-.../probe/verify.sh
# so the tree under test is the lane's and not the checkout's.
#
# What it proves: `knowledge.py` run from a LANE resolves the LIVE board's
# wiki, not a stub beside the lane's own copy of the script. Sections A-E
# run in a clean-room fixture built at run time under mktemp -d — never
# under the board, and never touching the live wiki. Section F reads the
# live board without writing to it. Section D is the negative control: the
# pre-fix resolver is reconstructed and must FAIL the same check, so no box
# here can be silently green.
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
cd "$ROOT" || exit 1

pass=0; fail=0
ok()  { pass=$((pass+1)); echo "  ok   $1"; }
bad() { fail=$((fail+1)); echo "  FAIL $1"; }

FIX="$(mktemp -d)"
trap 'rm -rf "$FIX"' EXIT
COPY="$FIX/repo"
LANE="$FIX/repo/pearde/.lanes/probe-lane"
mkdir -p "$COPY"

# ── the fixture: a code repo whose board is gitignored, and a lane worktree
# cut from it. This is the live layout in miniature — @resources/board/lanes.py
# `create` materialises a lane WITHOUT the board directory on purpose.
( cd "$ROOT" && git ls-files -z -- resources references \
    | rsync -a0 --files-from=- "$ROOT/" "$COPY/" ) 2>/dev/null
# the working tree, edits included — the harness measures what is on disk
for f in resources/knowledge.py resources/memos.py; do
  [ -f "$ROOT/$f" ] && cp "$ROOT/$f" "$COPY/$f"
done
[ -f "$COPY/resources/knowledge.py" ] \
  && ok "fixture carries resources/knowledge.py" \
  || { bad "fixture is missing resources/knowledge.py"; echo "verify.sh done, fail=$fail"; exit 1; }

printf '/pearde\n' > "$COPY/.gitignore"
# the seven undotted boards on this machine: the real directory and the
# `.pearde` compat symlink beside it — `board_named` reads through the link
# (`legacy-migrations-retire` spec04 dropped the undotted name as a resolver)
ln -s pearde "$COPY/.pearde"
mkdir -p "$COPY/pearde/prds/some-prd" "$COPY/pearde/wiki/sources"
cat > "$COPY/pearde/settings.md" <<'MD'
---
language: English
---

# fixture board
MD
cat > "$COPY/pearde/prds/some-prd/prd.md" <<'MD'
---
state: open
---

# some prd
MD
cat > "$COPY/pearde/wiki/sources/260902-fix1.md" <<'MD'
---
title: The lane fixture holds exactly one source note
date: 2026-09-02
type: source
tags: [fixture, lane, source]
provenance: "probe of a-lane-s-wiki-is-a-stub, 2026-09-02"
---

# The lane fixture holds exactly one source note

A lane worktree cut from this repo must read this note, not an empty stub.
MD

( cd "$COPY" && git init -q . && git add -A \
  && git -c user.email=probe@local -c user.name=probe commit -qm fixture ) 2>/dev/null
mkdir -p "$(dirname "$LANE")"
( cd "$COPY" && git worktree add -q --no-checkout "$LANE" -b lane/probe \
  && git -C "$LANE" sparse-checkout set --no-cone '/*' '!/pearde' \
  && git -C "$LANE" checkout -q ) 2>/dev/null
[ -f "$LANE/resources/knowledge.py" ] \
  && ok "lane worktree carries the script" \
  || { bad "lane worktree was not created"; echo "verify.sh done, fail=$fail"; exit 1; }
[ ! -d "$LANE/pearde/wiki" ] \
  && ok "lane starts with no wiki of its own" \
  || bad "lane already carries pearde/wiki before anything ran"

echo "== A: a query from the lane reads the live board's record =="
out=$( cd "$LANE" && python3 resources/knowledge.py query "lane fixture note" 2>&1 )
echo "$out" | head -1 | grep -q '1 notes on record' \
  && ok "query from the lane: $(echo "$out" | head -1)" \
  || bad "query from the lane did not report 1 notes on record — $(echo "$out" | head -1)"

echo "== B: the query made no stub beside the lane =="
[ ! -d "$LANE/pearde/wiki" ] \
  && ok "no <lane>/pearde/wiki was created" \
  || bad "the query created a stub wiki at <lane>/pearde/wiki"

echo "== C: a finding remembered from the lane lands on the live board =="
( cd "$LANE" && printf '%s\n' \
    "A lane's remember must write into the board it belongs to." \
  | python3 resources/knowledge.py remember "Remembered from a lane worktree" \
      --tags lane,probe \
      --provenance "probe of a-lane-s-wiki-is-a-stub, 2026-09-02" \
      >/dev/null 2>&1 )
n_board=$(ls "$COPY/pearde/wiki/sources" 2>/dev/null | grep -c '\.md$')
n_lane=$(ls "$LANE/pearde/wiki/sources" 2>/dev/null | grep -c '\.md$')
[ "$n_board" = "2" ] \
  && ok "the board's wiki holds 2 source notes after remember" \
  || bad "the board's wiki holds $n_board source note(s) after remember, want 2"
[ "$n_lane" = "0" ] \
  && ok "the lane's tree holds no source note of its own" \
  || bad "$n_lane source note(s) were written into the lane instead of the board"

echo "== D: negative control — the pre-fix resolver fails these same checks =="
OLD="$FIX/old"; mkdir -p "$OLD"
cp -R "$COPY/resources" "$OLD/resources"
python3 - "$OLD/resources/knowledge.py" <<'PY'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding="utf-8")
# the resolver as it stood before this PRD: the folder beside the script,
# and nothing else. Reconstructed here so the checks above can be shown to
# fail on it — a box that cannot fail is not a check.
s = re.sub(r"\n    board = memos\.board_above\([^\n]*\)\n    if board:\n"
           r"        return Path\(board\) / \"wiki\"\n", "\n", s, count=1)
p.write_text(s, encoding="utf-8")
PY
if grep -q 'memos.board_above' "$OLD/resources/knowledge.py"; then
  bad "could not reconstruct the pre-fix resolver — the control did not run"
else
  mkdir -p "$OLD/lane"
  cp -R "$OLD/resources" "$OLD/lane/resources"
  old_out=$( cd "$OLD/lane" && python3 resources/knowledge.py query "lane fixture note" 2>&1 | head -1 )
  echo "$old_out" | grep -q '0 notes on record' \
    && ok "pre-fix resolver reports 0 notes from a lane — the check can fail" \
    || bad "pre-fix resolver did not report 0 notes — the control proves nothing: $old_out"
  [ -d "$OLD/lane/.pearde/wiki" ] \
    && ok "pre-fix resolver created the stub the PRD names" \
    || bad "pre-fix resolver created no stub — the control proves nothing"
fi

echo "== E: no board above the cwd still falls back to the script's own repo =="
fb=$( cd "$FIX" && python3 "$COPY/resources/knowledge.py" query "lane fixture note" 2>&1 | head -1 )
echo "$fb" | grep -q 'notes on record' \
  && ok "a call from outside any board still answers: $fb" \
  || bad "a call from outside any board did not answer — $fb"

echo "== G: harvest recovers what the stubs already on disk are holding =="
# the stub as the defect left it: two notes a worker wrote into its lane,
# one of them a question the board has already queued. The shared graphify
# cache stands beside it as a symlink and must survive.
mkdir -p "$LANE/pearde/wiki/pending" "$LANE/pearde/wiki/sources" "$FIX/shared/cache"
ln -sfn "$FIX/shared" "$LANE/pearde/graphify"
cat > "$LANE/pearde/wiki/sources/260902-str1.md" <<'MD'
---
title: A finding a worker wrote inside its lane
date: 2026-09-02
type: source
tags: [lane, source]
---

# A finding a worker wrote inside its lane

It must survive the lane it was written in.
MD
cat > "$LANE/pearde/wiki/pending/260902-str2.md" <<'MD'
---
date: 2026-09-02
type: pending
status: pending
priority: med
tags: [pending]
question: "a question no one has asked yet"
---

# a question no one has asked yet
MD
cp "$LANE/pearde/wiki/pending/260902-str2.md" "$COPY/pearde/wiki/pending-seed.tmp"
mkdir -p "$COPY/pearde/wiki/pending"
sed 's/260902/260901/' "$COPY/pearde/wiki/pending-seed.tmp" > "$COPY/pearde/wiki/pending/260901-dup1.md"
rm -f "$COPY/pearde/wiki/pending-seed.tmp"

dry=$( cd "$LANE" && python3 resources/knowledge.py harvest --dry 2>&1 )
echo "$dry" | grep -q '^dry · ' \
  && ok "harvest --dry reports without moving: $(echo "$dry" | tail -1)" \
  || bad "harvest --dry printed nothing dry — $(echo "$dry" | tail -1)"
[ -f "$LANE/pearde/wiki/sources/260902-str1.md" ] \
  && ok "harvest --dry moved nothing" \
  || bad "harvest --dry moved a note"

run=$( cd "$LANE" && python3 resources/knowledge.py harvest 2>&1 )
echo "$run" | tail -1 | grep -q '1 note(s) recovered, 1 already on record' \
  && ok "harvest: $(echo "$run" | tail -1)" \
  || bad "harvest did not recover 1 and skip 1 — $(echo "$run" | tail -1)"
[ -f "$COPY/pearde/wiki/sources/260902-str1.md" ] \
  && ok "the stranded finding stands in the board's wiki" \
  || bad "the stranded finding did not reach the board's wiki"
[ ! -d "$LANE/pearde/wiki" ] \
  && ok "the emptied stub was removed from the lane" \
  || bad "the emptied stub still stands at <lane>/pearde/wiki"
[ -L "$LANE/pearde/graphify" ] && [ -d "$FIX/shared/cache" ] \
  && ok "the shared graphify cache beside it is untouched" \
  || bad "harvest reached through the shared graphify symlink"
again=$( cd "$LANE" && python3 resources/knowledge.py harvest 2>&1 | tail -1 )
echo "$again" | grep -q 'nothing stranded' \
  && ok "a second harvest finds nothing: $again" \
  || bad "harvest is not idempotent — $again"

echo "== F: the live board — the tree under test reads it, and writes nothing =="
live_disk=$(python3 - <<PY
import os
d = os.path.join("$BOARD", "wiki")
n = 0
for sub in ("sources", "conclusions"):
    p = os.path.join(d, sub)
    for r, dirs, files in os.walk(p):
        if os.path.basename(r) in (".absorbed", ".graphify"):
            dirs[:] = []
            continue
        n += sum(1 for f in files if f.endswith(".md") and not f.startswith("_"))
print(n)
PY
)
live_out=$( cd "$ROOT" && python3 resources/knowledge.py query "board" 2>&1 | head -1 )
live_n=$(echo "$live_out" | grep -oE '[0-9]+ notes on record' | grep -oE '^[0-9]+')
[ -n "$live_n" ] && [ "$live_n" = "$live_disk" ] \
  && ok "the tree under test reads $live_n note(s), matching the board on disk ($live_disk)" \
  || bad "the tree under test reads ${live_n:-none}, the board on disk holds $live_disk"
[ ! -d "$ROOT/pearde/wiki" ] || [ "$ROOT" = "$(dirname "$BOARD")" ] \
  && ok "no stub wiki under the tree under test" \
  || bad "a stub wiki stands at $ROOT/pearde/wiki"

echo
echo "$((pass+fail)) checks · $pass pass · $fail fail"
echo "verify.sh done, fail=$fail"
# the harness carries its own verdict — a run with a failed check must not
# exit 0, or the proof cannot fail
exit $(( fail != 0 ))

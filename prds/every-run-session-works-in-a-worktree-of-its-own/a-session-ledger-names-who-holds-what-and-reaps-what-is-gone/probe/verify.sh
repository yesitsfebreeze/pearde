#!/usr/bin/env bash
# probe — a session ledger names who holds what and reaps what is gone
#
# What this measures: `pearde session take/list/reap/owns` against a throwaway
# repo with a board in it. Every assertion below was run for real before it was
# written down; none is a prediction. Two stand-in sessions are real `sleep`
# processes we own, so `ps` answers about them exactly as it answers about a
# claude process, and `PEARDE_SESSION_PID` points the module at them.
#
#   bash prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh
#
# PEARDE_ROOT names the tree to measure; it defaults to the repo above the
# board, so a worker's lane measures the lane and not the checkout. The fixture
# is made at run time under $TMPDIR and never under the board — a directory
# holding a prd.md anywhere under the board is a PRD. The repo it is run from
# is never written to.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
RES="${RES:-$ROOT/resources}"
SESSION="$RES/board/session.py"
T="$(mktemp -d "${TMPDIR:-/tmp}/pearde-session-probe.XXXXXX")"
trap 'rm -rf "$T"' EXIT
pass=0
fail=0
ok()   { pass=$((pass+1)); echo "  ok   $*"; }
bad()  { echo "  FAIL $*"; fail=$((fail+1)); }
say()  { echo; echo "== $*"; }

echo "probe: a session ledger names who holds what and reaps what is gone — tree $ROOT"
[ -f "$SESSION" ] || { echo "  FAIL no $SESSION"; echo "PROBE RED — 1 failure(s)"; exit 1; }
cd "$T"
git init -q repo && cd repo
git config user.email p@p && git config user.name p
mkdir -p pearde/prds
printf -- '---\nname: probe\n---\n\n# probe board\n' > pearde/settings.md
echo 'pearde/' > .gitignore
echo one > a.txt && git add -A && git commit -qm init
BOARD="$T/repo/pearde"

# Two stand-in sessions: real processes we own, so `ps` answers about them
# exactly as it answers about a claude process.
sleep 600 & A=$!
sleep 600 & B=$!
sleep 600 & B2=$!

say "take — session A gets a worktree of its own"
PEARDE_SESSION_PID=$A python3 "$SESSION" take "$BOARD" || bad "take A exited nonzero"
[ -d "$BOARD/.sessions/s$A" ] && ok "worktree at .sessions/s$A" || bad "no worktree for A"
[ -f "$BOARD/.state/sessions.json" ] && ok "ledger written" || bad "no ledger"
git -C "$T/repo" branch --list "session/s$A" | grep -q . \
  && ok "branch session/s$A cut" || bad "no branch for A"
[ -e "$BOARD/.sessions/s$A/pearde" ] && bad "the board is inside the session tree" \
  || ok "the board is excluded from the session tree"

say "take is idempotent"
PEARDE_SESSION_PID=$A python3 "$SESSION" take "$BOARD" | grep -q holds \
  && ok "a second take holds, not takes" || bad "second take did not report holds"
[ "$(python3 -c 'import json,sys;print(len(json.load(open(sys.argv[1]))["sessions"]))' \
     "$BOARD/.state/sessions.json")" = 1 ] \
  && ok "one row, not two" || bad "the ledger grew a duplicate row"

say "take — session B gets a different worktree"
PEARDE_SESSION_PID=$B python3 "$SESSION" take "$BOARD" >/dev/null || bad "take B failed"
[ -d "$BOARD/.sessions/s$B" ] && ok "worktree at .sessions/s$B" || bad "no worktree for B"

say "owns — each session owns its own tree and not the other's"
PEARDE_SESSION_PID=$A python3 "$SESSION" owns "$BOARD/.sessions/s$A" --board "$BOARD" \
  >/dev/null && ok "A owns A" || bad "A does not own its own tree"
PEARDE_SESSION_PID=$A python3 "$SESSION" owns "$BOARD/.sessions/s$B" --board "$BOARD" \
  >/dev/null && bad "A claims to own B's tree" || ok "A does not own B"
PEARDE_SESSION_PID=$A python3 "$SESSION" owns "$T/repo" --board "$BOARD" \
  >/dev/null && bad "A claims to own the main checkout" \
  || ok "nobody owns the main checkout"

say "the work a dying session leaves"
echo "TRACKED EDIT" >> "$BOARD/.sessions/s$B/a.txt"
echo "untracked" > "$BOARD/.sessions/s$B/new.txt"
mkdir -p "$BOARD/.sessions/s$B/sub" && echo deep > "$BOARD/.sessions/s$B/sub/deep.txt"
git -C "$BOARD/.sessions/s$B" mv a.txt renamed.txt 2>/dev/null
echo "after the rename" >> "$BOARD/.sessions/s$B/renamed.txt"

say "reap — a LIVE session is never touched"
PEARDE_SESSION_PID=$A python3 "$SESSION" reap "$BOARD" --apply | tee "$T/reap1.txt"
[ -d "$BOARD/.sessions/s$B" ] && ok "B's tree survives while B is alive" \
  || bad "reaped a live session"
grep -q "keep   *s$B" "$T/reap1.txt" && ok "B reported kept" || bad "B not reported kept"

say "reap — a DEAD session's tree goes, its work first"
kill -9 $B 2>/dev/null; wait $B 2>/dev/null
PEARDE_SESSION_PID=$A python3 "$SESSION" reap "$BOARD" | tee "$T/dry.txt"
[ -d "$BOARD/.sessions/s$B" ] && ok "dry run removed nothing" || bad "dry run deleted a tree"
PEARDE_SESSION_PID=$A python3 "$SESSION" reap "$BOARD" --apply | tee "$T/reap2.txt"
[ -d "$BOARD/.sessions/s$B" ] && bad "dead session's tree still there" \
  || ok "dead session's tree removed"
[ -d "$BOARD/.sessions/s$A" ] && ok "the live session's tree is untouched" \
  || bad "the live session's tree was removed too"

say "the snapshot holds everything, untracked included"
SNAP="refs/pearde/reaped/s$B"
git -C "$T/repo" rev-parse --verify -q "$SNAP" >/dev/null \
  && ok "snapshot ref exists" || bad "no snapshot ref"
FILES=$(git -C "$T/repo" ls-tree -r --name-only "$SNAP" 2>/dev/null)
for f in renamed.txt new.txt sub/deep.txt; do
  echo "$FILES" | grep -qx "$f" && ok "snapshot holds $f" || bad "snapshot lost $f"
done
git -C "$T/repo" show "$SNAP:renamed.txt" 2>/dev/null | grep -q "after the rename" \
  && ok "the content of the edit is in the object store" \
  || bad "the snapshot holds the path but not the edit"
echo "$FILES" | grep -q "^pearde/" && bad "the board went into the snapshot" \
  || ok "the gitignored board stayed out of the snapshot"

say "the branch survives the reap"
git -C "$T/repo" branch --list "session/s$B" | grep -q . \
  && ok "session/s$B kept" || bad "the reap deleted the branch"

say "unknown liveness never reaps — a running pid whose start time is unrecorded"
sleep 600 & C=$!
mkdir -p "$BOARD/.sessions/sC"
python3 - "$BOARD" "$C" <<'PYEOF'
import json, sys
p = sys.argv[1] + "/.state/sessions.json"
d = json.load(open(p))
d["sessions"].append({"id": "sC", "pid": int(sys.argv[2]), "started": "",
                      "worktree": sys.argv[1] + "/.sessions/sC",
                      "branch": "session/sC"})
json.dump(d, open(p, "w"), indent=2)
PYEOF
PEARDE_SESSION_PID=$A python3 "$SESSION" reap "$BOARD" --apply | tee "$T/reap3.txt"
grep -Eq "keep +sC " "$T/reap3.txt" \
  && ok "a running pid with no recorded start time is kept, not reaped" \
  || bad "a row of unknown liveness was reaped"
[ -d "$BOARD/.sessions/sC" ] && ok "its directory survives" || bad "its directory was removed"

say "a reused pid reads as dead"
kill -9 $C 2>/dev/null; wait $C 2>/dev/null
python3 - "$BOARD" "$A" <<'PYEOF'
import json, sys
p = sys.argv[1] + "/.state/sessions.json"
d = json.load(open(p))
for r in d["sessions"]:
    if r["id"] == "sC":
        r["pid"] = int(sys.argv[2])                 # a pid that IS running…
        r["started"] = "Mon Jan  1 00:00:00 1990"   # …but not this process
json.dump(d, open(p, "w"), indent=2)
PYEOF
PEARDE_SESSION_PID=$B2 python3 "$SESSION" reap "$BOARD" | tee "$T/reap4.txt"
grep -Eq "reap +sC " "$T/reap4.txt" \
  && ok "a pid whose start time does not match is dead" \
  || bad "a reused pid was read as alive"

say "the running session's own tree is never reaped, whatever the ledger says"
# sC's row now points at $A's pid under a 1990 start time — dead by the test
# above. Run the reap AS $A: the guard that reads "this session" must fire
# before the liveness verdict is even consulted.
PEARDE_SESSION_PID=$A python3 "$SESSION" reap "$BOARD" --apply | tee "$T/reap5.txt"
grep -Eq "keep +sC +this session" "$T/reap5.txt" \
  && ok "a row this session holds is kept, dead ledger row and all" \
  || bad "the running session's own row was not kept"
[ -d "$BOARD/.sessions/sC" ] && ok "the running session's own tree survives" \
  || bad "reap --apply removed the running session's own worktree"

say "the snapshot leaves the worktree byte-identical"
echo "standing work" > "$BOARD/.sessions/s$A/untracked-before-snap.txt"
echo "edit" >> "$BOARD/.sessions/s$A/a.txt"
manifest() { (cd "$1" && find . -path ./.git -prune -o -type f -print \
  | sort | xargs shasum -a 256) ; }
manifest "$BOARD/.sessions/s$A" > "$T/tree-before.txt"
python3 - "$SESSION" "$T/repo" "$BOARD/.sessions/s$A" >"$T/snap-direct.txt" <<'PYEOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("sessionmod", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sha, files = m.snapshot(sys.argv[2], sys.argv[3], "sSNAP")
print(sha or "", len(files))
PYEOF
manifest "$BOARD/.sessions/s$A" > "$T/tree-after.txt"
cmp -s "$T/tree-before.txt" "$T/tree-after.txt" \
  && ok "the worktree is byte-identical across the snapshot" \
  || bad "the snapshot moved the worktree it snapshotted"
git -C "$T/repo" show "refs/pearde/reaped/sSNAP:untracked-before-snap.txt" 2>/dev/null \
  | grep -q "standing work" \
  && ok "and the snapshot it took holds the untracked file" \
  || bad "the snapshot did not capture the tree"

say "list"
PEARDE_SESSION_PID=$A python3 "$SESSION" list "$BOARD"

kill -9 $A $B2 2>/dev/null; wait $A $B2 2>/dev/null
echo
echo "$pass passed, $fail failed"
[ "$((pass+fail))" -ge 24 ] || { echo "PROBE RED — only $((pass+fail)) assertions ran, 24 expected"; exit 1; }
[ "$fail" -eq 0 ] && echo "PROBE GREEN" || echo "PROBE RED — $fail failure(s)"
exit "$fail"

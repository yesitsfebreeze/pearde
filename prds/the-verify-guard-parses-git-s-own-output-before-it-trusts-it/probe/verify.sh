#!/usr/bin/env bash
# the-verify-guard-parses-git-s-own-output-before-it-trusts-it — the harness.
#
# `collect_one` ran every spec's `## Verify and Proof` block, and the board's
# `gate`, as arbitrary `bash -e -o pipefail` straight in `repo` / `board_root`
# — the checkout every other session and every other PRD shares. `unland`
# exists only for a RED check, so a block that exits 0 having run
# `git reset --hard` or `rm -rf` takes whatever else was dirty there with it.
#
# Section A reproduces that on the collect at $PINNED — the last commit of
# `collect.py` with no guard in it (`git show` into scratch; that tree is
# never checked out). B drives `collect` end to end
# against this tree with the guard in it. C drives it on a board that is its
# OWN git repo, so `repo` and `board_root` differ — the shape this repo is
# in since the board moved to `pearde/`, and the one pass one's grouping got
# backwards. D runs the two unit probes. E drives a LANELESS board, where the
# PRD's uncommitted footprint IS the work under test and a block deleting it
# has nothing to recover it from — with the reproduction on spec01's collect
# beside it.
# One line per assertion, a count at the end.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] \
      && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
COLLECT="$ROOT/resources/board/collect.py"
EXAMPLE="$ROOT/resources/board/example"
# "Before" is the newest commit of `collect.py` that has no guard in it. It
# cannot be spelled `HEAD`: this harness is the verify block of the PRD that
# builds the guard, so `collect` runs it AFTER `land_lane` has merged the
# guard into the checkout's branch — at which point `HEAD` is "after" and the
# reproduction would quietly stop reproducing. Walking `collect.py`'s own
# history for the last commit without `def guarded_run` is right on both
# sides of that landing.
PINNED="${PINNED:-$(git -C "$ROOT" log --format=%H -- resources/board/collect.py \
  | while read -r c; do
      git -C "$ROOT" show "$c:resources/board/collect.py" 2>/dev/null \
        | grep -q '^def guarded_run' || { echo "$c"; break; }
    done)}"
PINNED="${PINNED:-HEAD}"
PASS=0; FAIL=0
export PEARDE_PORT=1
export PEARDE_ROOT="$ROOT"   # the D probes measure the tree this run measures
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@x \
       GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@x

ok()   { PASS=$((PASS+1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL $1"; [ -n "${2:-}" ] && echo "       got:  $2"; [ -n "${3:-}" ] && echo "       want: $3"; return 0; }
eq()   { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "$2" "$3"; fi; }
has()  { if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1" "$2" "contains: $3"; fi; }

TOP="$(mktemp -d)"; W="$(mktemp -d)"
trap 'for d in "$TOP"/*/; do git -C "$d" worktree prune >/dev/null 2>&1; git -C "$d/.pearde" worktree prune >/dev/null 2>&1; done; rm -rf "$TOP" "$W"' EXIT

# ── the pinned collect, in its own resources/ layout ─────────────────────────
OLD="$W/old/resources"; mkdir -p "$OLD/board"
for f in $(git -C "$ROOT" ls-tree -r --name-only "$PINNED" resources/ \
           | grep '^resources/\(board/\)\?[^/]*\.py$'); do
  git -C "$ROOT" show "$PINNED:$f" > "$OLD/${f#resources/}"
done

# ── pass one's collect: the guard as it landed at 6ea9c20 and was reverted ──
# The witness section F needs is "the same guard, before the parsing was
# fixed". It is pinned by CONTENT, not by a sha: the newest commit of
# `collect.py` that has `def guarded_run` in it and does NOT read git's output
# with `-z`. That is right on both sides of this PRD's landing, exactly as
# $PINNED is.
PASS1_SHA="${PASS1_SHA:-$(git -C "$ROOT" log --format=%H -- resources/board/collect.py \
  | while read -r c; do
      B="$(git -C "$ROOT" show "$c:resources/board/collect.py" 2>/dev/null)"
      printf '%s' "$B" | grep -q '^def guarded_run' || continue
      printf '%s' "$B" | grep -q '"--porcelain", "-z"' || { echo "$c"; break; }
    done)}"
PASS1="$W/pass1/resources"; mkdir -p "$PASS1/board"
if [ -n "$PASS1_SHA" ]; then
  for f in $(git -C "$ROOT" ls-tree -r --name-only "$PASS1_SHA" resources/ \
             | grep '^resources/\(board/\)\?[^/]*\.py$'); do
    git -C "$ROOT" show "$PASS1_SHA:$f" > "$PASS1/${f#resources/}"
  done
fi

# ── spec01's collect: this tree with spec02's snapshot taken back out ────────
# The reproduction section E needs is "the same collect one unit earlier", and
# that unit is uncommitted like the rest — so it is built from the shipped file
# rather than from a ref, and the build fails loudly if the two lines it
# reaches for are not there.
SPEC01="$W/spec01"; mkdir -p "$SPEC01"; cp -R "$ROOT/resources" "$SPEC01/resources"
python3 - "$SPEC01/resources/board/collect.py" <<'EOF'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
take, drop = "    snap = _snapshot(cwd, scoped)\n", "        _unerase(cwd, snap, out)\n"
assert take in t and drop in t, (
    "spec02's snapshot is not in collect.py in the shape this reproduction "
    "removes — the witness cannot be built")
open(p, "w", encoding="utf-8").write(t.replace(take, "    snap = {}\n").replace(drop, ""))
EOF

run()     { ( cd "$D" && PEARDE_AS=engineer python3 "$COLLECT" --board "$D/.pearde" "$@" ) 2>&1; }
run_s1()  { ( cd "$D" && PEARDE_AS=engineer python3 "$SPEC01/resources/board/collect.py" --board "$D/.pearde" "$@" ) 2>&1; }
run_old() { ( cd "$D" && PEARDE_AS=engineer python3 "$OLD/board/collect.py" --board "$D/.pearde" "$@" ) 2>&1; }
run_p1()  { ( cd "$D" && PEARDE_AS=engineer python3 "$PASS1/board/collect.py" --board "$D/.pearde" "$@" ) 2>&1; }
fm()      { grep -m1 "^$2:" "$D/.pearde/prds/$1/prd.md" | sed "s/^$2: *//"; }

# The destructive verify block. It exits 0, so nothing in `collect` treats it
# as a failure and `unland` never runs — the whole point. `git reset --hard`
# is the incident this PRD is filed from; `rm -rf other` is the same reach by
# a plainer route.
DESTRUCTIVE='git reset --hard HEAD >/dev/null 2>&1 || true
rm -rf other || true
true'
# The block for section C: it READS its own footprint. The lane merged an
# uncommitted change into it moments ago; a guard that parks the footprint
# makes this grep fail and the whole collect go red.
READS_ITS_FOOTPRINT='grep -q "def helper" src/util.py
rm -rf other || true
true'

# Section E's block. It exits 0 having deleted the very file the PRD is being
# collected for — the footprint the fence deliberately leaves reachable.
DELETES_ITS_FOOTPRINT='rm -f src/util.py
rm -rf other || true
true'

set_block() {   # set_block <spec path> <script>
  python3 - "$1" "$2" <<'EOF'
import re, sys
p, cmd = sys.argv[1], sys.argv[2]
t = open(p).read()
open(p, "w").write(re.sub(r"```sh\n.*?```", "```sh\n%s\n```" % cmd, t, flags=re.S))
EOF
}

# Section F's blocks. REVERTS is `git reset --hard HEAD` — the harness's own
# DESTRUCTIVE constant, and the incident in this PRD's title — on the laneless
# path, where the owned file stays PRESENT afterwards holding HEAD's bytes and
# pass one therefore saw nothing to put back. PEER_WRITES is a peer arriving
# inside the ~8s verify window with a brand new file. SPACED is the same wipe
# with a foreign path git would have quoted sitting in the checkout.
REVERTS='git reset --hard HEAD >/dev/null 2>&1 || true
true'
PEER_WRITES='printf "PEER WROTE THIS\n" > other/peer-new.txt
git reset --hard HEAD >/dev/null 2>&1 || true
true'

# ── the fixture ─────────────────────────────────────────────────────────────
# <name> <verify script> <own-repo: yes|no>. "yes" gives the board its own
# `git init`, so `repo_of` returns the enclosing checkout and `repo` and
# `board_root` are two different roots.
fixture() {
  D="$TOP/$1"; mkdir -p "$D/.pearde"; cp -R "$EXAMPLE/." "$D/.pearde/"
  mkdir -p "$D/.pearde/.state"
  set_block "$D/.pearde/prds/finished/specs/spec01.md" "$2"
  mkdir -p "$D/other"; echo "committed" > "$D/other/neighbour.txt"
  mkdir -p "$D/src"; echo "# empty" > "$D/src/util.py"
  find "$D" -type f -exec touch {} +
  if [ "$3" = yes ]; then
    printf '.pearde/\n' > "$D/.gitignore"
    ( cd "$D/.pearde" && git init -q -b pearde && git add -A \
      && git commit -q -m board )
  fi
  ( cd "$D" && git init -q -b main && git add -A && git commit -q -m fixture )
  if [ "${4:-lane}" = lane ]; then
    python3 - "$D" "$ROOT" <<'EOF'
import os, sys
d, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(root, "resources", "board"))
import lanes
lane = lanes.create(os.path.join(d, ".pearde"), d, "finished")
os.makedirs(os.path.join(lane, "src"), exist_ok=True)
open(os.path.join(lane, "src", "util.py"), "w").write(
    "def helper():\n    return 1\n")
EOF
  else
    # laneless — every claim taken before lanes, and every board outside a
    # git repo. The PRD's work is uncommitted in the checkout itself: there
    # is no lane to recover it from once a block deletes it.
    printf 'def helper():\n    return 1\n' > "$D/src/util.py"
  fi
  # the neighbour: uncommitted work no PRD on this board names
  echo "the neighbour's uncommitted work" > "$D/other/neighbour.txt"
}

# ═══ A. reproduced at $PINNED ════════════════════════════════════════════════
echo "A. reproduced at $PINNED: a GREEN verify block destroys the checkout"
fixture a1 "$DESTRUCTIVE" no
OUT="$(run_old finished)"; RC=$?
eq  "A1 the old collect exits 0 — the block never failed" "$RC" "0"
eq  "A1 ...and the PRD is done" "$(fm finished state)" "done"
eq  "A1 the neighbour's uncommitted work is GONE" \
    "$(cat "$D/other/neighbour.txt" 2>/dev/null || echo MISSING)" "MISSING"

# ═══ B. this tree: the block is fenced ══════════════════════════════════════
echo "B. the same block, guarded: the checkout it did not own is untouched"
fixture b1 "$DESTRUCTIVE" no
OUT="$(run finished)"; RC=$?
eq  "B1 collect exits 0" "$RC" "0"
eq  "B1 the PRD reaches done" "$(fm finished state)" "done"
eq  "B1 the neighbour's uncommitted work survives" \
    "$(cat "$D/other/neighbour.txt" 2>/dev/null || echo MISSING)" \
    "the neighbour's uncommitted work"
eq  "B1 no stash is left behind" "$( cd "$D" && git stash list )" ""

# ═══ C. repo != board_root ══════════════════════════════════════════════════
echo "C. the board is its own repo: the block still sees the change under test"
fixture c1 "$READS_ITS_FOOTPRINT" yes
OUT="$(run finished)"; RC=$?
eq  "C1 collect exits 0 — the footprint was NOT parked" "$RC" "0"
eq  "C1 the PRD reaches done" "$(fm finished state)" "done"
eq  "C1 the neighbour's uncommitted work survives" \
    "$(cat "$D/other/neighbour.txt" 2>/dev/null || echo MISSING)" \
    "the neighbour's uncommitted work"

echo "C. this repo's own roots: the footprint groups under the code repo"
# The bug pass one shipped, measured where it lives rather than in a fixture:
# on THIS board `repo_of` returns the checkout above `pearde/`, so `repo` and
# `board_root` are two paths, and a footprint rebased against `board_root`
# names `.pearde/resources/board/collect.py` — a file in neither root.
# `$BOARD` is passed in rather than re-derived through `find_board`: this
# harness's own walk already found the board, and `find_board` matches it by
# NAME, so the same directory is or is not a board depending on whether the
# path this script was invoked by went through the `.pearde` symlink.
OUT="$(cd "$ROOT" && python3 - "$ROOT" "$HERE" "$BOARD" <<'EOF'
import os, sys
root, here, board = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
sys.path.insert(0, os.path.join(root, "resources"))
sys.path.insert(0, os.path.join(root, "resources", "board"))
import plan as planlib, collect
br = planlib.repo_root(board)
prd = planlib.scan(board)[os.path.basename(os.path.dirname(here))]
repo = collect.repo_of(prd, board, br)
_, feet = planlib.spec_data(prd)
owned = collect.owned_by(prd, br, repo, feet)
print("same-root" if os.path.abspath(repo) == os.path.abspath(br) else "two-roots")
print(sorted(owned.get(os.path.abspath(repo), [])))
EOF
)"
eq  "C2 this board's repo and board root really are two paths" \
    "$(printf '%s' "$OUT" | sed -n 1p)" "two-roots"
eq  "C2 ...and the footprint groups under the code repo, unrebased" \
    "$(printf '%s' "$OUT" | sed -n 2p)" "['resources/board/collect.py']"

# ═══ E. the laneless path: the block deletes the work under test ════════════
echo "E. laneless: a green block deletes the PRD's own uncommitted footprint"
fixture e1 "$DELETES_ITS_FOOTPRINT" no laneless
OUT="$(run finished)"; RC=$?
eq  "E1 collect exits 0" "$RC" "0"
eq  "E1 the PRD reaches done" "$(fm finished state)" "done"
has "E1 collect names the path it put back, on its own line" "$OUT" \
    "put back: src/util.py"
eq  "E1 the uncommitted footprint is back on disk, not deleted" \
    "$(grep -c 'def helper' "$D/src/util.py" 2>/dev/null || echo MISSING)" "1"
eq  "E1 ...and it is the helper that got COMMITTED, not the deletion" \
    "$( cd "$D" && git show HEAD:src/util.py 2>/dev/null | grep -c 'def helper' \
        || echo MISSING )" "1"
eq  "E1 the neighbour's uncommitted work survives" \
    "$(cat "$D/other/neighbour.txt" 2>/dev/null || echo MISSING)" \
    "the neighbour's uncommitted work"

echo "E. the same fixture on spec01's collect: the deletion is what lands"
fixture e2 "$DELETES_ITS_FOOTPRINT" no laneless
OUT="$(run_s1 finished)"; RC=$?
eq  "E2 spec01's collect exits 0 — the block never failed" "$RC" "0"
eq  "E2 ...and the PRD is done" "$(fm finished state)" "done"
eq  "E2 the work under test is GONE from the checkout" \
    "$(cat "$D/src/util.py" 2>/dev/null || echo MISSING)" "MISSING"
eq  "E2 ...and the deletion is what got committed" \
    "$( cd "$D" && git show HEAD:src/util.py >/dev/null 2>&1 \
        && echo present || echo MISSING )" "MISSING"

# ═══ F. the parsing, and the peer, driven through `collect` ═════════════════
echo "F. laneless: a block that REVERTS the work under test to HEAD"
fixture f1 "$REVERTS" no laneless
OUT="$(run finished)"; RC=$?
eq  "F1 collect exits 0" "$RC" "0"
eq  "F1 the PRD reaches done" "$(fm finished state)" "done"
has "F1 collect names the path it put back" "$OUT" "put back: src/util.py"
eq  "F1 the work under test is on disk, not HEAD's bytes" \
    "$(grep -c 'def helper' "$D/src/util.py" 2>/dev/null || echo MISSING)" "1"
eq  "F1 ...and the helper is what got COMMITTED, not the revert" \
    "$( cd "$D" && git show HEAD:src/util.py 2>/dev/null | grep -c 'def helper' \
        || echo MISSING )" "1"

echo "F. the same fixture on pass one's collect ($PASS1_SHA): the revert lands"
fixture f2 "$REVERTS" no laneless
OUT="$(run_p1 finished)"; RC=$?
eq  "F2 pass one's collect exits 0 — the block never failed" "$RC" "0"
eq  "F2 ...and the PRD is done" "$(fm finished state)" "done"
eq  "F2 the work under test is reverted on disk" \
    "$(grep -c 'def helper' "$D/src/util.py" 2>/dev/null || :)" "0"
eq  "F2 ...and the revert is what got COMMITTED, silently" \
    "$( cd "$D" && git show HEAD:src/util.py 2>/dev/null | grep -c 'def helper' \
        || : )" "0"

echo "F. a peer's new file, written inside the verify window"
fixture f3 "$PEER_WRITES" no
OUT="$(run finished)"; RC=$?
eq  "F3 collect exits 0" "$RC" "0"
ASIDE="$(printf '%s' "$OUT" | sed -n 's/.*moved aside to \([^:]*\):.*/\1/p' | head -1)"
eq  "F3 the peer's file is not deleted — it is aside, with its bytes" \
    "$(cat "$ASIDE/other/peer-new.txt" 2>/dev/null || echo MISSING)" \
    "PEER WROTE THIS"
has "F3 collect says where it put it" "$OUT" "moved aside to"
eq  "F3 the neighbour's uncommitted work survives" \
    "$(cat "$D/other/neighbour.txt" 2>/dev/null || echo MISSING)" \
    "the neighbour's uncommitted work"

echo "F. the same block on pass one's collect: the peer's file is destroyed"
fixture f4 "$PEER_WRITES" no
OUT="$(run_p1 finished)"; RC=$?
eq  "F4 pass one's collect exits 0" "$RC" "0"
eq  "F4 the peer's new file is GONE" \
    "$(cat "$D/other/peer-new.txt" 2>/dev/null || echo MISSING)" "MISSING"
# pass one names every foreign row on one line whatever became of it, so the
# claim is read off that line rather than matched as a whole string
eq  "F4 ...while the output named it as put back" \
    "$(printf '%s' "$OUT" | grep -c 'put back:.*other/peer-new.txt' || :)" "1"

echo "F. a foreign path git would have quoted"
fixture f5 "$DESTRUCTIVE" no
printf 'a peer, with a space\n' > "$D/other/a peer file.txt"
OUT="$(run finished)"; RC=$?
eq  "F5 collect exits 0" "$RC" "0"
eq  "F5 the PRD reaches done" "$(fm finished state)" "done"
eq  "F5 the spaced foreign path survives, bytes intact" \
    "$(cat "$D/other/a peer file.txt" 2>/dev/null || echo MISSING)" \
    "a peer, with a space"
eq  "F5 no stash is left behind" "$( cd "$D" && git stash list )" ""

echo "F. the same fixture on pass one's collect: the quoting runs it unguarded"
fixture f6 "$DESTRUCTIVE" no
printf 'a peer, with a space\n' > "$D/other/a peer file.txt"
OUT="$(run_p1 finished)"; RC=$?
has "F6 pass one could not park it — it says so" "$OUT" \
    "could not park foreign dirt"
# `_heal` still runs when the park failed, so the file is back — holding
# HEAD's committed bytes. The neighbour's UNCOMMITTED work is what is gone.
eq  "F6 ...and the neighbour's uncommitted work went with the block" \
    "$(cat "$D/other/neighbour.txt" 2>/dev/null || echo MISSING)" "committed"

# ═══ D. the unit probes ═════════════════════════════════════════════════════
echo "D. the unit probes"
for p in probe_unit probe_roots; do
  OUT="$(python3 "$HERE/$p.py" 2>&1)"
  has "D $p" "$OUT" "ALL PASS"
done

echo
echo "$PASS passed, $FAIL failed"
# The exit status IS the verdict. Without this line the harness printed its
# tally and exited 0 whatever the tally said, so the `bash .../verify.sh` in
# both specs' `## Verify and Proof` was a check that could not go red.
exit $(( FAIL > 0 ))

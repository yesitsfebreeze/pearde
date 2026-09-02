#!/usr/bin/env bash
# a-master-need-is-the-union-of-its-members — the verify command of the memo
# of the same name. Run from the repo root:
#
#     bash resources/invariants/a-master-need-is-the-union-of-its-members.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: a master board's `need` is the union over `members:`, to any
# depth, its own tree counted as one more member; the floor lands on the sum;
# and a row credits the members the count came from. A plain board is
# untouched by all of that.
#
# Every count below is known by construction — three to seven git repos built
# in a `mktemp -d` and removed on exit — so an assertion is arithmetic rather
# than a reading of whichever trees this machine happens to hold. That
# matters: the fault this invariant exists for was a real board printing
# `rust 1` because it measured its own directory instead of the four Rust
# workspaces it plans over, and a check that reads the machine would have
# printed `rust 1` just as happily.
#
# It can fail, and the way to prove that is not to trust this comment:
#
#     D=$(mktemp -d); git archive HEAD | tar -x -C "$D"
#     RAMP="$D/resources/board/ramp.py" bash resources/invariants/<this>.sh
#
# `RAMP` points the whole run at another copy of the module. Against a
# `ramp.py` whose `scan_roots` returns only the board, the union, the floor,
# the credit, the depth, the cycle and the title union all go red and only the
# plain-board row stays green — which is the shape of a real regression.
#
# This machine ships no `timeout(1)` and no `gtimeout`, so a command that
# could hang is bounded by `perl -e 'alarm N; exec @ARGV'`. A `members:` list
# is a path list, so it can point in a circle; before the walk was keyed by
# realpath that circle was an infinite recursion, and an unbounded check would
# hang the harness sweep rather than fail it.
set -u
RAMP=${RAMP:-$(cd "$(dirname "$0")/../.." && pwd -P)/resources/board/ramp.py}
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }
say() { if [ "$1" = 0 ]; then okr "$2"; else no "$2"; fi; }

if [ ! -f "$RAMP" ]; then
  no "no ramp.py at $RAMP"
  exit 1
fi

T=$(mktemp -d) || exit 1
trap 'rm -rf "$T"' EXIT

# ── the fixtures ─────────────────────────────────────────────────────────────
# mkrepo <dir> <n .rs files> — a git repo with a board, its files staged so
# `git ls-files` sees them. Nothing is committed: `tracked()` reads the index.
mkrepo() {
  mkdir -p "$1/src" "$1/pearde/prds"
  i=0; while [ "$i" -lt "$2" ]; do : > "$1/src/f$i.rs"; i=$((i+1)); done
  printf 'x\n' > "$1/README.md"
  git -C "$1" init -q 2>/dev/null
  git -C "$1" add -A 2>/dev/null
  printf -- '---\nname: %s\n---\n' "$(basename "$1")" > "$1/pearde/settings.md"
}

# master <dir> <member board>… — rewrite one board's settings as a master
master() {
  d=$1; shift
  { printf -- '---\nname: %s\nmembers:\n' "$(basename "$(dirname "$d")")"
    for m in "$@"; do printf -- '  - %s\n' "$m"; done
    printf -- '---\n'; } > "$d/settings.md"
}

# prd <board> <slug> <title> — one PRD, for the title axis
prd() {
  mkdir -p "$1/prds/$2"
  printf -- '---\nstate: open\n---\n\n# %s\n' "$3" > "$1/prds/$2/prd.md"
}

# bounded <n> <cmd…> — this machine has no timeout(1)
bounded() { perl -e 'alarm shift; exec @ARGV' "$@"; }

need() { bounded 30 python3 "$RAMP" need --board "$1" 2>&1; }
row() { need "$1" | awk -v j="$2" '$1==j{print $2}'; }
why() { need "$1" | awk -v j="$2" '$1==j{$1="";$2="";print}'; }

mkrepo "$T/a" 30
mkrepo "$T/b" 12
mkrepo "$T/top" 1
master "$T/top/pearde" "$T/a/pearde" "$T/b/pearde"

# ── 1. a plain board is unchanged ────────────────────────────────────────────
# It counts its own tree, and its `why` is the marker list — not a member
# credit. This row must stay green through the regression the rest catch.
A=$(row "$T/a/pearde" rust)
[ "$A" = 30 ]; say $? "a plain board counts its own tree: 30 (got ${A:-none})"
AW=$(why "$T/a/pearde" rust)
case "$AW" in *'*.rs'*) r=0;; *) r=1;; esac
say $r "a plain board's why is the marker list, not a member credit (got${AW:-  none})"

# ── 2. the union is the sum, the master's own tree included ──────────────────
B=$(row "$T/b/pearde" rust)
[ "$B" = 12 ]; say $? "the second member counts its own 12 (got ${B:-none})"
O=$(row "$T/top/pearde" rust)
[ "$O" = 43 ]; say $? "the master sums 30+12+its own 1 = 43 (got ${O:-none})"

# ── 3. the row credits the members it came from, loudest first ───────────────
OW=$(why "$T/top/pearde" rust)
case "$OW" in *"a 30"*) r=0;; *) r=1;; esac
say $r "the master's row credits member a (got${OW:-  none})"
case "$OW" in *"top 1"*) r=0;; *) r=1;; esac
say $r "the master's row credits its own tree as one more member"
case "$OW" in *'*.rs'*) r=1;; *) r=0;; esac
say $r "the master's row is a member credit, not a marker list"
# loudest first: a (30) before b (12)
case "$OW" in *"a 30, b 12"*) r=0;; *) r=1;; esac
say $r "the master's credits are loudest member first"

# ── 4. the floor lands on the sum, never per member ──────────────────────────
# writing's floor is 25. Two members of 15 `.md` each fall short alone and
# clear it together — which is the whole reason the floor moved to the sum.
mkrepo "$T/c" 0; mkrepo "$T/d" 0; mkrepo "$T/mid" 0
i=0; while [ "$i" -lt 15 ]; do : > "$T/c/n$i.md"; : > "$T/d/n$i.md"; i=$((i+1)); done
git -C "$T/c" add -A 2>/dev/null; git -C "$T/d" add -A 2>/dev/null
master "$T/mid/pearde" "$T/c/pearde" "$T/d/pearde"
[ -z "$(row "$T/c/pearde" writing)" ]
say $? "one member's 15 .md stays under writing's floor on its own"
MID=$(row "$T/mid/pearde" writing)
{ [ -n "$MID" ] && [ "$MID" -ge 30 ]; }
say $? "the floor lands on the sum: ${MID:-none} over two members that each fall short"

# ── 5. a master under a master, to any depth ─────────────────────────────────
# The contract's own words are that a member is measured the way its own board
# would measure it — and a member that is itself a master measures a union. A
# one-level walk returns the middle repo's own tree and calls it the answer.
mkrepo "$T/root" 0
master "$T/root/pearde" "$T/top/pearde"
R=$(row "$T/root/pearde" rust)
[ "$R" = 43 ]; say $? "a master under a master reaches the grandchildren: 43 (got ${R:-none})"

# ── 6. a members: cycle terminates and counts each repo once ─────────────────
mkrepo "$T/x" 4; mkrepo "$T/y" 4
master "$T/x/pearde" "$T/y/pearde"
master "$T/y/pearde" "$T/x/pearde"
if out=$(bounded 20 python3 "$RAMP" need --board "$T/x/pearde" 2>&1); then
  n=$(printf '%s' "$out" | awk '$1=="rust"{print $2}')
  [ "$n" = 8 ]; say $? "a members cycle terminates and counts each repo once: 8 (got ${n:-none})"
else
  no "a members cycle terminates (it hit the alarm or died)"
fi

# ── 7. the title axis crosses the member boundary too ────────────────────────
# `board_words` is the public union accessor the contract names. Nothing
# inside `needs` calls it — `_measure` needs the per-board split — so this is
# the only thing that holds it to the contract.
prd "$T/a/pearde" only-a "a dockerfile for the thing"
prd "$T/top/pearde" only-top "the top board's own title"
W=$(bounded 30 python3 - "$RAMP" "$T/top/pearde" <<'PY' 2>&1
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ramp_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
words = " ".join(m.board_words(sys.argv[2]))
print("MEMBER" if "dockerfile" in words else "-",
      "OWN" if "top board" in words else "-")
PY
)
case "$W" in *MEMBER*) r=0;; *) r=1;; esac
say $r "board_words unions a member's PRD titles (got ${W:-none})"
case "$W" in *OWN*) r=0;; *) r=1;; esac
say $r "board_words keeps the master's own PRD titles in that union"

# ── 8. the fork a person reads names the member, not "the tree" ──────────────
# On a master the signal is a union, and the master's own repo is usually the
# smallest part of it. `The tree asks for rust` on a board whose own tree holds
# one .rs file points the reader at the wrong repo — the fault that filed this.
#
# The producer is guarded before any needle reads it. A module with no
# `ask_subject` prints a traceback, and a traceback does not contain the words
# `The tree` — so an unguarded "does not say The tree" needle reads green on
# the exact regression it exists to catch. Nothing below runs unless the
# producer exited 0 and printed the two lines it owes.
S=$(bounded 30 python3 - "$RAMP" "$T/top/pearde" "$T/a/pearde" <<'PY' 2>&1
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ramp_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for board in (sys.argv[2], sys.argv[3]):
    why = dict((j, w) for j, _, w in m.needs(board)).get("rust", "")
    print("SUBJECT", m.ask_subject("rust", why, m.contributors(board))[0])
PY
) && src=0 || src=$?
lines=$(printf '%s\n' "$S" | grep -c '^SUBJECT ' || true)
if [ "$src" != 0 ] || [ "$lines" != 2 ]; then
  no "the fork subject could not be read (exit $src): ${S:-no output}"
  no "a master's fork names the member that asked — not reached"
  no "a plain board's fork still says \"The tree\" — not reached"
else
  MS=$(printf '%s\n' "$S" | sed -n 's/^SUBJECT //p' | sed -n 1p)
  PS=$(printf '%s\n' "$S" | sed -n 's/^SUBJECT //p' | sed -n 2p)
  case "$MS" in *"a 30"*) r=0;; *) r=1;; esac
  say $r "a master's fork names the member that asked (got: ${MS:-none})"
  case "$MS" in *"The tree"*) r=1;; *) r=0;; esac
  say $r "a master's fork does not say \"The tree\""
  case "$PS" in "The tree asks for rust"*) r=0;; *) r=1;; esac
  say $r "a plain board's fork still says \"The tree\" (got: ${PS:-none})"
fi

[ "$FAIL" = 0 ] || printf '\n%s check(s) failed — the invariant is broken.\n' "$FAIL"
[ "$FAIL" = 0 ]

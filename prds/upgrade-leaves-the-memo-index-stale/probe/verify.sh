#!/usr/bin/env bash
# verify.sh — a board brought forward by `upgrade` is exactly as healthy as
# one made fresh by `init`.
#
# `cmd_upgrade` shared `plant_graph` with `cmd_init` and not `index_memos`,
# so the two paths diverged on one file: a board created by `init --example`
# landed with a current `memos/README.md`, and a board brought forward by
# `upgrade` kept whatever index it had — which, on every board made before
# `index_memos` existed, is no index at all. `memo check` calls that stale
# and doctor's `memos` row reports it broken. The command whose whole job is
# to bring a board current was the one command that left it red.
#
# The old shape is built rather than described: the fixture is the example
# board copied through `shutil.ignore_patterns("README.md")`, which is
# literally what `init --example` did before the index step existed. Section
# A sees it red before anything repairs it, so every box below is ticked
# against a predicate that was seen failing — memos/one-author-is-not-an-
# accepted-spec.md.
#
# Section C is the contract itself, driven: no doctor row's verdict differs
# between an upgraded board and a freshly `init`ed one.
#
# Section F strips the call back out of a COPY of init.py and watches the red
# come back, so the boxes above it are not checks that cannot fail. Section G
# proves the failure line names `upgrade`, not `init`.
#
# Everything runs on a copy of the repo built from `git ls-files` — tracked
# paths read out of the WORKING tree, so an uncommitted footprint edit is
# what is measured and an untracked drop of a neighbour's is not. Every
# fixture is under one `mktemp -d` removed at exit, and every command runs
# under a HOME holding no Obsidian config, so `register_vault` finds nothing
# to write to: a fixture board must never land in this machine's real vault
# list. Section H asserts both registers are byte-identical afterwards.
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
TOP="$(mktemp -d)"
COPY="$TOP/pearde"
NOOBS="$TOP/no-obsidian"
OBS="$HOME/Library/Application Support/obsidian/obsidian.json"
OBS_BEFORE="$( [ -f "$OBS" ] && cksum < "$OBS" )"
trap 'rm -rf "$TOP"' EXIT

PASS=0; FAIL=0; SKIP=0
ok()   { PASS=$((PASS+1)); echo "  ok    $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }
skip() { SKIP=$((SKIP+1)); echo "  skip  $1"; }
eq()   { [ "$2" = "$3" ] && ok "$1" || bad "$1 — got: $2 · want: $3"; }
has()  { printf '%s' "$2" | grep -qF -- "$3" && ok "$1" || bad "$1 — missing: $3"; }
lacks(){ printf '%s' "$2" | grep -qF -- "$3" && bad "$1 — present: $3" || ok "$1"; }

mkdir -p "$COPY" "$NOOBS"
( cd "$ROOT" && git ls-files -z | rsync -a0 --files-from=- "$ROOT/" "$COPY/" )
INIT="$COPY/resources/board/init.py"
DOC="$COPY/resources/doctor.sh"
MEMOS="$COPY/resources/memos.py"
EXPAGE="$COPY/resources/board/example/memos/README.md"
GREEN="pearde: every part this repo owns checks out."

# PEARDE_PORT=1 points every board command at a dead port, so a repair that
# registers whatever board it is handed cannot reach the live daemon.
export PEARDE_AS=engineer PEARDE_PORT=1
# every board command, under a home with no Obsidian config
R() { env -u XDG_CONFIG_HOME HOME="$NOOBS" "$@"; }

# a board shaped the way `init --example` left one before `index_memos`
# existed: the example copied through the directory-blind README glob, so it
# holds a memo and no index.
old_board() {
  local d="$1"; mkdir -p "$d"; ( cd "$d" && git init -q . )
  python3 - "$d" "$COPY" <<'PY'
import os, shutil, sys
d, copy = sys.argv[1], sys.argv[2]
shutil.copytree(os.path.join(copy, "resources", "board", "example"),
                os.path.join(d, ".pearde"), dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("README.md"))
PY
}
# a row's verdict FIELD, never a substring: `ok` is inside `broken`, so a
# `grep -F ok` over a row is a check that cannot fail.
verdict() { printf '%s\n' "$2" | sed -nE "s/^  $1 +(ok|broken|off) .*/\\1/p"; }
rows() { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +(ok|broken|off) .*/\1 \2/p'; }

echo "A. the old shape is red before anything touches it"
A="$TOP/a"; old_board "$A"
eq  "A the copy landed a memo" \
    "$(ls "$A/.pearde/memos" | grep -c '\.md$')" "1"
eq  "A ...and no index beside it" \
    "$( [ -e "$A/.pearde/memos/README.md" ] && echo yes || echo no )" "no"
MC="$(R python3 "$MEMOS" check "$A" 2>&1)"; MRC=$?
eq  "A memo check exits 1 on it" "$MRC" "1"
has "A ...calling the kind index stale" "$MC" "the kind index is stale"
DA="$(R bash "$DOC" "$A" 2>&1)"
eq  "A doctor's memos row reads broken" "$(verdict memos "$DA")" "broken"

echo "B. upgrade regenerates the index"
UOUT="$(R python3 "$INIT" upgrade "$A" 2>&1)"; URC=$?
eq  "B upgrade exits 0" "$URC" "0"
has "B ...and says it regenerated the page" "$UOUT" \
    "memos     regenerated memos/README.md, the index by kind"
eq  "B memos/README.md is on the board" \
    "$( [ -f "$A/.pearde/memos/README.md" ] && echo yes || echo no )" "yes"
MC2="$(R python3 "$MEMOS" check "$A" 2>&1)"; MRC2=$?
eq  "B memo check exits 0" "$MRC2" "0"
eq  "B ...and says nothing" "$(printf '%s' "$MC2" | wc -c | tr -d ' ')" "0"
has "B the page is the generated one, not a copied one" \
    "$(cat "$A/.pearde/memos/README.md")" \
    "<!-- Generated by \`memo index\` and rewritten by \`memo add\`;"
eq  "B ...and byte-identical to the example board's own page" \
    "$(cmp -s "$A/.pearde/memos/README.md" "$EXPAGE" && echo same || echo differs)" "same"

echo "C. an upgraded board is as healthy as a fresh one"
DU="$(R bash "$DOC" "$A" 2>&1)"; DURC=$?
eq  "C doctor exits 0 on the upgraded board" "$DURC" "0"
has "C ...and closes green" "$DU" "$GREEN"
eq  "C the memos row reads ok" "$(verdict memos "$DU")" "ok"
eq  "C the knowledge row reads ok" "$(verdict knowledge "$DU")" "ok"
FRESH="$TOP/fresh"; mkdir -p "$FRESH"; ( cd "$FRESH" && git init -q . )
FOUT="$(cd "$FRESH" && R python3 "$INIT" init --example 2>&1)"
has "C the fresh board's init regenerated its index too" "$FOUT" \
    "init: regenerated memos/README.md, the memo index by kind"
DF="$(R bash "$DOC" "$FRESH" 2>&1)"
RN=$(rows "$DF" | wc -l | tr -d ' ')
eq  "C the row reader read the whole report — 19 rows, not zero" "$RN" "19"
eq  "C no row reads broken on either board" \
    "$( { rows "$DU"; rows "$DF"; } | grep -c ' broken' || true)" "0"
# `vision` is the ONE row that still differs, and it is a second divergence of
# exactly this shape: `write_board` copies the vision template on `init` and
# `upgrade` never seeds it, so an upgraded board reads `vision off` where a
# fresh one reads `vision ok`. Doctor calls that off rather than broken — the
# board is healthy, not identical — and closing it is its own contract, named
# in the report. Excluding the row by name keeps this check true both before
# and after that gap closes; it never locks the gap in.
eq  "C every other row's verdict matches the fresh board's" \
    "$(diff <(rows "$DU" | grep -v '^vision ') \
            <(rows "$DF" | grep -v '^vision ') | grep -c '^[<>] ' || true)" "0"
eq  "C ...and the two boards' index pages are the same bytes" \
    "$(cmp -s "$A/.pearde/memos/README.md" "$FRESH/.pearde/memos/README.md" \
       && echo same || echo differs)" "same"

echo "D. a second upgrade is additive — it rewrites nothing"
SUM_BEFORE="$(cksum < "$A/.pearde/memos/README.md")"
U2="$(R python3 "$INIT" upgrade "$A" 2>&1)"; U2RC=$?
eq  "D upgrade exits 0 again" "$U2RC" "0"
has "D ...and the row says the index is already current" "$U2" \
    "memos     already current memos/README.md, the index by kind"
eq  "D ...and the page is the same bytes" \
    "$(cksum < "$A/.pearde/memos/README.md")" "$SUM_BEFORE"

echo "E. a board with no memo gets no page written over nothing"
E="$TOP/e"; mkdir -p "$E"; ( cd "$E" && git init -q . )
( cd "$E" && R python3 "$INIT" init >/dev/null 2>&1 )
EOUT="$(R python3 "$INIT" upgrade "$E" 2>&1)"; ERC=$?
eq  "E upgrade exits 0" "$ERC" "0"
has "E ...and says there is nothing to index" "$EOUT" \
    "memos     no memo on this board — nothing to index"
eq  "E memos/ holds no generated index" \
    "$( [ -e "$E/.pearde/memos/README.md" ] && echo yes || echo no )" "no"
has "E doctor calls the empty board green" "$(R bash "$DOC" "$E" 2>&1)" "$GREEN"

echo "F. the check can fail — take the call back out and the red returns"
cp "$INIT" "$TOP/init.py.bak"
python3 - "$INIT" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = '    indexed = index_memos(board, "upgrade")\n'
assert s.count(old) == 1, "the upgrade call site did not match"
open(p, "w").write(s.replace(old, "    indexed = None\n"))
PY
eq  "F the mutation reached the copy" \
    "$(grep -c 'indexed = index_memos(board, "upgrade")' "$INIT")" "0"
F="$TOP/f"; old_board "$F"
R python3 "$INIT" upgrade "$F" >/dev/null 2>&1
FRC=$(R python3 "$MEMOS" check "$F" >/dev/null 2>&1; echo $?)
eq  "F an upgrade without the call leaves memo check failing" "$FRC" "1"
eq  "F ...and doctor's memos row broken" \
    "$(verdict memos "$(R bash "$DOC" "$F" 2>&1)")" "broken"
cp "$TOP/init.py.bak" "$INIT"
eq  "F ...and the copy is restored" \
    "$(cmp -s "$TOP/init.py.bak" "$INIT" && echo same || echo differs)" "same"

echo "G. a failing index is said, and names upgrade rather than init"
cp "$MEMOS" "$TOP/memos.py.bak"
python3 - "$MEMOS" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = '    if cmd == "index":\n        print(write_index(board))\n        return 0\n'
assert s.count(old) == 1, "the index branch did not match"
open(p, "w").write(s.replace(
    old,
    '    if cmd == "index":\n'
    '        print("memos: cannot write the index", file=sys.stderr)\n'
    '        return 1\n'))
PY
eq  "G the failing-index mutation reached the copy" \
    "$(grep -c 'cannot write the index' "$MEMOS")" "1"
G="$TOP/g"; old_board "$G"
GOUT="$(R python3 "$INIT" upgrade "$G" 2>&1)"
has "G the failure is said, not swallowed" "$GOUT" \
    "upgrade: could not regenerate memos/README.md"
has "G ...naming what memos.py reported" "$GOUT" "cannot write the index"
lacks "G ...and it does not name the wrong command" "$GOUT" \
    "init: could not regenerate"
cp "$TOP/memos.py.bak" "$MEMOS"
eq  "G ...and the copy is restored" \
    "$(cmp -s "$TOP/memos.py.bak" "$MEMOS" && echo same || echo differs)" "same"

echo "H. nothing of this machine's was written to"
# What a stray fixture registration actually lands in is the daemon's own
# board list, and that is the only half of this obligation the run can move.
# No file on disk can carry it: `save_entry` returns early on an ephemeral
# path (`serve.py:385,402` — `EPHEMERAL` covers `/var/folders/`, where every
# fixture here lives), and `entry_path` is board-local, so this repo's
# `.pearde/.state/serve.json` is on no path the probe can reach. Comparing
# its bytes was `constant == the same constant` — a second check that could
# not fail, after the empty-string one it replaced. This one has been seen
# red: an `init` run without `PEARDE_PORT=1` during this unit's build reached
# 127.0.0.1:8443 and put a fixture board in that list.
# `PEARDE_PORT=1` is exported above and would make every probe answer "not
# running", so it is cleared for this one question.
SRV="$(env -u PEARDE_PORT PEARDE_AS=engineer \
       python3 "$ROOT/resources/board/serve.py" status 2>&1)"
if printf '%s' "$SRV" | grep -q 'not running'; then
  skip "the daemon is down, so it cannot be asked whether a fixture of this \
run reached its board list — down is not the same answer as clean"
else
  eq "H no fixture of this run reached the live daemon's board list" \
     "$(printf '%s' "$SRV" | grep -cF -- "$TOP")" "0"
fi
# The obligation this run owns, and it is race-free: not one path under this
# run's own temp root may appear in the machine's real Obsidian vault list.
# Every board command above runs under a HOME that holds no Obsidian config,
# so `register_vault` finds nothing to write to and returns (None, None).
# `grep -c` prints 0 AND exits 1 on no match, so a `|| echo 0` tail prints the
# zero twice and the comparison can never hold — the count is taken alone and
# the empty case (no register on this machine at all) is filled in after.
MINE="$(grep -cF -- "$TOP" "$OBS" 2>/dev/null)"; [ -n "$MINE" ] || MINE=0
eq  "H no fixture of this run reached Obsidian's vault list" "$MINE" "0"
# The whole file is a machine-wide resource every session's probes write to —
# a-check-decided-by-scheduling.md. Asserting it unchanged makes this harness's
# verdict depend on what else is running, so it stands down instead, and a
# stand-down reports skip and is never counted a pass.
OBS_NOW="$( [ -f "$OBS" ] && cksum < "$OBS" )"
if [ "$OBS_NOW" = "$OBS_BEFORE" ]; then
  ok "H ...and the vault list is byte-identical, so no session wrote it"
else
  skip "the vault list moved while this ran and holds no path of ours — \
another session's probe registered a fixture of its own; that harness set \
writes this machine's real Obsidian config and is a finding, not this run's"
fi

echo
echo "$((PASS+FAIL+SKIP)) checks · $PASS pass · $FAIL fail · $SKIP skip"
[ "$FAIL" = 0 ]

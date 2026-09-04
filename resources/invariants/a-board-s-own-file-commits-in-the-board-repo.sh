#!/usr/bin/env bash
# a-board-s-own-file-commits-in-the-board-repo — the verify command of the
# memo of the same name. Run from the repo root:
#
#     bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: a footprint path that resolves inside a board which is its
# own git repo is committed in the BOARD repo under its board-relative name.
# It is never staged in the code repo, which ignores the board and holds no
# such path, and it is never staged in the lane, which is cut without the
# board. A board that is not its own repo — the flat layout — is
# untouched by all of that and keeps the behaviour it always had.
#
# The fault this exists for: `pearde session` needed a row in the board's own
# `.gitignore`, so a spec's `footprint:` named `.pearde/.gitignore`. `collect`
# spells every footprint against the code repo, so `land_lane` ran `git add --
# .pearde/.gitignore` in a worktree that holds no such path. git answers
# `fatal: pathspec … did not match any files` and aborts the add WHOLE — so
# nothing was staged, nothing committed, the lane never merged, and every PRD
# gated behind it stalled. Past that, `sort_paths` filed the path under the
# code repo, whose `git status` never reports it, and the board's own edit was
# committed nowhere at all.
#
# Every repo below is built in a `mktemp -d` removed on exit — three git repos
# and a worktree — so each assertion is arithmetic about the tool rather than
# a reading of whichever trees this machine happens to hold. That matters
# here more than usual: this repo IS the nested layout, so a check that read
# the live tree would be measuring the very board it runs on.
#
# It can fail, and the way to prove that is not to trust this comment:
#
#     D=$(mktemp -d)
#     python3 -c 'import sys; t=open(sys.argv[1]).read();
#       k="def foot_root(p, board, board_root, repo):"; assert k in t;
#       open(sys.argv[2],"w").write(t.replace(k, k+"\n    return repo, p"))' \
#       resources/board/collect.py "$D/collect.py"
#     COLLECT="$D/collect.py" bash resources/invariants/<this>.sh
#
# `COLLECT` points the whole run at another copy of the module: the tree is
# copied to scratch and that file swapped in, because `collect.py` imports
# its siblings from its own directory and a lone copy cannot run. Against a
# `foot_root` that routes nothing, every nested row goes red and the flat row
# stays green — which is the shape of the real regression.
#
# `PEARDE_PORT` is pinned to a dead port for every run. `post_report` reads
# the machine's live daemon, and on a machine registering a master board it
# raises on `path: None` — so an unpinned run would crash collect for a reason
# that has nothing to do with this invariant.
set -u

ROOT=${PEARDE_ROOT:-$(cd "$(dirname "$0")/../.." && pwd -P)}
COLLECT=${COLLECT:-$ROOT/resources/board/collect.py}
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }
say() { if [ "$1" = 0 ]; then okr "$2"; else no "$2"; fi; }

if [ ! -f "$COLLECT" ]; then
  no "no collect.py at $COLLECT"
  exit 1
fi
if [ ! -d "$ROOT/resources/board" ]; then
  no "no resources/board under $ROOT"
  exit 1
fi

T=$(mktemp -d) || exit 1
trap 'rm -rf "$T"' EXIT

export PEARDE_PORT=1        # a dead port: no run below reaches the daemon
unset PEARDE_ROOT           # the fixtures are their own roots

# ── the module under test ────────────────────────────────────────────────────
# `collect.py` does `sys.path.insert(0, dirname(__file__))` and imports plan,
# edit, transitions, specs and lanes from beside itself, so a bare copy of the
# file cannot be run. The tree is copied and the file swapped in.
SRC="$T/src"
mkdir -p "$SRC"
cp -R "$ROOT/resources" "$SRC/resources" || exit 1
cp "$COLLECT" "$SRC/resources/board/collect.py" || exit 1
CO="$SRC/resources/board/collect.py"

# ── the fixtures ─────────────────────────────────────────────────────────────
SETTINGS='---
board: probe
language: English
max-complexity: 40
max-specs: 6
---

# settings
'

PRD='---
state: claimed
origin: requested
priority: 50
complexity: 4
blast-radius: low
claim: probe 2026-09-02 10:00
---

# p1 — a session ledger gets its row in the board own gitignore
'

# the nested spec names one file in EACH repo — that pair is the whole case
SPEC='---
complexity: 4
footprint:
  - resources/board/session.py
  - .pearde/.gitignore
---

# spec01 — the session tree is not dirt on the board branch

## Acceptance

- [x] `session.py` stands
- [x] the board ignore file names `.sessions/`

## Verify

```bash
true
```
'

# the board-spelled spec names the board file the way the BOARD spells it —
# `prds/p1/probe/verify.sh`, which is where every probe on a pearde board is
# told to live. Joined to the code repo that path names nothing, and a
# `foot_root` that only ever joins to the code repo refuses the whole collect
# before a single file is staged.
BS_SPEC='---
complexity: 4
footprint:
  - resources/board/session.py
  - prds/p1/probe/verify.sh
---

# spec01 — a probe is spelled the way the board spells it

## Acceptance

- [x] `session.py` stands
- [x] the probe stands where the board keeps it

## Verify

```bash
true
```
'

# the under PRD names its code repo: `repo: work`, resolved against the
# board's own root, is how a board says the code lives somewhere other than
# the directory above it. Here that somewhere is INSIDE the board, which is
# the shape a lane and a run-session worktree both have.
UNDER_PRD='---
state: claimed
origin: requested
priority: 50
complexity: 4
blast-radius: low
repo: work
claim: probe 2026-09-02 10:00
---

# p1 — a session ledger gets its row in the board own gitignore
'

# the under spec names one code file and nothing else. The layout is what
# makes it a case: the code repo is a checkout INSIDE the board directory,
# which is every lane and every run-session worktree this board cuts.
UNDER_SPEC='---
complexity: 4
footprint:
  - resources/board/session.py
---

# spec01 — a code checkout under the board is still its own repo

## Acceptance

- [x] `session.py` stands

## Verify

```bash
true
```
'

FLAT_SPEC='---
complexity: 4
footprint:
  - resources/board/session.py
---

# spec01 — the flat layout, where the board is not its own repo

## Acceptance

- [x] `session.py` stands

## Verify

```bash
true
```
'

gitq() { git -C "$1" -c user.email=probe@example.com -c user.name=probe \
         "${@:2}" >/dev/null 2>&1; }

# nested <dir> [<spec text>] — a code repo that IGNORES its board, and a board
# that is its own git repo tracking `.gitignore`. This repo's own layout. The spec defaults to `$SPEC`; the board-spelled section hands its
# own, so the two sections differ in the footprint and in nothing else.
nested() {
  code=$1/code; board=$code/.pearde
  mkdir -p "$code/resources/board" "$board/prds/p1/specs"
  gitq "$code" init -q -b main
  printf '/.pearde\n' > "$code/.gitignore"
  printf '# session\n' > "$code/resources/board/session.py"
  gitq "$code" add -A; gitq "$code" commit -qm base
  gitq "$board" init -q -b pearde
  printf '.lanes/\n.claims/\n.state/\n' > "$board/.gitignore"
  printf '%s' "$SETTINGS" > "$board/settings.md"
  printf '%s' "$PRD" > "$board/prds/p1/prd.md"
  printf '%s' "${2:-$SPEC}" > "$board/prds/p1/specs/spec01.md"
  gitq "$board" add -A; gitq "$board" commit -qm board
}

# under <dir> — the third layout, and the one the string prefix could never
# read: the board is its own git repo and the CODE repo is a checkout INSIDE
# it. Every lane this board cuts (`<board>/.lanes/<prd>`) and every run-session
# worktree has this shape. The board ignores the directory the code checkout
# sits in, exactly as it ignores `.lanes/`, so neither repo's status ever
# reports the other's files.
under() {
  board=$1/board; code=$board/work
  mkdir -p "$code/resources/board" "$board/prds/p1/specs"
  gitq "$board" init -q -b pearde
  printf '.lanes/\n.claims/\n.state/\nwork/\n' > "$board/.gitignore"
  printf '%s' "$SETTINGS" > "$board/settings.md"
  printf '%s' "$UNDER_PRD" > "$board/prds/p1/prd.md"
  printf '%s' "$UNDER_SPEC" > "$board/prds/p1/specs/spec01.md"
  gitq "$board" add -A; gitq "$board" commit -qm board
  gitq "$code" init -q -b main
  printf '# session\n' > "$code/resources/board/session.py"
  gitq "$code" add -A; gitq "$code" commit -qm base
}

# flat <dir> — the other layout: the board INSIDE the code repo and not a
# repo of its own, so `board_root` and `repo` are one root and nothing is ever
# rerouted. This row is the regression guard and must stay green.
flat() {
  code=$1/code; board=$code/.pearde
  mkdir -p "$code/resources/board" "$board/prds/p1/specs"
  gitq "$code" init -q -b main
  printf '.pearde/.lanes/\n' > "$code/.gitignore"
  printf '# session\n' > "$code/resources/board/session.py"
  printf '%s' "$SETTINGS" > "$board/settings.md"
  printf '%s' "$PRD" > "$board/prds/p1/prd.md"
  printf '%s' "$FLAT_SPEC" > "$board/prds/p1/specs/spec01.md"
  gitq "$code" add -A; gitq "$code" commit -qm base
}

# work <code> <board> — what the worker leaves standing: the code edit in its
# lane, and the board edit in the board, the only tree that holds that file.
work() {
  lane=$(python3 -c 'import sys
sys.path.insert(0, sys.argv[1])
import lanes
print(lanes.create(sys.argv[2], sys.argv[3], "p1"))' \
    "$SRC/resources/board" "$2" "$1" 2>&1) || { printf '%s\n' "$lane"; return 1; }
  printf '# session\ndef take():\n    pass\n' \
    > "$lane/resources/board/session.py"
  if [ -f "$2/.gitignore" ]; then
    printf '.sessions/\n' >> "$2/.gitignore"
  fi
  printf '%s' "$lane"
}

# code_work <code> <board> — the same as `work` without the board edit, for a
# section whose spec does not contract the board's `.gitignore`. Appending a
# line no footprint names would leave foreign dirt on the board and the run
# would be measuring the park, not the routing.
code_work() {
  lane=$(python3 -c 'import sys
sys.path.insert(0, sys.argv[1])
import lanes
print(lanes.create(sys.argv[2], sys.argv[3], "p1"))' \
    "$SRC/resources/board" "$2" "$1" 2>&1) || { printf '%s\n' "$lane"; return 1; }
  printf '# session\ndef take():\n    pass\n' \
    > "$lane/resources/board/session.py"
  printf '%s' "$lane"
}

run() { (cd "$1" && python3 "$CO" p1 --board "$2" --as engineer --trust 2>&1); }

# ── the nested layout: the case this invariant exists for ────────────────────
N=$T/n; mkdir -p "$N"
nested "$N"
NC=$N/code; NB=$NC/.pearde
LANE=$(work "$NC" "$NB") || no "the lane could not be cut: $LANE"
# The lane's `.pearde` is a symlink back at the board, so reading through it
# lands on the board's own `.gitignore` — which is the point: the lane holds
# no copy of the board's file. `-e` on the symlink path is therefore always
# true and says nothing; what must hold is that it resolves to the BOARD's
# `.gitignore` (a lane that held its own copy would resolve elsewhere).
if [ "$(realpath "$NB/.lanes/p1/.pearde/.gitignore" 2>/dev/null)" \
    = "$(realpath "$NB/.gitignore" 2>/dev/null)" ]; then r=0; else r=1; fi
say $r "the lane does not hold the board own file — it is cut without the board"

# both HEADs BEFORE the run: every log needle below reads only what
# collect itself committed. A `git log -3` over the whole history
# matches the fixture's own base commit and can never fail.
NB0=$(git -C "$NB" rev-parse HEAD)
NC0=$(git -C "$NC" rev-parse HEAD)
OUT=$(run "$NC" "$NB"); RC=$?
[ "$RC" = 0 ]
say $? "nested: collect exits 0 (got $RC)$(if [ "$RC" != 0 ]; then \
  printf ' — %s' "$(printf '%s' "$OUT" | tail -1)"; fi)"

case "$OUT" in *"did not match any files"*) r=1;; *) r=0;; esac
say $r "nested: no run hits \`fatal: pathspec … did not match any files\`"

LOG=$(git -C "$NB" log --name-only --pretty=format: "$NB0"..HEAD 2>/dev/null)
printf '%s\n' "$LOG" | grep -qx '\.gitignore'; r=$?
say $r "nested: a NEW commit in the BOARD repo holds .gitignore"

DIRT=$(git -C "$NB" status --porcelain -- .gitignore 2>/dev/null)
[ -z "$DIRT" ]
say $? "nested: the board working tree is clean after (got '${DIRT}')"

# the code repo committed the code file and never the board's — a
# `.pearde/.gitignore` in the code repo's history is the bug coming back by
# another door, since that repo ignores the whole directory.
CLOG=$(git -C "$NC" log --name-only --pretty=format: "$NC0"..HEAD 2>/dev/null)
printf '%s\n' "$CLOG" | grep -qx 'resources/board/session\.py'; r=$?
say $r "nested: the code repo commits the code file"
if printf '%s\n' "$CLOG" | grep -q '\.pearde/\.gitignore'; then r=1; else r=0; fi
say $r "nested: the code repo never stages the board own path"

case "$OUT" in *"own repo, not the lane"*) r=0;; *) r=1;; esac
say $r "nested: collect names the board-owned path it dropped from the lane add"

# ── the flat layout: nothing is rerouted, nothing moved ──────────────────────
F=$T/f; mkdir -p "$F"
flat "$F"
FC=$F/code; FB=$FC/.pearde
FLANE=$(work "$FC" "$FB") || no "the flat lane could not be cut: $FLANE"
FC0=$(git -C "$FC" rev-parse HEAD)
FOUT=$(run "$FC" "$FB"); FRC=$?
[ "$FRC" = 0 ]
say $? "flat: collect exits 0 (got $FRC)$(if [ "$FRC" != 0 ]; then \
  printf ' — %s' "$(printf '%s' "$FOUT" | tail -1)"; fi)"

FLOG=$(git -C "$FC" log --name-only --pretty=format: "$FC0"..HEAD 2>/dev/null)
printf '%s\n' "$FLOG" | grep -qx 'resources/board/session\.py'; r=$?
say $r "flat: the code file lands in the one repo there is"
case "$FOUT" in *"not the lane"*) r=1;; *) r=0;; esac
say $r "flat: nothing is rerouted — the two roots are one"

# ── board-spelled: the footprint written the way the board writes it ─────────
# The nested rows above only ever name the board file the CODE repo's way
# (`.pearde/.gitignore`). Every probe on a pearde board is told to live at
# `prds/<prd>/probe/`, which is the board's own spelling, and a `foot_root`
# that joins a footprint to the code repo and nowhere else cannot place it:
# the whole collect stops before a file is staged. That regression is silent
# in every row above it.
S=$T/bs; mkdir -p "$S"
nested "$S" "$BS_SPEC"
SC=$S/code; SB=$SC/.pearde
SLANE=$(code_work "$SC" "$SB") || no "board-spelled: the lane could not be cut: $SLANE"
mkdir -p "$SB/prds/p1/probe"
printf '#!/usr/bin/env bash\necho "1 check · 1 pass · 0 fail"\n' \
  > "$SB/prds/p1/probe/verify.sh"
SB0=$(git -C "$SB" rev-parse HEAD)
SC0=$(git -C "$SC" rev-parse HEAD)
SOUT=$(run "$SC" "$SB"); SRC_=$?
[ "$SRC_" = 0 ]
say $? "board-spelled: collect exits 0 (got $SRC_)$(if [ "$SRC_" != 0 ]; then \
  printf ' — %s' "$(printf '%s' "$SOUT" | tail -1)"; fi)"

case "$SOUT" in *"in no repo that holds it"*|*"matched no repo"*) r=1;; *) r=0;; esac
say $r "board-spelled: no run refuses the footprint for want of a repo"

SLOG=$(git -C "$SB" log --name-only --pretty=format: "$SB0"..HEAD 2>/dev/null)
printf '%s\n' "$SLOG" | grep -qx 'prds/p1/probe/verify\.sh'; r=$?
say $r "board-spelled: a NEW commit in the BOARD repo holds prds/p1/probe/verify.sh"

SCLOG=$(git -C "$SC" log --name-only --pretty=format: "$SC0"..HEAD 2>/dev/null)
if printf '%s\n' "$SCLOG" | grep -q 'probe/verify\.sh'; then r=1; else r=0; fi
say $r "board-spelled: the code repo never stages the board own probe path"

# ── under: the code repo is a checkout INSIDE the board ──────────────────────
# `full.startswith(board + os.sep)` reads "inside the board's path" as "the
# board's file". A code checkout nested under the board is inside that path
# and in neither the board's index nor its worktree, so every footprint of
# that repo was routed to the board, staged against an index that ignores it,
# and committed as nothing. No error and no refusal — which is why the two
# rows that matter here read the BOARD's commit rather than an exit code.
U=$T/u; mkdir -p "$U"
under "$U"
UB=$U/board; UC=$UB/work
ULANE=$(code_work "$UC" "$UB") || no "under: the lane could not be cut: $ULANE"
UB0=$(git -C "$UB" rev-parse HEAD)
UC0=$(git -C "$UC" rev-parse HEAD)
UOUT=$(run "$UC" "$UB"); URC=$?
[ "$URC" = 0 ]
say $? "under: collect exits 0 (got $URC)$(if [ "$URC" != 0 ]; then \
  printf ' — %s' "$(printf '%s' "$UOUT" | tail -1)"; fi)"

UCLOG=$(git -C "$UC" log --name-only --pretty=format: "$UC0"..HEAD 2>/dev/null)
printf '%s\n' "$UCLOG" | grep -qx 'resources/board/session\.py'; r=$?
say $r "under: the CODE repo commits resources/board/session.py"

# under ANY spelling: the board could carry it as `work/resources/…` or as
# `resources/…`, and both are the defect. A grep for the basename catches
# every spelling there is.
UBLOG=$(git -C "$UB" log --name-only --pretty=format: "$UB0"..HEAD 2>/dev/null)
if printf '%s\n' "$UBLOG" | grep -q 'session\.py'; then r=1; else r=0; fi
say $r "under: the BOARD repo commits the code path under no spelling"

UDIRT=$(git -C "$UC" status --porcelain -- resources/board/session.py 2>/dev/null)
[ -z "$UDIRT" ]
say $? "under: the code working tree is clean after (got '${UDIRT}')"

# ── nothing outside the temp dir was touched ─────────────────────────────────
case "$T" in /*) r=0;; *) r=1;; esac
say $r "every fixture is under one mktemp -d, removed on exit ($T)"

[ "$FAIL" = 0 ] || printf '\n%s check(s) failed — the invariant is broken.\n' "$FAIL"
[ "$FAIL" = 0 ]

#!/usr/bin/env bash
# collect-runs-the-invariants-and-red-refuses — the probe.
#
#     bash probe/verify.sh
#
# Exit 0 while the contract holds. Every fixture below is built in a
# `mktemp -d` removed on exit — two git repos and a board of its own — so
# each assertion is arithmetic about the tool, never a reading of whichever
# trees this machine happens to hold. Modelled on
# @resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh,
# which is the board's own template for exercising `collect` on a fixture.
#
# The contract, from the PRD:
#
#   `collect` runs every invariant before writing `done`. Any non-zero exit
#   refuses the collect, prints the failing invariant and its output, and
#   leaves state unchanged — the PRD stays exactly where it was.
#
# `COLLECT` points the whole run at another copy of the module: the tree is
# copied to scratch and that file swapped in, because `collect.py` imports
# its siblings from its own directory and a lone copy cannot run.
#
# `PEARDE_PORT` is pinned to a dead port for every run — `post_report` reads
# the machine's live daemon and would otherwise reach it.
set -u

ROOT=${PEARDE_ROOT:-$(cd "$(dirname "$0")/../../../../.." && pwd -P)}
COLLECT=${COLLECT:-$ROOT/resources/board/collect.py}
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }
say() { if [ "$1" = 0 ]; then okr "$2"; else no "$2"; fi; }

if [ ! -f "$COLLECT" ]; then no "no collect.py at $COLLECT"; exit 1; fi
if [ ! -d "$ROOT/resources/board" ]; then no "no resources/board under $ROOT"; exit 1; fi

T=$(mktemp -d) || exit 1
trap 'rm -rf "$T"' EXIT

export PEARDE_PORT=1
unset PEARDE_ROOT

SRC="$T/src"; mkdir -p "$SRC"
cp -R "$ROOT/resources" "$SRC/resources" || exit 1
cp "$COLLECT" "$SRC/resources/board/collect.py" || exit 1
CO="$SRC/resources/board/collect.py"

gitq() { git -C "$1" -c user.email=probe@example.com -c user.name=probe \
         "${@:2}" >/dev/null 2>&1; }

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

# p1 — the code file gets a function
'

SPEC='---
complexity: 4
footprint:
  - resources/board/session.py
---

# spec01 — the session tree stands

## Acceptance

- [x] `session.py` stands

## Verify

```bash
true
```
'

# the memo. `kind: invariant` with a `verify:` command is the whole
# registry — @.pearde/memos/invariants-are-testable-memos-and-the-kind-index-is-generated.md
# rejected a directory as the record and made the memo it.
memo() {  # memo <board> <slug> <command>
  mkdir -p "$1/memos"
  cat > "$1/memos/$2.md" <<EOF
---
memo: $2
kind: invariant
status: decided
subject: $2
date: 2026-09-02
verify: $3
---

# $2 — a rule the fixture board says binds
EOF
}

# flat <dir> — `.pearde/` inside the code repo, the layout most boards have.
flat() {
  code=$1/code; board=$code/.pearde
  mkdir -p "$code/resources/board" "$board/prds/p1/specs"
  gitq "$code" init -q -b main
  printf '.pearde/.lanes/\n.pearde/.claims/\n' > "$code/.gitignore"
  printf '# session\n' > "$code/resources/board/session.py"
  printf '%s' "$SETTINGS" > "$board/settings.md"
  printf '%s' "$PRD" > "$board/prds/p1/prd.md"
  printf '%s' "$SPEC" > "$board/prds/p1/specs/spec01.md"
  gitq "$code" add -A; gitq "$code" commit -qm base
}

# what the worker leaves standing, in the checkout — no lane, so the edit is
# uncommitted dirt in the footprint, which is the ordinary non-lane path.
work() { printf '# session\ndef take():\n    pass\n' > "$1/resources/board/session.py"; }

run() { (cd "$1" && python3 "$CO" p1 --board "$2" --as engineer 2>&1); }
state_of() { grep -m1 '^state:' "$1/prds/p1/prd.md" | sed 's/^state: *//'; }

# ── 1 · a red invariant refuses the collect ─────────────────────────────────
A=$T/a; mkdir -p "$A"; flat "$A"
AC=$A/code; AB=$AC/.pearde
printf '#!/usr/bin/env bash\necho "the rule the board says binds is broken"\nexit 1\n' \
  > "$AC/red.sh"
memo "$AB" "a-planted-rule" "bash red.sh"
work "$AC"
H0=$(git -C "$AC" rev-parse HEAD)
OUT=$(run "$AC" "$AB"); RC=$?

[ "$RC" = 1 ]; say $? "red: collect exits 1 (got $RC)"

# the slug alone is not the assertion: the board's memos dir is dirt in
# this fixture, so the unchanged collect prints the slug in its
# "inherited, not added" list. The refusal line is what is asserted.
case "$OUT" in *"invariant a-planted-rule: exit 1"*) r=0;; *) r=1;; esac
say $r "red: the output names the failing invariant and its exit"

case "$OUT" in *"the rule the board says binds is broken"*) r=0;; *) r=1;; esac
say $r "red: the output carries the script's own output"

# `## Done means` asks the output to name the script. A slug spells its
# script only where the memo author named the two alike, so the refusal
# line carries the `verify:` command verbatim — that is always what ran.
case "$OUT" in *"bash red.sh"*) r=0;; *) r=1;; esac
say $r "red: the output names the script the invariant runs"

[ "$(state_of "$AB")" = "claimed" ]
say $? "red: the PRD stays \`claimed\` (got \`$(state_of "$AB")\`)"

grep -q '^claim:' "$AB/prds/p1/prd.md"
say $? "red: the claim is still on the file"

grep -q '^actual:' "$AB/prds/p1/prd.md" && r=1 || r=0
say $r "red: no \`actual:\` was written"

[ "$(git -C "$AC" rev-parse HEAD)" = "$H0" ]
say $? "red: no commit was made"

# ── 2 · --fail does not file it as failed either ────────────────────────────
B=$T/b; mkdir -p "$B"; flat "$B"
BC=$B/code; BB=$BC/.pearde
printf '#!/usr/bin/env bash\nexit 1\n' > "$BC/red.sh"
memo "$BB" "a-planted-rule" "bash red.sh"
work "$BC"
(cd "$BC" && python3 "$CO" p1 --board "$BB" --as engineer --fail >/dev/null 2>&1)
[ "$(state_of "$BB")" = "claimed" ]
say $? "--fail: state unchanged, not \`failed\` (got \`$(state_of "$BB")\`)"

# ── 3 · --trust does not skip them ──────────────────────────────────────────
C=$T/c; mkdir -p "$C"; flat "$C"
CC=$C/code; CB=$CC/.pearde
printf '#!/usr/bin/env bash\nexit 1\n' > "$CC/red.sh"
memo "$CB" "a-planted-rule" "bash red.sh"
work "$CC"
OUT=$( (cd "$CC" && python3 "$CO" p1 --board "$CB" --as engineer --trust 2>&1) ); RC=$?
[ "$RC" = 1 ]; say $? "--trust: still refused (got $RC)"

# ── 4 · remove it and collect proceeds ──────────────────────────────────────
rm -f "$CB/memos/a-planted-rule.md"
OUT=$(run "$CC" "$CB"); RC=$?
[ "$RC" = 0 ]
say $? "green: with the invariant gone, collect exits 0 (got $RC)$(if [ "$RC" != 0 ]; then printf ' — %s' "$(printf '%s' "$OUT" | tail -3)"; fi)"
[ "$(state_of "$CB")" = "done" ]
say $? "green: the PRD reached \`done\` (got \`$(state_of "$CB")\`)"

# ── 5 · a green invariant does not refuse ───────────────────────────────────
D=$T/d; mkdir -p "$D"; flat "$D"
DC=$D/code; DB=$DC/.pearde
printf '#!/usr/bin/env bash\nexit 0\n' > "$DC/green.sh"
memo "$DB" "a-rule-that-holds" "bash green.sh"
work "$DC"
OUT=$(run "$DC" "$DB"); RC=$?
[ "$RC" = 0 ]
say $? "green invariant: collect exits 0 (got $RC)$(if [ "$RC" != 0 ]; then printf ' — %s' "$(printf '%s' "$OUT" | tail -3)"; fi)"

# ── 6 · a board with no memos at all is untouched ───────────────────────────
E=$T/e; mkdir -p "$E"; flat "$E"
EC=$E/code; EB=$EC/.pearde
work "$EC"
OUT=$(run "$EC" "$EB"); RC=$?
[ "$RC" = 0 ]
say $? "no memos: collect exits 0 (got $RC)$(if [ "$RC" != 0 ]; then printf ' — %s' "$(printf '%s' "$OUT" | tail -3)"; fi)"
case "$OUT" in *"no invariants on this board"*) r=1;; *) r=0;; esac
say $r "no memos: nothing about invariants is printed"

# ── 7 · an invariant memo with no verify: command is red, not a skip ────────
F=$T/f; mkdir -p "$F"; flat "$F"
FC=$F/code; FB=$FC/.pearde
mkdir -p "$FB/memos"
cat > "$FB/memos/a-rule-with-no-command.md" <<'EOF'
---
memo: a-rule-with-no-command
kind: invariant
status: decided
subject: a rule with no command
date: 2026-09-02
---

# a-rule-with-no-command
EOF
work "$FC"
OUT=$(run "$FC" "$FB"); RC=$?
[ "$RC" = 1 ]
say $? "no command: collect exits 1 (got $RC)"

# ── 8 · a superseded invariant no longer binds ──────────────────────────────
G=$T/g; mkdir -p "$G"; flat "$G"
GC=$G/code; GB=$GC/.pearde
mkdir -p "$GB/memos"
printf '#!/usr/bin/env bash\nexit 1\n' > "$GC/red.sh"
cat > "$GB/memos/a-retired-rule.md" <<'EOF'
---
memo: a-retired-rule
kind: invariant
status: superseded
subject: a retired rule
date: 2026-09-02
verify: bash red.sh
---

# a-retired-rule
EOF
work "$GC"
OUT=$(run "$GC" "$GB"); RC=$?
[ "$RC" = 0 ]
say $? "superseded: collect exits 0 (got $RC)$(if [ "$RC" != 0 ]; then printf ' — %s' "$(printf '%s' "$OUT" | tail -3)"; fi)"

# ── 9 · memos verify still prints one line per invariant ────────────────────
OUT=$( (cd "$DC" && python3 "$SRC/resources/memos.py" verify "$DB" 2>&1) )
case "$OUT" in *"a-rule-that-holds: holds"*) r=0;; *) r=1;; esac
say $r "memo verify: unchanged, prints \`<slug>: holds\`"

printf '\n%s\n' "$(if [ "$FAIL" = 0 ]; then echo OK; else echo "$FAIL FAIL"; fi)"
[ "$FAIL" = 0 ]

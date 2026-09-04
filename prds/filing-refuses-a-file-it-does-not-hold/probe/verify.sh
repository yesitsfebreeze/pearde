#!/usr/bin/env bash
# filing-refuses-a-file-it-does-not-hold — the probe's harness.
#
# `collect --also <path>` resolves a relative path against the board root
# first and the caller's cwd second, and a name both hold is the board's.
# A path neither holds refuses the whole call: nothing written, nothing
# committed, and the refusal names the path as given, both places it was
# looked for, and the board root.
# The rule is the user's, taken 2026-09-02 — *look in the notes first, then
# where you are standing* — and recorded in
# `.pearde/memos/also-resolves-against-the-board-first.md`.
#
# Builds a throwaway board under its own `git init` in a temp dir, one fresh
# copy per scenario. Never the real board. One line per assertion, a count at
# the end.
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
# overridable so the harness can be pointed at an older collect.py and shown
# to go red — a check that cannot fail proves nothing
COLLECT="${COLLECT:-$ROOT/resources/board/collect.py}"
PASS=0; FAIL=0
export PEARDE_PORT=1          # nothing listens there — the daemon is "down"
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@x \
       GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@x

ok()   { PASS=$((PASS+1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL $1"; [ -n "${2:-}" ] && echo "       got:  $2"; [ -n "${3:-}" ] && echo "       want: $3"; }
eq()   { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "$2" "$3"; fi; }
has()  { if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1" "$2" "contains: $3"; fi; }
lacks(){ if printf '%s' "$2" | grep -qF -- "$3"; then bad "$1" "$2" "without: $3"; else ok "$1"; fi; }

TOP="$(cd "$(mktemp -d)" && pwd -P)"     # -P: /var is a symlink on darwin
trap 'rm -rf "$TOP"' EXIT

# ── the fixture ──────────────────────────────────────────────────────────────
# $D is a repo, $D/.pearde is the board. `finished` and `second` are both
# claimed with their one box ticked and their code written — two collectable
# PRDs, so a refusal can be shown to stop the whole call and not just one PRD.
# `held` is the container's child, so `parent` closes as a container.
fixture() {
  D="$TOP/$1"; rm -rf "$D"; mkdir -p "$D"; ( cd "$D" && git init -q -b main )
  mkdir -p "$D/src" "$D/other" "$D/notes" "$D/docs" "$D/away" \
           "$D/.pearde/prds/finished/specs" "$D/.pearde/prds/second/specs" \
           "$D/.pearde/prds/parent/child/specs" "$D/.pearde/.state"
  echo 'true' > "$D/verify.sh"
  cat > "$D/.pearde/settings.md" <<'EOF'
---
name: fixture
language: English
workers: 1
pipeline: 1
---
EOF
  prd finished 50 src
  prd second   40 other
  cat > "$D/.pearde/prds/parent/prd.md" <<'EOF'
---
state: open
origin: requested
priority: 20
complexity: 3
---

# parent — a container, nothing of its own
EOF
  prd_at parent/child 10 notes
  ( cd "$D" && git add -A && git commit -q -m fixture )
  # a real file on the board, spelled from the board root, and untracked —
  # `--also` only ever adds a path the commit would otherwise carry
  echo 'atomic: x' > "$D/docs/x.md"
  # `$D/away` is a cwd inside the same repo that is *not* the board root:
  # `rider.md` is reachable only from there, `dup.md` from both roots under
  # the one spelling — the two halves of the resolution order.
  echo 'from where you stand' > "$D/away/rider.md"
  echo 'the board copy'       > "$D/dup.md"
  echo 'the cwd copy'         > "$D/away/dup.md"
  work finished src
  work second   other
  work parent/child notes
}
prd()    { prd_at "$1" "$2" "$3"; }
prd_at() {
  mkdir -p "$D/.pearde/prds/$1/specs"
  cat > "$D/.pearde/prds/$1/prd.md" <<EOF
---
state: claimed
origin: requested
claim: impl-1 2026-09-01 10:00
priority: $2
complexity: 5
workflow: implement-a-spec
footprint:
  - $3
---

# $(basename "$1") — writes one file under $3
EOF
  cat > "$D/.pearde/prds/$1/specs/spec01.md" <<EOF
---
complexity: 5
footprint:
  - $3
---

# spec01 — the file says hello

## Acceptance

- [ ] \`$3/lib.txt\` holds \`hello\`

## Verify and Proof

\`\`\`sh
bash verify.sh
\`\`\`
EOF
}
# the worker's run: the code, and the box ticked
work() {
  echo hello > "$D/$2/lib.txt"
  sed -i '' 's/- \[ \] /- [x] /' "$D/.pearde/prds/$1/specs/spec01.md"
}
# run from the board's own repo root, the ordinary case
run()  { ( cd "$D" && PEARDE_AS=engineer python3 "$COLLECT" --board "$D/.pearde" "$@" ) 2>&1; }
# run from somewhere else entirely — the caller's cwd must not be what an
# `--also` path resolves against
runat(){ local w="$1"; shift; ( cd "$w" && PEARDE_AS=engineer python3 "$COLLECT" --board "$D/.pearde" "$@" ) 2>&1; }
ncommits() { ( cd "$D" && git rev-list --count HEAD ); }
paths()    { ( cd "$D" && git show --name-only --format= "${1:-HEAD~1}" | sort | tr '\n' ' ' ); }
fm()       { grep -m1 "^$2:" "$D/.pearde/prds/$1/prd.md" | sed "s/^$2: *//"; }
NOTE="the fixture taught nothing"

# ── A. a path that exists nowhere ────────────────────────────────────────────
echo "A. --also names a file that does not exist"
fixture a
OUT="$(run finished --also notes/nope.md --also-note "$NOTE")"; RC=$?
eq   "A exit 1" "$RC" "1"
has  "A the refusal names the path" "$OUT" "notes/nope.md"
has  "A ...and the directory it was resolved against" "$OUT" "$D"
has  "A ...and says nothing was written" "$OUT" "nothing written"
eq   "A no commit was made" "$(ncommits)" "1"
eq   "A the PRD is untouched" "$(fm finished state)" "claimed"
eq   "A the claim still stands" "$(fm finished claim)" "impl-1 2026-09-01 10:00"
eq   "A no transition was recorded" \
     "$([ -f "$D/.pearde/.state/transitions.jsonl" ] && wc -l < "$D/.pearde/.state/transitions.jsonl" | tr -d ' ' || echo 0)" "0"
eq   "A the worker's tick is still dirty, not staged" \
     "$( cd "$D" && git diff --cached --name-only | wc -l | tr -d ' ' )" "0"

# ── B. the refusal is the whole call, not one PRD ────────────────────────────
echo "B. the whole call is refused"
fixture b
OUT="$(run finished second --also notes/nope.md --also-note "$NOTE")"; RC=$?
eq   "B exit 1" "$RC" "1"
eq   "B neither PRD was committed" "$(ncommits)" "1"
eq   "B finished untouched" "$(fm finished state)" "claimed"
eq   "B second untouched" "$(fm second state)" "claimed"
eq   "B the refusal is printed once, not per PRD" \
     "$(printf '%s\n' "$OUT" | grep -c 'notes/nope.md')" "1"
# and with no `--also` at all the same two PRDs do collect — the refusal is
# the flag's, not the fixture being uncollectable
fixture b2
OUT="$(run finished second)"; RC=$?
eq   "B control: without --also both collect" "$RC" "0"
eq   "B control: four commits land" "$(ncommits)" "5"

# ── C. a path that exists, spelled from the board root ───────────────────────
echo "C. resolution is against the board, the way --widen does it"
fixture c
OUT="$(run finished --also docs/x.md --also-note "$NOTE")"; RC=$?
eq   "C exit 0" "$RC" "0"
has  "C the file is on the commit" "$(paths)" "docs/x.md"
has  "C the note is in the message" \
     "$( cd "$D" && git log -1 --format=%B HEAD~1 )" "$NOTE"
# the same call from a cwd that is not the board — the path still resolves
fixture c2
OUT="$(runat "$TOP" finished --also docs/x.md --also-note "$NOTE")"; RC=$?
eq   "C from another cwd, exit 0" "$RC" "0"
has  "C from another cwd, the file is still on the commit" "$(paths)" "docs/x.md"

# ── D. a path that exists only relative to the caller's cwd ──────────────────
# the second half of the user's answer: *then where you are standing*. The
# board does not hold `rider.md`; the cwd does, so it resolves there and
# rides the commit.
echo "D. the caller's cwd is the second place a path is looked for"
fixture d
OUT="$(runat "$D/away" finished --also rider.md --also-note "$NOTE")"; RC=$?
eq   "D exit 0" "$RC" "0"
has  "D the cwd's file is on the commit" "$(paths)" "away/rider.md"
has  "D the note is in the message" \
     "$( cd "$D" && git log -1 --format=%B HEAD~1 )" "$NOTE"
eq   "D the PRD landed" "$(fm finished state)" "done"
# and when neither place holds it, the refusal names both
fixture d2
OUT="$(runat "$D/away" finished --also nope.md --also-note "$NOTE")"; RC=$?
eq   "D2 exit 1" "$RC" "1"
has  "D2 the refusal names the path as given" "$OUT" "nope.md"
has  "D2 ...the board place it was looked for" "$OUT" "$D/nope.md"
has  "D2 ...the cwd place it was looked for" "$OUT" "$D/away/nope.md"
has  "D2 ...and the board root" "$OUT" "board root $D"
eq   "D2 nothing committed" "$(ncommits)" "1"
eq   "D2 the PRD is untouched" "$(fm finished state)" "claimed"

# ── I. a name both places hold goes to the board's ───────────────────────────
# *look in the notes first*: `dup.md` is at the board root and in the cwd,
# and the board's copy is the one that rides. The cwd's copy stays untracked.
echo "I. precedence — the board's copy wins"
fixture i
OUT="$(runat "$D/away" finished --also dup.md --also-note "$NOTE")"; RC=$?
eq   "I exit 0" "$RC" "0"
has  "I the board's copy is on the commit" "$(paths)" "dup.md"
lacks "I the cwd's copy is not" "$(paths)" "away/dup.md"
eq   "I the commit carries the board's bytes" \
     "$( cd "$D" && git show HEAD~1:dup.md )" "the board copy"
eq   "I the cwd's copy is still untracked" \
     "$( cd "$D" && git status --porcelain -- away/dup.md )" "?? away/dup.md"

# ── E. an absolute path still behaves ────────────────────────────────────────
echo "E. absolute paths"
fixture e
OUT="$(run finished --also "$D/docs/x.md" --also-note "$NOTE")"; RC=$?
eq   "E an absolute path that exists: exit 0" "$RC" "0"
has  "E ...and is on the commit" "$(paths)" "docs/x.md"
fixture e2
OUT="$(run finished --also "$D/notes/gone.md" --also-note "$NOTE")"; RC=$?
eq   "E an absolute path that does not exist: exit 1" "$RC" "1"
has  "E ...named in the refusal" "$OUT" "$D/notes/gone.md"
eq   "E ...nothing committed" "$(ncommits)" "1"

# ── F. what exists is not refused ────────────────────────────────────────────
# the guard is existence, the same predicate the footprint loop eight lines
# above it already uses — `os.path.exists`, so a directory that is on the
# board goes through, and only what the board does not hold is refused.
echo "F. a directory that exists"
fixture f
OUT="$(run finished --also docs --also-note "$NOTE")"; RC=$?
eq   "F a directory on the board is not refused" "$RC" "0"
has  "F ...and its file rides the commit" "$(paths)" "docs/x.md"
fixture f2
OUT="$(run finished --also docs/sub --also-note "$NOTE")"; RC=$?
eq   "F a directory the board does not hold is refused" "$RC" "1"
eq   "F ...nothing committed" "$(ncommits)" "1"

# ── G. the container path is refused too ─────────────────────────────────────
echo "G. closing a container"
fixture g
OUT="$(run parent/child --also docs/x.md --also-note "$NOTE")"   # land the child
OUT="$(run parent --also notes/nope.md --also-note "$NOTE")"; RC=$?
eq   "G a container close with a bad --also exits 1" "$RC" "1"
has  "G ...naming the path" "$OUT" "notes/nope.md"
eq   "G ...and parent did not close" "$(fm parent state)" "open"

# ── H. the flag's own usage is unchanged ─────────────────────────────────────
echo "H. usage"
fixture h
OUT="$(run finished --also docs/x.md)"; RC=$?
eq   "H --also without --also-note is still usage, exit 2" "$RC" "2"
OUT="$(run finished --also)"; RC=$?
eq   "H --also without a path is still usage, exit 2" "$RC" "2"
eq   "H neither wrote a commit" "$(ncommits)" "1"

echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" -eq 0 ]

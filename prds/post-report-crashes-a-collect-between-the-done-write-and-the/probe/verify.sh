#!/usr/bin/env bash
# post-report-crashes-a-collect-between-the-done-write-and-the — the harness.
#
# `collect_one` writes the record — `actual:`, the claim gone, `state: done`
# — then calls `post_report`, then commits. `post_report` guards only
# `URLError, OSError, ValueError`. Anything else raises through it, and the
# board is left with a `prd.md` saying `done`, no claim, no `commit:`, and no
# commit anywhere: the PRD is finished on disk and unfinished in git, and the
# next scan reads a done PRD nothing landed.
#
# Four live-but-wrong daemons put a real exception outside that tuple on the
# wire (`stub_daemon.py`), and `inject.py` raises a bare one in the same place
# for the general case. Each is measured twice: on the code as it stood at
# $PINNED (`git show` into scratch — the tree is never checked out) and on the
# tree's `resources/board/collect.py`. One line per assertion, a count at the
# end.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
COLLECT="$ROOT/resources/board/collect.py"
EXAMPLE="$ROOT/resources/board/example"
PINNED="${PEARDE_PINNED:-58c92e6}"     # the last commit before this probe's fix
PASS=0; FAIL=0
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@x \
       GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@x

ok()   { PASS=$((PASS+1)); echo "  ok   $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL $1"; [ -n "${2:-}" ] && echo "       got:  $2"; [ -n "${3:-}" ] && echo "       want: $3"; }
eq()   { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "$2" "$3"; fi; }
ne()   { if [ "$2" != "$3" ]; then ok "$1"; else bad "$1" "$2" "anything but: $3"; fi; }
has()  { if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1" "$(printf '%s' "$2" | tail -4)" "contains: $3"; fi; }
lacks(){ if printf '%s' "$2" | grep -qF -- "$3"; then bad "$1" "$(printf '%s' "$2" | tail -4)" "without: $3"; else ok "$1"; fi; }

TOP="$(mktemp -d)"; W="$(mktemp -d)"
STUB_PID=""
cleanup() { [ -n "$STUB_PID" ] && kill "$STUB_PID" 2>/dev/null; rm -rf "$TOP" "$W"; return 0; }
trap cleanup EXIT

# ── the two collects: the pinned one, and the tree's ─────────────────────────
OLD="$W/old/resources"; mkdir -p "$OLD/board"
for f in $(git -C "$ROOT" ls-tree -r --name-only "$PINNED" resources/ | grep '\.py$'); do
  mkdir -p "$(dirname "$OLD/${f#resources/}")"
  git -C "$ROOT" show "$PINNED:$f" > "$OLD/${f#resources/}"
done
[ -f "$OLD/board/collect.py" ] || { echo "no pinned collect.py at $PINNED"; exit 2; }

run_old() { ( cd "$D" && PEARDE_AS=engineer PEARDE_PORT="$PORT" \
                python3 "$OLD/board/collect.py" --board "$D/.pearde" "$@" ) 2>&1; }
run()     { ( cd "$D" && PEARDE_AS=engineer PEARDE_PORT="$PORT" \
                python3 "$COLLECT" --board "$D/.pearde" "$@" ) 2>&1; }
run_inj() { local c="$1"; shift; ( cd "$D" && PEARDE_AS=engineer PEARDE_PORT=1 \
                python3 "$HERE/inject.py" "$c" RuntimeError -- \
                --board "$D/.pearde" "$@" ) 2>&1; }

ncommits() { ( cd "$D" && git rev-list --count HEAD ); }
fm()       { grep -m1 "^$2:" "$D/.pearde/prds/$1/prd.md" | sed "s/^$2: *//"; }
setline()  { python3 -c 'import sys; p,n,t=sys.argv[1],int(sys.argv[2]),sys.argv[3]; L=open(p).read().splitlines(True); L[n-1]=t+"\n"; open(p,"w").write("".join(L))' "$@"; }

# ── the stub daemon ──────────────────────────────────────────────────────────
stub() {   # stub <mode> — sets PORT, kills any previous one
  [ -n "$STUB_PID" ] && kill "$STUB_PID" 2>/dev/null
  local out="$W/port.$$"; : > "$out"
  python3 "$HERE/stub_daemon.py" "$1" "$D/.pearde" > "$out" 2>"$W/stub.err" &
  STUB_PID=$!
  disown "$STUB_PID" 2>/dev/null || true   # else bash prints `Terminated` at
  for _ in $(seq 1 100); do [ -s "$out" ] && break; sleep 0.05; done
  PORT="$(head -1 "$out")"
  [ -n "$PORT" ] || { echo "stub daemon did not start: $(cat "$W/stub.err")"; exit 2; }
}

# ── the fixture: the example board, its own repo, one PRD ready to collect ───
fixture() {
  D="$TOP/$1"; mkdir -p "$D/.pearde"; cp -R "$EXAMPLE/." "$D/.pearde/"
  mkdir -p "$D/.pearde/.state"
  python3 - "$D/.pearde/prds/finished/specs/spec01.md" <<'EOF'
import re, sys; p = sys.argv[1]; t = open(p).read()
open(p, "w").write(re.sub(r"```sh\n.*?```", "```sh\ntrue\n```", t, flags=re.S))
EOF
  find "$D" -type f -exec touch {} +
  ( cd "$D" && git init -q -b main && git add -A && git commit -q -m fixture )
  sed -i '' 's/^- \[ \] /- [x] /' "$D/.pearde/prds/finished/specs/spec01.md"
  mkdir -p "$D/src"; echo 'def helper(): return 1' > "$D/src/util.py"
  BEFORE="$(cat "$D/.pearde/prds/finished/prd.md")"
  N0="$(ncommits)"
}
# every child of `big` done — the container `collect big` closes
container_fixture() {
  fixture "$1"
  setline "$D/.pearde/prds/big/second/prd.md" 2 "state: done"
  python3 -c 'import sys; p=sys.argv[1]; t=open(p).read().replace("blast-radius: low","blast-radius: low\ncommit: none\nactual: 2h",1); open(p,"w").write(t)' "$D/.pearde/prds/big/second/prd.md"
  ( cd "$D" && git add -A && git commit -q -m children )
  BEFORE="$(cat "$D/.pearde/prds/big/prd.md")"
  N0="$(ncommits)"
}

torn() {   # torn <label> <prd> — the record says done and nothing landed
  eq   "$1 the record on disk says done" "$(fm "$2" state)" "done"
  eq   "$1 ...and no commit: on it"      "$(fm "$2" commit)" ""
  eq   "$1 ...and nothing was committed" "$(ncommits)" "$N0"
}
whole() {  # whole <label> <prd> — prd.md is byte-identical and nothing landed
  eq   "$1 the record was put back whole" "$(cat "$D/.pearde/prds/$2/prd.md")" "$BEFORE"
  eq   "$1 ...and nothing was committed"  "$(ncommits)" "$N0"
}

echo "R. reproduced at $PINNED: the four live-but-wrong daemons"
for MODE in garbage truncate list entry; do
  fixture "old-$MODE"; stub "$MODE"
  OUT="$(run_old finished)"; RC=$?
  ne   "R/$MODE the pinned collect does not exit 0" "$RC" "0"
  has  "R/$MODE ...it exits by traceback"           "$OUT" "Traceback (most recent call last)"
  has  "R/$MODE ...raised through post_report"      "$OUT" "post_report"
  torn "R/$MODE" finished
done

echo "R. reproduced at $PINNED: anything raised in the same place"
fixture old-inject
OUT="$(run_inj "$OLD/board/collect.py" finished)"; RC=$?
eq   "R/inject the injected error escapes the process" "$RC" "99"
has  "R/inject ...as a traceback"                      "$OUT" "injected — post_report blew up"
torn "R/inject" finished

echo "R. reproduced at $PINNED: the container path tears the same way"
container_fixture old-container; stub garbage
OUT="$(run_old big)"; RC=$?
ne   "R/container the pinned collect does not exit 0" "$RC" "0"
has  "R/container ...it exits by traceback"           "$OUT" "Traceback (most recent call last)"
eq   "R/container the record on disk says done"       "$(fm big state)" "done"
eq   "R/container ...and nothing was committed"       "$(ncommits)" "$N0"

echo "T. the tree: a wrong daemon is said, never raised"
for MODE in garbage truncate list entry; do
  fixture "new-$MODE"; stub "$MODE"
  OUT="$(run finished)"; RC=$?
  eq    "T/$MODE exit 0"                       "$RC" "0"
  lacks "T/$MODE ...no traceback"              "$OUT" "Traceback (most recent call last)"
  has   "T/$MODE ...the line says not posted"  "$OUT" "not posted"
  eq    "T/$MODE the record says done"         "$(fm finished state)" "done"
  ne    "T/$MODE ...with a commit: on it"      "$(fm finished commit)" ""
  eq    "T/$MODE ...two commits on top"        "$(ncommits)" "$((N0 + 2))"
done

echo "T. the tree: a daemon that answers is still posted to"
fixture new-ok; stub ok
OUT="$(run finished)"; RC=$?
eq   "T/ok exit 0"                    "$RC" "0"
has  "T/ok the line says report posted" "$OUT" "report posted"
eq   "T/ok ...two commits on top"     "$(ncommits)" "$((N0 + 2))"

echo "T. the tree: anything raised in the window puts the record back"
fixture new-inject
OUT="$(run_inj "$COLLECT" finished)"; RC=$?
eq    "T/inject exit 1 — a refusal, not a traceback" "$RC" "1"
lacks "T/inject ...nothing escaped"                  "$OUT" "Traceback (most recent call last)"
has   "T/inject ...it says the record was put back"  "$OUT" "put back"
has   "T/inject ...and names what raised"            "$OUT" "RuntimeError"
whole "T/inject" finished

echo "T. the tree: the container path is guarded the same way"
container_fixture new-container; stub garbage
OUT="$(run big)"; RC=$?
eq    "T/container exit 0"                      "$RC" "0"
lacks "T/container ...no traceback"             "$OUT" "Traceback (most recent call last)"
has   "T/container ...the line says not posted" "$OUT" "not posted"
eq    "T/container the record says done"        "$(fm big state)" "done"
eq    "T/container ...one commit on top"        "$(ncommits)" "$((N0 + 1))"

container_fixture new-container-inject
OUT="$(run_inj "$COLLECT" big)"; RC=$?
eq    "T/container-inject exit 1"           "$RC" "1"
lacks "T/container-inject ...nothing escaped" "$OUT" "Traceback (most recent call last)"
whole "T/container-inject" big

echo
echo "verify: $((PASS + FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" -eq 0 ]

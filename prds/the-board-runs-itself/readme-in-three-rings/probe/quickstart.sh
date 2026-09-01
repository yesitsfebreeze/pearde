#!/usr/bin/env bash
# quickstart.sh — the README's five lines, run end to end on a temp dir.
#
# Everything is isolated: the repo is copied (minus prds/ and .git), the
# skills dir is fresh, the board is a fresh git repo, and the daemon is the
# copy's serve.py on a spare port — its registry lives beside the copy, so
# the live daemon's state/serve.json is never touched (proven at the end).
# `pearde view` is run `--no-open`: the registration, not a window.
#
# Prints each command's output under a `$ ` line, so a reader can compare it
# with the README, then one count. Exit 1 on any failed check.
set -u
ROOT="$(cd "$(dirname "$0")/../../../../.." && pwd)"
TOP="$(mktemp -d)"
COPY="$TOP/pearde"; SKILLS="$TOP/skills"; PROJ="$TOP/proj"
REG="$ROOT/resources/board/state/serve.json"
REG_BEFORE="$( [ -f "$REG" ] && cksum < "$REG" )"
SPARE="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')"
export PEARDE_PORT="$SPARE"
cleanup() {
  PEARDE_PORT="$SPARE" python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1
  rm -rf "$TOP"
}
trap cleanup EXIT

PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); }
bad()  { FAIL=$((FAIL+1)); echo "FAIL: $1"; }
eq()   { [ "$2" = "$3" ] && ok || bad "$1 — got '$2', want '$3'"; }
has()  { printf '%s' "$2" | grep -qF -- "$3" && ok || bad "$1 — missing '$3'"; }
show() { echo; echo "\$ $1"; printf '%s\n' "$2"; }

# the copy: what a clone holds — every tracked file as it is in the working
# tree, no history, no gitignored file, and never the live daemon's state/
mkdir -p "$COPY" "$SKILLS" "$PROJ"
( cd "$ROOT" && git ls-files -z | rsync -a0 --files-from=- "$ROOT/" "$COPY/" )

# ── 1. install ───────────────────────────────────────────────────────────────
OUT="$(python3 "$COPY/resources/pearde.py" install --apply "$SKILLS" 2>&1)"; RC=$?
show "python3 <repo>/resources/pearde.py install --apply $SKILLS" "$OUT"
eq  "1 install exits 0" "$RC" "0"
has "1 install says built" "$OUT" "pearde install: built."
ALIAS="$(printf '%s\n' "$OUT" | sed -n "s/^ *alias pearde='\(.*\)'$/\1/p")"
has "1 install prints the alias" "$OUT" "alias pearde='python3 "
EXPORT="$(printf '%s\n' "$OUT" | sed -n 's/^ *\(export PEARDE_AS=engineer\)$/\1/p')"
eq  "1 install prints the export, bare" "$EXPORT" "export PEARDE_AS=engineer"
eq  "1 the skills dir holds fifteen folders — the set grew (knowledge, graph, update)" "$(find "$SKILLS" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" "15"
eq  "1 each folder holds the five links" "$(find "$SKILLS" -mindepth 2 -maxdepth 2 -type l | wc -l | tr -d ' ')" "75"
pearde() { $ALIAS "$@"; }
eval "$EXPORT"          # the second pasted line — who is working, as the README says

# ── 2. init --example ────────────────────────────────────────────────────────
cd "$PROJ" && git init -q .
OUT="$(pearde init --example 2>&1)"; RC=$?
show "pearde init --example" "$OUT"
eq  "2 init exits 0" "$RC" "0"
has "2 first line names the language" "$(printf '%s\n' "$OUT" | head -1)" "language English"
has "2 says it wrote the example board" "$OUT" "from the example board"
has "2 wrote .gitignore" "$OUT" ".gitignore +="
has "2 the daemon watches" "$OUT" "watching · http://127.0.0.1:$SPARE/board/example"
has "2 doctor closes green" "$OUT" "pearde: every part this repo owns checks out."
has "2 closes with the URL" "$OUT" "http://127.0.0.1:$SPARE/board/example"
has "2 closes with add" "$OUT" 'pearde add "<title>"'
eq  "2 settings.md exists" "$( [ -f .pearde/settings.md ] && echo yes )" "yes"
eq  "2 vision.md exists" "$( [ -f .pearde/vision.md ] && echo yes )" "yes"
eq  "2 six PRDs on disk" "$(find .pearde/prds -mindepth 2 -maxdepth 2 -name prd.md | wc -l | tr -d ' ')" "6"

# ── 3. add ───────────────────────────────────────────────────────────────────
OUT="$(pearde add "Ship the quickstart" 2>&1)"; RC=$?
show 'pearde add "Ship the quickstart"' "$OUT"
eq  "3 add exits 0" "$RC" "0"
has "3 the progress line names the PRD" "$OUT" "ship-the-quickstart"
has "3 ...and its state" "$OUT" "open"
eq  "3 ...as engineer, from the export — no --as on the line" "$([[ "$OUT" == *" · as engineer" ]]; echo $?)" "0"
eq  "3 prd.md exists" "$( [ -f .pearde/prds/ship-the-quickstart/prd.md ] && echo yes )" "yes"
eq  "3 state: open" "$(awk -F'[: #]+' '/^state:/{print $2; exit}' .pearde/prds/ship-the-quickstart/prd.md)" "open"

# ── 4. scan ──────────────────────────────────────────────────────────────────
OUT="$(pearde 2>&1)"; RC=$?
show "pearde" "$OUT"
eq  "4 scan exits 0" "$RC" "0"
has "4 the scan lists the new PRD" "$OUT" "ship-the-quickstart"
has "4 ...under ready" "$OUT" "ready"
has "4 ...and the finished one under collect" "$OUT" "collect"

# ── 5. view ──────────────────────────────────────────────────────────────────
OUT="$(pearde view --no-open 2>&1)"; RC=$?
show "pearde view" "$OUT"
eq  "5 view exits 0" "$RC" "0"
URL="$(printf '%s\n' "$OUT" | grep -o 'http://[^ ]*' | head -1)"
has "5 view prints the URL" "$URL" "http://127.0.0.1:$SPARE/board/example"
CODE="$(python3 -c 'import sys,urllib.request; print(urllib.request.urlopen(sys.argv[1], timeout=5).status)' "$URL" 2>&1)"
eq  "5 the page answers at the URL" "$CODE" "200"

# ── 6. the same board, read by a machine with no Obsidian ────────────────────
# The five lines above ran under this machine's own home, which happens to
# hold an Obsidian register — so `2 doctor closes green` proves the board is
# green *here*, and says nothing about the reader who has never installed
# Obsidian. That reader is the quickstart's whole audience. So doctor is run
# once more over the same fresh board under a home that holds no Obsidian
# config at all: an empty directory, with XDG_CONFIG_HOME scrubbed so the
# ambient one cannot leak the real register back in.
#
# What is asserted is that the vault row *answers* — `ok · Obsidian not
# installed here` — rather than reporting a missing register as a fault, that
# doctor still closes green, and that this is the only row that moved. The
# last one is the check that catches a home-dependent row elsewhere in the
# report: any other `ok|broken|off` verdict that differs between the two runs
# fails here, whatever it is.
NOOBS="$TOP/no-obsidian"; mkdir -p "$NOOBS"
rows() { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +(ok|broken|off) .*/\1 \2/p'; }
WITH="$(bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1)"
OUT="$(env -u XDG_CONFIG_HOME HOME="$NOOBS" bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1)"; RC=$?
show "HOME=<a home with no Obsidian config> pearde doctor" \
     "$(printf '%s\n' "$OUT" | grep -E '^  (vault|memos|knowledge) |^pearde:')"
eq  "6 doctor exits 0 under a home holding no Obsidian config" "$RC" "0"
has "6 ...and closes green there too" "$OUT" "pearde: every part this repo owns checks out."
# the verdict field, never a substring: `ok` is inside `broken`
eq  "6 the vault row answers rather than faulting" \
    "$(printf '%s\n' "$OUT" | sed -nE "s/^  vault +(ok|broken|off) .*/\\1/p")" "ok"
has "6 ...naming the machine, not the board" \
    "$(printf '%s\n' "$OUT" | grep -E '^  vault ')" "Obsidian not installed here"
# tripwire: an extractor reading nothing would make the diff below unfailable
eq  "6 the row reader read the whole report — 18 rows, not zero" "$(rows "$WITH" | wc -l | tr -d ' ')" "18"
eq  "6 no row's verdict moves under the scrubbed home — same names, same ok|broken|off" \
    "$(diff <(rows "$WITH") <(rows "$OUT") | grep -c '^[<>] ' || true)" "0"

# ── the live daemon was never touched ────────────────────────────────────────
python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1
eq  "the real registry is untouched" "$( [ -f "$REG" ] && cksum < "$REG" )" "$REG_BEFORE"

echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]

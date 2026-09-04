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
# What install promises is a relation — one folder per skill file, five links
# in each — and the relation is what is checked. The two numbers that used to
# stand here (`16`, `80`) were readings of whatever happened to be in the
# working tree at the moment of the run: a neighbouring session adding or
# removing one file under references/skills/ moved both, and the harness went
# red on code that was correct.
NSK="$(find "$COPY/references/skills" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
NDIR="$(find "$SKILLS" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
[ "$NSK" -gt 0 ] && ok || bad "1 the copy holds no skill file — nothing to build from"
eq  "1 the skills dir holds one folder per references/skills/*.md" "$NDIR" "$NSK"
eq  "1 each folder holds the five links" "$(find "$SKILLS" -mindepth 2 -maxdepth 2 -type l | wc -l | tr -d ' ')" "$((NDIR * 5))"
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
# `init` runs doctor and prints the report. What the README claims is that
# the board init just wrote is sound — not that the whole checkout is. Those
# are different sentences, and the second one is a reading of a working tree
# that several sessions write at once: on 2026-09-02 a neighbour's untracked
# resources/board/ramp.py, with no row in references/files.md yet, turned
# `index` broken and reddened this line while init was perfectly correct.
# So the control: the same doctor over a git repo with no board in it at
# all. A row broken there is broken for a reason that is not the board, it
# is named in a note, and it is not charged to `init`.
BARE="$TOP/bare"; mkdir -p "$BARE"; ( cd "$BARE" && git init -q . )
brokenrows() { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +broken .*/\1/p' | sort -u; }
NOBOARD="$(bash "$COPY/resources/doctor.sh" "$BARE" 2>&1)"
PRE="$(brokenrows "$NOBOARD")"
OWNED="$(comm -23 <(brokenrows "$OUT") <(printf '%s\n' "$PRE" | sed '/^$/d'))"
has "2 init ran doctor over the board it wrote" "$OUT" "pearde:"
[ -n "$PRE" ] && echo "  note: broken before any board existed, so not init's — $(printf '%s' "$PRE" | tr '\n' ' ')"
eq  "2 the board init wrote breaks no doctor row" \
    "$(printf '%s' "$OWNED" | tr '\n' ' ' | sed 's/ $//')" ""
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
# the board's URL, not the first URL on the page: when the service is not
# already up, `view` starts it and prints `serve: started on http://…:PORT`
# first, and whether the service happens to be up is machine state, not
# something the README claims
URL="$(printf '%s\n' "$OUT" | grep -o 'http://[^ ]*/board/[^ ]*' | head -1)"
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
#
# The last one used to be a plain diff of two whole doctor reports taken one
# after the other. A doctor report is not only a reading of this board: the
# `view` row curls a live service, `plugins` reads what is installed on the
# machine, `statusline` reads a working tree several sessions write. Any of
# those can move BETWEEN the two runs for a reason that has nothing to do
# with HOME, and the diff then failed on correct code — measured on
# 2026-09-02: stopping the service between the two runs, exactly what a
# neighbouring session's `serve.py stop` does, produced `< view ok / > view
# off` and a red.
#
# So the runs come in a control pair. Three reports: real HOME, scrubbed
# HOME, real HOME again. A row that moves between the two runs that share a
# HOME moved for a reason that is not HOME — it is the machine, it is named
# in a note, and it is not judged. A row that moves only across the HOME
# boundary is the finding, and before it is called a red it has to reproduce
# on a second pair. What is asserted is what the section is about: no row
# except the vault one reads the home.
NOOBS="$TOP/no-obsidian"; mkdir -p "$NOOBS"
rows()  { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +(ok|broken|off) .*/\1 \2/p'; }
docA()  { bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1; }
docB()  { env -u XDG_CONFIG_HOME HOME="$NOOBS" bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1; }
moved() { diff <(rows "$1") <(rows "$2") | sed -nE 's/^[<>] ([a-z]+) .*/\1/p' | sort -u; }

WITH="$(docA)"
OUT="$(docB)"; RC=$?
AGAIN="$(docA)"
show "HOME=<a home with no Obsidian config> pearde doctor" \
     "$(printf '%s\n' "$OUT" | grep -E '^  (vault|memos|knowledge) |^pearde:')"
# the same control as section 2: rows already broken with no board in the
# picture are the checkout's, not the home's and not init's
eq  "6 the report is complete under a home holding no Obsidian config" \
    "$(printf '%s\n' "$OUT" | grep -c '^pearde:')" "1"
eq  "6 ...and the scrubbed home breaks no row the checkout had not already broken" \
    "$(comm -23 <(brokenrows "$OUT") <(printf '%s\n' "$PRE" | sed '/^$/d') | tr '\n' ' ' | sed 's/ $//')" ""
# the verdict field, never a substring: `ok` is inside `broken`
eq  "6 the vault row answers rather than faulting" \
    "$(printf '%s\n' "$OUT" | sed -nE "s/^  vault +(ok|broken|off) .*/\\1/p")" "ok"
has "6 ...naming the machine, not the board" \
    "$(printf '%s\n' "$OUT" | grep -E '^  vault ')" "Obsidian not installed here"
# tripwire: an extractor reading nothing would make the comparison unfailable.
# A floor and two named rows, never a pinned total — doctor gains rows, and a
# new row is not a fault in the README.
NROWS="$(rows "$WITH" | wc -l | tr -d ' ')"
[ "$NROWS" -ge 15 ] && ok || bad "6 the row reader found $NROWS rows, under the floor of 15"
has "6 ...including the row under test" "$(rows "$WITH")" "vault "
has "6 ...and one that has nothing to do with the home" "$(rows "$WITH")" "board "
VOLATILE="$(moved "$WITH" "$AGAIN")"
HOMEDEP="$(comm -23 <(moved "$WITH" "$OUT") <(printf '%s\n' "$VOLATILE" | sed '/^$/d'))"
if [ -n "$HOMEDEP" ]; then
  # a red has to reproduce on a second pair before it is called one
  W2="$(docA)"; O2="$(docB)"
  HOMEDEP="$(comm -12 <(printf '%s\n' "$HOMEDEP") <(moved "$W2" "$O2"))"
fi
[ -n "$VOLATILE" ] && echo "  note: moved with the home held constant, so not judged — $(printf '%s' "$VOLATILE" | tr '\n' ' ')"
eq  "6 no row but vault reads the home — twice measured, against a control pair" \
    "$(printf '%s\n' "$HOMEDEP" | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')" ""

# ── the live daemon was never touched ────────────────────────────────────────
python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1
eq  "the real registry is untouched" "$( [ -f "$REG" ] && cksum < "$REG" )" "$REG_BEFORE"

echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]

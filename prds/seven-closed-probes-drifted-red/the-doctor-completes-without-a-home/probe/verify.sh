#!/usr/bin/env bash
# the-doctor-completes-without-a-home — probe harness.
#
# c02546f added doctor's vault row, which read `$HOME` bare (doctor.sh:334).
# doctor runs under `set -uo pipefail`, so in a shell that holds no HOME that
# read does not fail the row — it aborts the whole script. Every row below
# vault (members, memos, workflows, knowledge, briefs, questions, view, plan,
# harnesses, jstests) stops printing, and doctor's report ends mid-sentence.
#
# That is exactly the environment the committed view-row harness runs doctor
# in: `env -i PEARDE_PORT=<port> /bin/bash doctor.sh <board>`, scrubbed on
# purpose to prove no unset variable can kill a row. It went red on all four
# of its live checks the moment the vault row landed.
#
# Fixtures are made at run time under mktemp -d, never under .pearde/prds/.
# Nothing here reads or writes the real Obsidian register, the live daemon,
# or any real board: every register is a file this script wrote, and the one
# doctor call that talks to a port uses a scratch port with no listener.
#
#   bash .pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh
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
cd "$ROOT" || exit 1
[ -f "$ROOT/resources/doctor.sh" ] || { echo "  FAIL  no repo root at $ROOT"; exit 1; }
DOCTOR="$ROOT/resources/doctor.sh"
VIEWROW="$BOARD/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh"

pass=0; fail=0; skip=0
ok()  { pass=$((pass+1)); echo "  ok    $1"; }
bad() { fail=$((fail+1)); echo "  FAIL  $1${2:+  — $2}"; }
# A check that could not run is a skip. It is NOT a pass: counting it as one
# manufactures evidence — the mode in which a check stands down is exactly
# the mode in which it cannot fail, so a green count taken there proves
# nothing about the assertion it stood down from.
skp() { skip=$((skip+1)); echo "  skip  $1"; }
# one named row out of a full doctor report
vrow() { printf '%s\n' "$2" | grep -E "^ +$1 " | head -1; }

D="$(mktemp -d /tmp/pearde-nohome.XXXXXX)"
cleanup() { rm -rf "$D"; }
trap cleanup EXIT

# the fixture board: a .pearde/ with settings and a vault directory, so the
# vault row reaches its register read instead of stopping at `off`
FIXB="$D/repo/.pearde"
mkdir -p "$FIXB/prds" "$FIXB/.obsidian"
printf 'name: nohome-fixture\nlanguage: English\n' > "$FIXB/settings.md"
BABS="$(cd "$FIXB" && pwd -P)"

# a home that holds an Obsidian register naming this board, and one that
# holds no Obsidian config at all
mkdir -p "$D/home-reg/.config/obsidian" "$D/home-bare"
printf '{"vaults":{"a":{"path":"%s","ts":1}}}\n' "$BABS" \
  > "$D/home-reg/.config/obsidian/obsidian.json"

# every doctor call is pointed at a port nothing real holds
PORT=9147
run_doctor() {  # $1.. = env assignments, then the board
  env -i PATH="$PATH" PEARDE_PORT="$PORT" "$@" /bin/bash "$DOCTOR" "$D/repo" 2>&1
}

# ── 1. the source no longer reads $HOME unguarded ─────────────────────────
# A bare HOME expansion in a `set -u` script is the whole defect. Guarded
# spellings (${HOME:-...}) are not matches, and neither are comment lines —
# the row's own prose names the variable it is explaining.
# `${HOME}` is caught too: it is one brace away from `$HOME` and equally
# fatal under `set -u`. Only `${HOME` followed by an operator (`:-`, `-`,
# `+`, `:+`) is a guarded read.
BARE=$(grep -nE '(^|[^{A-Za-z_])\$HOME|\$\{HOME\}' "$DOCTOR" | grep -vE '^[0-9]+:[[:space:]]*#' || true)
[ -z "$BARE" ] && ok "no unguarded \$HOME read anywhere in doctor.sh" \
                || bad "doctor.sh still reads \$HOME bare" "$(printf '%s' "$BARE" | head -2 | tr '\n' ' ')"

# ── 2. no HOME at all: the report runs to the end ─────────────────────────
out="$(run_doctor)"
[ "$(printf '%s\n' "$out" | grep -c 'unbound variable')" -eq 0 ] \
  && ok "no unbound-variable line in doctor's report under a scrubbed env" \
  || bad "doctor trips over an unset variable" "$(printf '%s\n' "$out" | grep 'unbound variable' | head -1)"

# every row that sits below the vault row in the script must still print.
# `vault` itself is the row that used to abort; `view` and `plan` are the
# proof the script kept going after it.
MISSING=""
for r in board vault view plan; do
  [ -n "$(vrow "$r" "$out")" ] || MISSING="$MISSING $r"
done
[ -z "$MISSING" ] && ok "every row below vault still prints with no HOME (board vault view plan)" \
                  || bad "doctor stopped before these rows:$MISSING"

# ── 3. the row reports rather than aborting, and says the same thing with
#       and without HOME on one and the same board ────────────────────────
V="$(vrow vault "$out")"
if printf '%s' "$V" | grep -qE 'vault +(ok|off|broken) '; then
  ok "the vault row reports rather than aborting — $(printf '%s' "$V" | sed 's/^ *//')"
else
  bad "the vault row should report ok, off or broken when no HOME is exported" "got: ${V:-<no row>}"
fi

# The same fixture board, run twice: once with HOME set to the home this uid
# actually has, once with the variable scrubbed away. A shell that exports no
# HOME still HAS a home — `env -i /bin/bash -c 'echo ~'` prints it, and
# doctor's own `plugins` row resolves it through getpwuid in that same run —
# so both runs read the same register and must reach the same verdict: same
# row text, same exit code. Reading only the variable makes the scrubbed run
# say `ok … cannot be read here` about a board the with-home run calls
# `broken`, which is this row's own failure turned green by unsetting one
# variable. That is what this check exists to catch, and it goes red the
# moment the resolution below OBSHOME is taken back out.
RESHOME="$(python3 -c 'import os,pwd;print(pwd.getpwuid(os.getuid()).pw_dir)' 2>/dev/null || true)"
run_doctor HOME="$RESHOME" > "$D/out-home"   2>&1; RCH=$?
run_doctor                 > "$D/out-nohome" 2>&1; RCN=$?
VH="$(vrow vault "$(cat "$D/out-home")"   | sed 's/^ *//')"
VN="$(vrow vault "$(cat "$D/out-nohome")" | sed 's/^ *//')"
if [ -n "$RESHOME" ] && [ -n "$VH" ] && [ "$VH" = "$VN" ] && [ "$RCH" = "$RCN" ]; then
  ok "no HOME reaches the same verdict as HOME=$RESHOME on one board — $VH (exit $RCH both)"
else
  bad "the no-HOME run disagrees with the with-HOME run on the same board" \
      "with HOME=$RESHOME rc=$RCH: ${VH:-<no row>} // scrubbed rc=$RCN: ${VN:-<no row>}"
fi

# ── 4. the guard did not cost the row its real answers ────────────────────
# a home whose register names this board → ok, registered
out="$(run_doctor HOME="$D/home-reg")"
V="$(vrow vault "$out")"
printf '%s' "$V" | grep -qE 'vault +ok .*registered with Obsidian' \
  && ok "HOME with a register naming the board still reads ok, registered" \
  || bad "registered board should read ok" "got: ${V:-<no row>}"

# a home with no Obsidian config → ok, nothing to register (the branch
# init-seeds-a-board-doctor-calls-green needs green)
out="$(run_doctor HOME="$D/home-bare")"
V="$(vrow vault "$out")"
printf '%s' "$V" | grep -qE 'vault +ok .*Obsidian not installed here' \
  && ok "HOME holding no Obsidian config still reads ok, nothing to register" \
  || bad "a home with no Obsidian config should read ok" "got: ${V:-<no row>}"

# a home whose register does NOT name this board → broken, the row's point
mkdir -p "$D/home-other/.config/obsidian"
printf '{"vaults":{"a":{"path":"/somewhere/else","ts":1}}}\n' \
  > "$D/home-other/.config/obsidian/obsidian.json"
out="$(run_doctor HOME="$D/home-other")"
V="$(vrow vault "$out")"
printf '%s' "$V" | grep -qE 'vault +broken' \
  && ok "an unregistered board is still called broken — the guard did not mute the row" \
  || bad "unregistered board should read broken" "got: ${V:-<no row>}"

# XDG_CONFIG_HOME is still honoured where it is the register that exists: a
# home that holds no macOS `Library/Application Support` register. It does
# not outrank one that does exist — that precedence is the committed one and
# reads the same whether HOME was exported or resolved from the passwd
# database, which is why this check no longer has a "no home at all" leg:
# there is no such shell on a host whose uid has a passwd entry, and the
# earlier leg only reached XDG because `python3` was forced to fail.
mkdir -p "$D/xdg/obsidian"
printf '{"vaults":{"a":{"path":"%s","ts":1}}}\n' "$BABS" \
  > "$D/xdg/obsidian/obsidian.json"
V1="$(vrow vault "$(run_doctor HOME="$D/home-bare" XDG_CONFIG_HOME="$D/xdg")")"
if printf '%s' "$V1" | grep -qE 'vault +ok .*registered with Obsidian'; then
  ok "XDG_CONFIG_HOME finds the register over a home that holds no macOS register"
else
  bad "XDG_CONFIG_HOME should be read when the home holds no macOS register" \
      "got: ${V1:-<no row>}"
fi

# ── 4b. THE SAME-VERDICT PREDICATE WITH NO USABLE python3 ─────────────────
# The environments this row exists for — `env -i`, launchd, a container —
# are exactly the thin-PATH ones, and on macOS `/usr/bin/python3` is a stub
# that exits non-zero without the Command Line Tools. Check 5 above runs the
# predicate on a full PATH; a fallback that resolves the home through
# `python3` passes there and still converts a true `broken` into `ok` here.
# So the predicate is run again in three shapes with no usable interpreter:
#   a) `stub`   — a `python3` first on PATH that exits 1, the macOS stub
#   b) `thin`   — a PATH holding only the handful of tools doctor needs and
#                 no python3 at all: the launchd / container shape
#   c) `nopath` — no PATH exported at all (`env -i` with only PEARDE_PORT);
#                 bash then supplies its own default PATH, so this shape is
#                 about the scrubbed environment, not about a missing python3
# Same board, same two legs each time, same requirement: same row text. Both
# legs of a shape run equally degraded, so the comparison stays honest even
# where the rest of the report is not.
mkdir -p "$D/nopy" "$D/thinbin"
printf '#!/bin/sh\nexit 1\n' > "$D/nopy/python3"; chmod +x "$D/nopy/python3"
for c in bash sh grep sed awk cat ls mkdir dirname basename head tail tr cut \
         sort uniq wc find stat date printf chmod rm cp mv xargs; do
  p="$(command -v "$c" 2>/dev/null)" && ln -sf "$p" "$D/thinbin/$c"
done
NOPYFAIL=""
for shape in stub thin nopath; do
  case "$shape" in
    stub)   E="PATH=$D/nopy:$PATH" ;;
    thin)   E="PATH=$D/thinbin" ;;
    nopath) E="PEARDE_PORT=$PORT" ;;
  esac
  WH="$(vrow vault "$(env -i "$E" PEARDE_PORT="$PORT" HOME="$RESHOME" /bin/bash "$DOCTOR" "$D/repo" 2>&1)")"
  NH="$(vrow vault "$(env -i "$E" PEARDE_PORT="$PORT" /bin/bash "$DOCTOR" "$D/repo" 2>&1)")"
  WH="$(printf '%s' "$WH" | sed 's/^ *//')"; NH="$(printf '%s' "$NH" | sed 's/^ *//')"
  [ -n "$NH" ] && [ "$WH" = "$NH" ] \
    || NOPYFAIL="$NOPYFAIL [$shape] with HOME: ${WH:-<no row>} // scrubbed: ${NH:-<no row>}"
done
if [ -z "$NOPYFAIL" ]; then
  ok "with no usable python3 the scrubbed run still reaches the with-HOME verdict — a python3 stub that exits 1, a thin PATH with no python3, and no PATH exported"
else
  bad "with no usable python3 the no-HOME run disagrees with the with-HOME run" "$NOPYFAIL"
fi

# ── 4c. the last resort, at the source ────────────────────────────────────
# On any host whose uid has a passwd entry this arm is unreachable: bash
# expands `~` out of the passwd database with no PATH and no interpreter,
# which is the whole point of resolving with a builtin first. So it is
# asserted at the source rather than driven. Two things must hold. It must
# report `broken`, not `ok` — a row that could not perform its check has not
# passed it, and doctor already answers that way for an unusable interpreter
# (`index broken · no python3 to read it`). And it must claim only what it
# can check — that the home could not be resolved — never that the uid HAS
# no home, and never that Obsidian is absent.
ARM="$(grep -A2 -F 'elif [ -z "$OBSCFG" ]; then' "$DOCTOR" | grep -E '^[[:space:]]*row vault ' | head -1)"
if printf '%s' "$ARM" | grep -qE '^[[:space:]]*row vault broken ' \
   && printf '%s' "$ARM" | grep -qF 'could not be resolved' \
   && ! printf '%s' "$ARM" | grep -qE 'resolves to no home|not installed here'; then
  ok "the last-resort arm reports broken and claims only that the home could not be resolved"
else
  bad "the last-resort arm must report broken and claim only an unresolved home" \
      "got: ${ARM:-<no arm>}"
fi

# ── 5. the harness the defect reddened reads green end to end ─────────────
# Stood down inside a board sweep. That harness binds hard-coded ports
# 8477-8479 with no bind check, and `doctor --harnesses` launches every
# harness at once with PEARDE_HARNESSES=1 (doctor.sh:722, no job cap) — so a
# sweep would run it there AND here at the same time on the same ports, and
# this probe would be green or red by scheduling. It is already in the sweep
# in its own right, so running it twice buys nothing. Same stand-down for a
# standalone run that finds those ports already held by somebody else's run.
#
# The stand-down is a SKIP and is not counted as a pass. In the stood-down
# mode this check cannot fail, so a green count taken there is produced by
# the stand-down and not by the harness; counting it would be manufactured
# evidence. The stand-down also fires on any holder of 8477-8479 — a bare
# unrelated socket is enough — and that harness leaks its listeners on every
# early exit (report finding 7), so one leak would otherwise retire this
# check forever while it still read as a pass.
port_busy() { (: < "/dev/tcp/127.0.0.1/$1") >/dev/null 2>&1; }
VRBUSY=""
for p in 8477 8478 8479; do port_busy "$p" && VRBUSY="$VRBUSY $p"; done
if [ -n "${PEARDE_HARNESSES:-}" ]; then
  skp "the view-row harness is left to the sweep's own run of it — it binds 8477-8479 and this is a sweep; not asserted here"
elif [ -n "$VRBUSY" ]; then
  skp "the view-row harness could not be run — 8477-8479 are held elsewhere (:$VRBUSY); not asserted here"
elif [ -f "$VIEWROW" ]; then
  vout="$(bash "$VIEWROW" 2>&1)"; vrc=$?
  vsum="$(printf '%s\n' "$vout" | grep -E '^[0-9]+ checks' | head -1)"
  if [ "$vrc" -eq 0 ] && printf '%s' "$vsum" | grep -qE '· 0 fail$'; then
    ok "the view-row harness reads green end to end — $vsum"
  else
    bad "the view-row harness is still red (rc=$vrc)" "${vsum:-no summary}
$(printf '%s\n' "$vout" | grep '^  FAIL' | head -4)"
  fi
else
  bad "the view-row harness is missing" "$VIEWROW"
fi

echo "$((pass+fail+skip)) checks · $pass pass · $fail fail · $skip skip"
echo "probe harness complete"
[ "$fail" -eq 0 ] || exit 1

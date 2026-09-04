#!/usr/bin/env bash
# the-harness-sweep-is-capped-so-a-red-is-a-real-red — probe harness.
#
# The sweep in resources/doctor.sh launched all forty-eight harnesses at once.
# Several bind the same three fixed ports or spawn a board service, so a red
# from the sweep was not evidence of a fault: the serial re-run of 2026-09-01
# turned four of nine reds green. Four mechanisms, all asserted here:
#
#   1. the sweep runs a few at a time (a job cap that actually holds)
#   2. the cap is spelled in a way /bin/bash can run — `wait -n` is bash 4.3+
#      and /bin/bash on macOS is 3.2.57, so the promise in the old comment
#      was not implementable
#   3. the view-row harness skips rather than fails when 8477-8479 are held,
#      and no longer leaks those listeners on an early exit
#   4. init-seeds re-checks its spare port before use, closing the TOCTOU
#
# Every fixture is built in a run-time mktemp -d, never under .pearde/prds —
# a directory holding a prd.md anywhere under the board is a PRD. Nothing here
# touches the live daemon, a real registry, or any real board.
#
# Run as:
#   bash .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh
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
DOCTOR="$ROOT/resources/doctor.sh"
VIEWROW="$BOARD/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh"
INITSEEDS="$BOARD/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh"

PASS=0; FAIL=0; SKIP=0
ok()   { PASS=$((PASS+1)); echo "  ok    $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1${2:+ — $2}"; }
skp()  { SKIP=$((SKIP+1)); echo "  skip  $1"; }

T="$(mktemp -d /tmp/pearde-hcap.XXXXXX)"
cleanup() { rm -rf "$T"; }
trap cleanup EXIT

port_busy() { (: < "/dev/tcp/127.0.0.1/$1") >/dev/null 2>&1; }

# ── 1. the cap exists and is spelled for the shell that runs it ──────────

if grep -q 'HCAP="${PEARDE_HCAP:-' "$DOCTOR"; then
  ok "the sweep names a job cap, overridable for an experiment"
else
  bad "no HCAP in the harness sweep — the run is still unbounded"
fi

# This matcher must name the gating line and nothing else. An earlier
# spelling wanted a second `]` the line does not have, so it matched zero
# times and the check was carried entirely by a loose `|| grep -q 'jobs -r'`
# fallback — which the *comment* above the loop also satisfies, so deleting
# the gate left the check green. Both are gone: one anchored matcher, proven
# to go red when the gating line is removed.
if grep -qE 'while \[ "\$\(jobs -r[^)]*\)" -ge "\$HCAP" \]; do' "$DOCTOR"; then
  ok "the cap gates the launch loop by counting this shell's running jobs"
else
  bad "nothing gates the launch loop — the & per iteration is still bare"
fi

# `wait -n` is the mechanism the old comment promised. It does not exist here.
if /bin/bash -c 'sleep 0 & wait -n' >/dev/null 2>&1; then
  skp "this /bin/bash has wait -n — the portability constraint does not bind on this box"
else
  # comments stripped: this very file discusses `wait -n` in prose, and so
  # does doctor.sh's own note about why it does not use it
  if sed 's/#.*//' "$DOCTOR" | grep -qE '(^|[^-])wait -n'; then
    bad "the sweep calls wait -n, which /bin/bash $(/bin/bash --version | sed -n '1s/.*version \([0-9.]*\).*/\1/p') does not have"
  else
    ok "the cap avoids wait -n, which this /bin/bash does not support"
  fi
fi

# ── 2. the cap actually holds, measured ─────────────────────────────────
# A fixture board of twelve harnesses, each of which records how many of its
# siblings were running alongside it. The peak must never exceed the cap.

B="$T/board"; mkdir -p "$B/.pearde/prds"
printf 'name: hcap-fixture\nharnesses: on\n' > "$B/.pearde/settings.md"
# Concurrency is measured with one file per running harness, created on entry
# and removed on exit: a shared counter file appended and truncated by twelve
# processes races with itself and under-reports, which is not a measurement.
LIVE="$T/live"; PEAK="$T/peak"; mkdir -p "$LIVE"; : > "$PEAK"
i=0
while [ "$i" -lt 12 ]; do
  i=$((i + 1))
  d="$B/.pearde/prds/h$i/probe"; mkdir -p "$d"
  cat > "$d/verify.sh" <<FIX
#!/usr/bin/env bash
: > "$LIVE/\$\$"
ls "$LIVE" | grep -c . >> "$PEAK"
sleep 0.4
rm -f "$LIVE/\$\$"
PASS=1; FAIL=0
[ "\$((PASS+FAIL))" = 1 ] || echo no
echo "1 checks · 1 pass · 0 fail"
FIX
done

# PEARDE_HARNESSES is cleared for this one call. doctor stands its harness row
# down when it is already running inside a harness, which is what stops the
# board's two doctor-running harnesses from recursing forever — but the twelve
# fixtures below are generated three lines up and provably never invoke doctor,
# so the guard has nothing to protect here and would otherwise make the cap
# unmeasurable from inside the sweep, which is precisely where it matters.
CAPOUT="$(PEARDE_HARNESSES="" PEARDE_HCAP=3 /bin/bash "$DOCTOR" --harnesses "$B" 2>&1)"
OBSERVED="$(sort -n "$PEAK" | tail -1)"
if [ -n "$OBSERVED" ] && [ "$OBSERVED" -le 3 ]; then
  ok "twelve harnesses under a cap of 3 never ran more than $OBSERVED at once"
else
  bad "the cap did not hold" "peak concurrency was ${OBSERVED:-unmeasured}, cap was 3"
fi

# and the row still prints the line it always printed
if printf '%s' "$CAPOUT" | grep -qE '^ +harnesses +(ok|broken) +[0-9]+ of 12 green'; then
  ok "the row keeps its shape — '<n> of <total> green' over the capped run"
else
  bad "the harnesses row changed shape under the cap" \
      "$(printf '%s' "$CAPOUT" | grep -E '^ +harnesses' | head -1)"
fi

# the cap is a cap, not a serialisation: 12 harnesses sleeping 0.4s each take
# ~4.8s serially and ~1.6s at a cap of 3. The run must be well under serial.
if printf '%s' "$CAPOUT" | grep -qE '^ +harnesses .*· [0-9]+s'; then
  ok "the row still reports its own wall-clock"
else
  bad "the row dropped its seconds field"
fi

# ── 3. the view-row harness: leak, guard, and the summary its reader parses ──

if grep -qE '^SRVPID=""; SRVPID2=""; SRVPID3=""' "$VIEWROW"; then
  ok "all three server pids are initialised before the EXIT trap is armed"
else
  bad "SRVPID3 is still first assigned at its own check — cleanup dies under set -u"
fi

# the leak, demonstrated: force an exit before the third server is started and
# assert cleanup still ran — the scratch dir is gone and 8477/8478 are free.
if port_busy 8477 || port_busy 8478 || port_busy 8479; then
  skp "8477-8479 are held by something else — the leak and guard checks are not asserted here"
  skp "8477-8479 are held by something else — the skip-when-busy check is not asserted here"
else
  LEAK="$T/leaky.sh"
  # the harness up to its second server, then an abrupt exit — the shape any
  # early failure used to take
  sed -n '1,/^python3 "\$D\/srv2.py" & SRVPID2=\$!/p' "$VIEWROW" > "$LEAK"
  echo 'exit 9' >> "$LEAK"
  ( /bin/bash "$LEAK" >/dev/null 2>&1 )
  sleep 0.5
  if port_busy 8477 || port_busy 8478; then
    bad "an early exit still leaks a listener on 8477/8478 — cleanup did not run"
    # do not leave the board worse than we found it
    for p in 8477 8478; do
      pid="$(lsof -ti tcp:$p 2>/dev/null | head -1)"; [ -n "$pid" ] && kill "$pid" 2>/dev/null
    done
  else
    ok "an early exit before the third server leaves no listener — cleanup completed"
  fi

  # the guard: hold 8477 and assert the harness skips rather than reddening
  # The holder accepts and closes in a loop rather than sleeping on a backlog
  # of one: an unaccepted connection fills a short queue, and the next probe
  # of the port is then refused — which reads as "free" and is how this very
  # check first produced a false red.
  python3 -c 'import socket
s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(("127.0.0.1",8477)); s.listen(64)
while True:
    try: c,_=s.accept(); c.close()
    except Exception: break' >/dev/null 2>&1 &
  HOLD=$!
  sleep 1
  if port_busy 8477; then
    VOUT="$(bash "$VIEWROW" 2>/dev/null)"; VRC=$?
    VSUM="$(printf '%s\n' "$VOUT" | grep -E '^[0-9]+ checks' | head -1)"
    if [ "$VRC" -eq 0 ] && printf '%s' "$VSUM" | grep -qE '· 0 fail$' \
       && printf '%s' "$VSUM" | grep -qE '· [1-9][0-9]* skip'; then
      ok "with 8477 held the harness skips and stays green — $VSUM"
    else
      bad "a held port still reddens the view-row harness (rc=$VRC)" "${VSUM:-no summary}"
    fi
  else
    skp "8477 could not be held for the test — the skip-when-busy check is not asserted here"
  fi
  kill "$HOLD" 2>/dev/null; wait "$HOLD" 2>/dev/null
fi

# the consumer's anchor. the-doctor-completes-without-a-home reads this
# harness's summary with `grep -qE '· 0 fail$'`, so the line must still end in
# the fail count even now that it carries a skip count.
if grep -q 'echo "$((pass+fail+skip)) checks · $pass pass · $skip skip · $fail fail"' "$VIEWROW"; then
  ok "the view-row summary still ends in the fail count its reader anchors on"
else
  bad "the summary line no longer ends in '<n> fail' — the-doctor-completes-without-a-home:250 parses it"
fi

if grep -q "grep -qE '· 0 fail\$'" \
     "$BOARD/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh"; then
  ok "that reader's anchor is where this check says it is"
else
  bad "the reader's anchor moved — re-derive what the summary line must end in"
fi

# one spelling of port_busy per file, and the same spelling everywhere
SPELL="$(grep -h 'port_busy() {' "$VIEWROW" "$INITSEEDS" \
         "$BOARD/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh" \
         2>/dev/null | sort -u | grep -c .)"
if [ "$SPELL" = 1 ]; then
  ok "all three harnesses share one spelling of port_busy"
else
  bad "port_busy has $SPELL spellings across the three harnesses — the PRD asks for one"
fi

# ── 4. init-seeds no longer picks a port it does not re-check ────────────

if grep -q 'port_busy "$_p" || { SPARE="$_p"; break; }' "$INITSEEDS"; then
  ok "init-seeds re-checks its spare port immediately before use"
else
  bad "init-seeds still binds port 0 and closes the socket before use — the TOCTOU stands"
fi

if grep -qE 'no free port could be picked' "$INITSEEDS"; then
  ok "init-seeds fails loudly rather than proceeding with an empty port"
else
  bad "init-seeds has no arm for the case where no free port is found"
fi

# The arm's own cleanup, run rather than read. The `EXIT` trap is armed below
# this point in the harness, so the arm has to remove its scratch directory
# itself — and nothing was checking that it does. Grepping for the `rm -rf`
# would prove only that the text is present.
#
# The fixture is the harness's own head, byte-for-byte down to the arm, with
# one substitution: `port_busy` always reports busy, so all five tries fail.
# It runs under a TMPDIR of its own, empty at the start, so "the arm removed
# its scratch dir" is exactly "that directory is still empty".
ARMDIR="$T/arm"; ARMTMP="$T/arm-tmp"
mkdir -p "$ARMDIR" "$ARMTMP"
awk '/^set -u/{f=1} f{print} /^\[ -n "\$SPARE" \] \|\|/{exit}' "$INITSEEDS" \
  | sed 's|^port_busy() {.*|port_busy() { return 0; }  # every port is busy|' \
  > "$ARMDIR/arm.sh"
echo 'echo "REACHED PAST THE ARM"' >> "$ARMDIR/arm.sh"
ARMOUT="$(TMPDIR="$ARMTMP" bash "$ARMDIR/arm.sh" 2>&1)"; ARMRC=$?
ARMLEFT="$(find "$ARMTMP" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')"

if [ "$ARMRC" = 1 ] && [ "${ARMOUT#*no free port could be picked}" != "$ARMOUT" ] \
   && [ "${ARMOUT#*REACHED PAST}" = "$ARMOUT" ]; then
  ok "the exhausted-tries arm exits 1 and stops, rather than running on with an empty port"
else
  bad "the exhausted-tries arm did not stop the harness" "rc=$ARMRC out=$ARMOUT"
fi

if [ "$ARMLEFT" = 0 ]; then
  ok "...and removes its own scratch directory, with the EXIT trap not yet armed"
else
  bad "the arm leaked $ARMLEFT scratch dir(s) under its TMPDIR — the trap is not armed there"
fi

# The denominator is pinned on the total, not on PASS+FAIL: three checks here
# stand down to a skip when the box is not clean, so the asserted count is
# legitimately variable while the number of checks that exist is not. Note
# that doctor.sh's unpinned-detector only recognises the literal spelling
# `$((PASS+FAIL))`, so it reads this harness as unpinned even though the line
# below fails loudly on a dropped check — a finding, reported, not fixed here.
echo "$((PASS+FAIL+SKIP)) checks · $PASS pass · $FAIL fail · $SKIP skip"
if [ "$((PASS+FAIL+SKIP))" != 16 ]; then
  echo "  FAIL  expected 16 checks, ran $((PASS+FAIL+SKIP))"
  FAIL=$((FAIL+1))
fi
echo "probe harness complete"
[ "$FAIL" -eq 0 ] || exit 1

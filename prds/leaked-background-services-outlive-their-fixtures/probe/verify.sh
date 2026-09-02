#!/usr/bin/env bash
# leaked-background-services-outlive-their-fixtures — the leak, reproduced.
#
# Five mechanisms, each measured on this probe's OWN pids. A count of
# `serve.py run` on the machine is a number a neighbouring session moves, so
# nothing here counts one: every assertion names a pid this script started, or
# a directory this script made.
#
# Run as:
#   bash .pearde/prds/leaked-background-services-outlive-their-fixtures/probe/verify.sh
#
# The live daemon on 8443 is never touched: every fixture binds a spare port
# picked at run time, and the fixture boards live under `mktemp -d`.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
SRV="$ROOT/resources/board/serve.py"

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ok    $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL  $1${2:+ — $2}"; }

T="$(mktemp -d /tmp/pearde-leak.XXXXXX)"
PIDS=""            # every daemon this probe starts, killed unconditionally
cleanup() {
  for p in $PIDS; do kill -9 "$p" 2>/dev/null; done
  rm -rf "$T"
}
trap cleanup EXIT INT TERM

spare() { python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()'; }
alive() { kill -0 "$1" 2>/dev/null; }

# a fixture board, the way every harness on this repo builds one
mkboard() {   # $1 = dir
  mkdir -p "$1/.pearde/prds"
  printf 'name: leak-fixture-%s\n' "$(basename "$1")" > "$1/.pearde/settings.md"
}

# ── 1. a daemon outlives the directory it watches ────────────────────────────
# The watch loop calls digest(b.path); a vanished board raises OSError, the
# loop sets d=None and falls through. Nothing anywhere reaps the process.

D1="$T/b1"; mkboard "$D1"
P1="$(spare)"
export PEARDE_IDLE_EXIT_S=3
PEARDE_PORT="$P1" python3 "$SRV" run >"$T/log1" 2>&1 &
S1=$!; PIDS="$PIDS $S1"
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
  curl -fsS -m 1 "http://127.0.0.1:$P1/status" >/dev/null 2>&1 && break
  sleep 0.2
done
( cd "$D1" && PEARDE_PORT="$P1" python3 "$SRV" ensure "$D1/.pearde" ) >/dev/null 2>&1
rm -rf "$D1"
sleep 8
if alive "$S1"; then
  bad "a daemon whose only board directory is deleted keeps running (pid $S1)"
else
  ok  "the daemon exited when its last board went away"
fi
kill -9 "$S1" 2>/dev/null; wait "$S1" 2>/dev/null

# ── 2. `ensure` puts the daemon in its own session, so killing the fixture's
#       whole process group leaves it running ─────────────────────────────────
# This is the leak an EXIT trap cannot close: a harness killed with SIGKILL,
# or a session torn down, never runs its trap, and the daemon is not even in
# the group the kill reaches.

D2="$T/b2"; mkboard "$D2"
P2="$(spare)"
cat > "$T/fixture.sh" <<FIX
#!/usr/bin/env bash
set -u
trap 'PEARDE_PORT="$P2" python3 "$SRV" stop >/dev/null 2>&1' EXIT
cd "$D2" && PEARDE_PORT="$P2" PEARDE_IDLE_EXIT_S=3 python3 "$SRV" ensure "$D2/.pearde" >/dev/null 2>&1
echo up > "$T/fixture.up"
sleep 60
FIX
# macOS ships no setsid(1); Python's os.setsid gives the fixture its own
# session, so the kill below reaches the fixture's whole group and nothing else
python3 -c 'import os,sys;os.setsid();os.execv(sys.argv[1],sys.argv[1:])' \
  /bin/bash "$T/fixture.sh" >/dev/null 2>&1 &
FIXPID=$!
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25; do
  [ -f "$T/fixture.up" ] && break
  sleep 0.2
done
DPID="$(curl -fsS -m 2 "http://127.0.0.1:$P2/status" 2>/dev/null \
        | sed -n 's/.*"pid"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p')"
if [ -z "$DPID" ]; then
  bad "the fixture's daemon never came up on $P2 — mechanism 2 not measured"
else
  PIDS="$PIDS $DPID"
  kill -9 -- "-$FIXPID" 2>/dev/null || kill -9 "$FIXPID" 2>/dev/null
  sleep 8
  if alive "$DPID"; then
    bad "SIGKILL on the fixture's whole process group left its daemon alive (pid $DPID)"
  else
    ok  "the daemon died with the fixture that started it"
  fi
  kill -9 "$DPID" 2>/dev/null
fi

# ── 3. the already-stranded ones can be found and stopped ────────────────────
# `status` speaks to one port; a daemon on a spare PEARDE_PORT is reachable by
# no port anyone remembers. `reap` starts from the process table instead. Two
# things are asserted, and the second matters more than the first: that it
# names a stranded daemon THIS probe started, and that it keeps a daemon
# watching a board still on disk — a reaper that stops the machine's real
# service is worse than the leak.

D3="$T/b3"; mkboard "$D3"            # a stranded one: board deleted after
P3="$(spare)"
PEARDE_IDLE_EXIT_S=9999 PEARDE_PORT="$P3" python3 "$SRV" run >"$T/log3" 2>&1 &
S3=$!; PIDS="$PIDS $S3"
D4="$T/b4"; mkboard "$D4"            # a kept one: board stays on disk
P4="$(spare)"
PEARDE_IDLE_EXIT_S=9999 PEARDE_PORT="$P4" python3 "$SRV" run >"$T/log4" 2>&1 &
S4=$!; PIDS="$PIDS $S4"
for _ in $(seq 1 40); do
  curl -fsS -m 1 "http://127.0.0.1:$P3/status" >/dev/null 2>&1 \
    && curl -fsS -m 1 "http://127.0.0.1:$P4/status" >/dev/null 2>&1 && break
  sleep 0.25
done
( cd "$D3" && PEARDE_PORT="$P3" python3 "$SRV" ensure "$D3/.pearde" ) >/dev/null 2>&1
( cd "$D4" && PEARDE_PORT="$P4" python3 "$SRV" ensure "$D4/.pearde" ) >/dev/null 2>&1
# wait for the REGISTRATION, not just the bind: a daemon whose board has not
# landed yet reads as "listening on no port" or "watching no board", and this
# section is about the judgement, not about the race
for _ in $(seq 1 40); do
  curl -fsS -m 1 "http://127.0.0.1:$P4/status" 2>/dev/null | grep -q '"b4"' && break
  sleep 0.25
done
rm -rf "$D3"
sleep 2

# First, at the shipped grace: both of these daemons are seconds old, and a
# daemon seconds old is the shape a `SessionStart` hook leaves behind between
# `ensure`'s bind and the board's first `/register`. Neither may be touched.
YOUNG="$(python3 "$SRV" reap --dry-run 2>&1)"
case "$YOUNG" in
  *"would stop pid $S3"*)
    bad "reap would stop a daemon seconds old — a session start's daemon looks exactly like this (pid $S3)" ;;
  *"keeping pid $S3"*)
    ok  "reap keeps a just-started daemon watching nothing (pid $S3) — the SessionStart window" ;;
  *) bad "reap said nothing about the just-started pid $S3" "$(printf '%s' "$YOUNG" | tr '\n' ' ')" ;;
esac

# and now with the grace explicitly stood down, which is the only way to
# measure the stranded judgement itself on a daemon this probe just started.
# `--pid` scopes both the dry run and the real one to this probe's own pids: a
# grace-less sweep over the whole process table would stop a neighbouring
# session's daemon inside the very window the grace exists to protect — this
# PRD's own leak, manufactured by its own check.
REAP="$(PEARDE_REAP_GRACE_S=0 python3 "$SRV" reap --dry-run --pid "$S3" --pid "$S4" 2>&1)"
case "$REAP" in
  *"would stop pid $S3"*) ok "reap names the stranded daemon this probe left (pid $S3)" ;;
  *) bad "reap did not name the stranded pid $S3" "$(printf '%s' "$REAP" | tr '\n' ' ')" ;;
esac
case "$REAP" in
  *"keeping pid $S4"*) ok "reap keeps the daemon whose board is still on disk (pid $S4)" ;;
  *) bad "reap did not keep the live-board daemon pid $S4" "$(printf '%s' "$REAP" | tr '\n' ' ')" ;;
esac

# and the real run stops it. Scoped to this probe's own pid — never a count.
PEARDE_REAP_GRACE_S=0 python3 "$SRV" reap --pid "$S3" --pid "$S4" >/dev/null 2>&1
sleep 2
if alive "$S3"; then
  bad "reap left the stranded daemon running (pid $S3)"
else
  ok  "reap stopped the stranded daemon"
fi
if alive "$S4"; then
  ok  "reap left the daemon with a live board alone (pid $S4)"
else
  bad "reap stopped a daemon that was watching a board still on disk (pid $S4)"
fi
kill -9 "$S3" "$S4" 2>/dev/null

# ── 4. the reap must not undo a session start ────────────────────────────────
# `pearde guard on` writes a SessionStart hook that runs `serve.py ensure`, and
# `doctor.sh --harnesses` ends its sweep with `serve.py reap`. Both are normal
# behaviour on this machine and they meet routinely. In the window between
# `ensure` binding its port and the board's first `/register`, a daemon
# somebody very much wants watches nothing and is indistinguishable from a
# leak — so this section runs the hook's own command line and then reaps, at
# the shipped grace, and asserts the board is still being watched.

D5="$T/b5"; mkboard "$D5"
P5="$(spare)"
# the idle leash is parked high here on purpose: this section measures `reap`
# against a session start, and a daemon that exited on its own three seconds
# in would read as a reap that killed it. `$T` is under /tmp, so the fixture
# board is EPHEMERAL and the owner rule would otherwise apply the moment the
# subshell below returns.
HOOKCMD="python3 $SRV ensure >/dev/null 2>&1 || true"
( cd "$D5" && PEARDE_PORT="$P5" PEARDE_IDLE_EXIT_S=9999 sh -c "$HOOKCMD" )
D5PID="$(curl -fsS -m 2 "http://127.0.0.1:$P5/status" 2>/dev/null \
         | sed -n 's/.*"pid"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p')"
if [ -z "$D5PID" ]; then
  bad "the session-start hook's own command line started no daemon on $P5"
  bad "so the reap-against-a-session-start collision could not be measured"
else
  PIDS="$PIDS $D5PID"
  python3 "$SRV" reap >/dev/null 2>&1
  sleep 1
  if alive "$D5PID"; then
    ok  "a reap right after a session start leaves its daemon alone (pid $D5PID)"
  else
    bad "reap killed the daemon a session start had just brought up (pid $D5PID)"
  fi
  WANT="$(cd "$D5" && pwd -P)/.pearde"
  if PEARDE_PORT="$P5" python3 "$SRV" status 2>/dev/null | grep -qF "$WANT"; then
    ok  "and the board the hook registered is still watched"
  else
    bad "the board the session start registered is no longer watched" "$WANT"
  fi
  PEARDE_PORT="$P5" python3 "$SRV" stop >/dev/null 2>&1
  kill -9 "$D5PID" 2>/dev/null
fi

# ── 5. `--pid` refuses a pid it cannot read ─────────────────────────────────
# `--pid` exists so a check can stand REAP_GRACE_S down without reaching a
# neighbouring session's daemon. A spelling of it that falls back to the whole
# process table when the pid is malformed is worse than not having the flag:
# `--pid "$PIDVAR"` with PIDVAR unset reads as "sweep everything", silently,
# at whatever grace the caller stood down. It must refuse instead.

for arg in abc "" -- 12x; do
  OUT="$(python3 "$SRV" reap --dry-run --pid "$arg" 2>&1)"; RC=$?
  LABEL="reap --pid '$arg' refuses instead of sweeping the machine"
  if [ "$RC" = 0 ]; then
    bad "$LABEL" "exit 0, and it reported on: $(printf '%s' "$OUT" | tr '\n' ' ')"
  elif printf '%s' "$OUT" | grep -q 'keeping pid\|would stop pid\|stopped pid'; then
    bad "$LABEL" "it judged a daemon anyway: $(printf '%s' "$OUT" | tr '\n' ' ')"
  else
    ok  "$LABEL"
  fi
done

# ── 6. the grace expires ────────────────────────────────────────────────────
# Every stop assertion above stands the grace down to zero, so all of them
# stay green if REAP_GRACE_S is set to a day and the reaper never reaps
# anything again. This is the check that cannot be satisfied that way: a real,
# non-zero grace, genuinely waited out on a daemon this probe started.

D6="$T/b6"; mkboard "$D6"
P6="$(spare)"
PEARDE_IDLE_EXIT_S=9999 PEARDE_PORT="$P6" python3 "$SRV" run >"$T/log6" 2>&1 &
S6=$!; PIDS="$PIDS $S6"
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
  curl -fsS -m 1 "http://127.0.0.1:$P6/status" >/dev/null 2>&1 && break
  sleep 0.2
done
# inside a one-second grace it is kept; two seconds later the same command,
# same grace, must judge it. Both readings are on this probe's own pid.
YOUNG6="$(PEARDE_REAP_GRACE_S=30 python3 "$SRV" reap --dry-run --pid "$S6" 2>&1)"
sleep 2
OLD6="$(PEARDE_REAP_GRACE_S=1 python3 "$SRV" reap --dry-run --pid "$S6" 2>&1)"
case "$YOUNG6" in
  *"keeping pid $S6"*) ok "inside PEARDE_REAP_GRACE_S the daemon is kept (pid $S6)" ;;
  *) bad "the grace did not keep a daemon inside it (pid $S6)" "$(printf '%s' "$YOUNG6" | tr '\n' ' ')" ;;
esac
case "$OLD6" in
  *"would stop pid $S6"*) ok "and once PEARDE_REAP_GRACE_S has passed the same daemon is judged (pid $S6)" ;;
  *) bad "the grace never expires — a daemon older than it is still kept (pid $S6)" "$(printf '%s' "$OLD6" | tr '\n' ' ')" ;;
esac
kill -9 "$S6" 2>/dev/null

# The two checks above both name PEARDE_REAP_GRACE_S explicitly, so neither
# would notice the shipped DEFAULT being widened to a day — which keeps every
# other assertion here green while the reaper never reaps anything again. A
# bound, not a pinned literal: 30 or 120 pass, 86400 does not.
DEF="$(python3 -c 'import importlib.util,sys
sp=importlib.util.spec_from_file_location("s",sys.argv[1]); m=importlib.util.module_from_spec(sp)
sp.loader.exec_module(m); print(m.REAP_GRACE_S)' "$SRV" 2>/dev/null)"
if [ -z "$DEF" ]; then
  bad "the shipped PEARDE_REAP_GRACE_S default could not be read from $SRV"
elif [ "$(python3 -c "print(1 if 0 < float('$DEF') <= 600 else 0)")" = 1 ]; then
  ok  "the shipped grace default is a real wait a session can outlive (${DEF}s)"
else
  bad "the shipped grace default is ${DEF}s — long enough that nothing is ever reaped"
fi

# ── 7. a malformed neighbour does not take the whole reap down ──────────────
# `/status` is another process's JSON. A board entry mid-register carries a
# null `path`, and `b.get("path", "")` returns that None — the default is only
# for a MISSING key — so `os.path.isdir(None)` raised TypeError and the reap
# died with a traceback before judging anything. A reaper that crashes on one
# malformed neighbour reaps nothing at all, which is worse than the leak.

cat > "$T/liar.py" <<'LIAR'
import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        b = json.dumps({"pid": os.getpid(),
                        "boards": [{"name": None, "path": None}]}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers()
        self.wfile.write(b)
    def log_message(self, *a): pass
HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
LIAR
P7="$(spare)"
python3 "$T/liar.py" "$P7" >/dev/null 2>&1 &
S7=$!; PIDS="$PIDS $S7"
for _ in $(seq 1 40); do
  curl -fsS -m 1 "http://127.0.0.1:$P7/status" >/dev/null 2>&1 && break
  sleep 0.25
done
# the grace short-circuits before the payload is ever parsed, so it has to
# be stood down to reach the line that crashed. This names one pid — its
# own — and stops nothing: `stranded()` is a question, not an action.
VERDICT="$(PEARDE_REAP_GRACE_S=0 python3 - "$SRV" "$S7" <<'CALL' 2>&1
import importlib.util, sys
sp = importlib.util.spec_from_file_location("srv", sys.argv[1])
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
print(m.stranded(int(sys.argv[2])))
CALL
)"
case "$VERDICT" in
  *Traceback*|*TypeError*)
    bad "stranded() crashes on a /status board entry whose path is null" "$(printf '%s' "$VERDICT" | tr '\n' ' ')" ;;
  *"(True,"*)
    ok  "a /status board entry with a null path is judged, not crashed on" ;;
  *) bad "stranded() gave no verdict on the malformed neighbour" "$(printf '%s' "$VERDICT" | tr '\n' ' ')" ;;
esac
kill -9 "$S7" 2>/dev/null

echo
[ "$((PASS+FAIL))" = 17 ] || echo "  FAIL  the probe ran $((PASS+FAIL)) checks, not the 17 it holds"
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]

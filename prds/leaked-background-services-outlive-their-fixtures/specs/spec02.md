---
complexity: 10
footprint:
  - resources/board/serve.py
  - resources/pearde.py
  - references/parts/view.md
---

# spec02 — `reap` finds the ones already stranded, and keeps the real one

spec01 stops new leaks; this clears the ones running when it landed, and the
case spec01 cannot reach — a daemon that died between `run` and its first
`/register`, listening on a port nothing remembers. There is no machine-wide
registry to consult and there must not be one (`resources/invariants/
every-artifact-lands-inside-the-board.sh` checks 2 and 4 exist to keep it
gone), so the scan starts from the process table: `ps` for every `serve.py
run` argv, `lsof` for the port that pid listens on, `GET /status` on that port
for what it watches, and `os.path.isdir` on each board path for whether
anyone still needs it.

**What stands.** `daemon_pids()`, `listen_port()`, `age_s()`, `stranded()`
and `cmd_reap()` in `resources/board/serve.py`, the `reap` branch in
`main()`, `--dry-run`, `--pid`, `REAP_GRACE_S`, and the usage line. `reap` is
in `FORWARD["view"]` in `resources/pearde.py` and `references/parts/view.md`
names it among the verbs. Measured live in the probe pass: it stopped two
stranded daemons and kept three, pid 28740 — the machine's registered
service — among them.

**What the implementer added.** `--pid` — and its refusal of a value that is
not a process id, which is the whole point of it — and the block below
re-aimed onto it. Also one crash: `stranded()` read a board's path as
`b.get("path", "")`, and that default only covers a MISSING key, so a
neighbour's `/status` carrying `"path": null` — a board mid-register — put
`None` into `os.path.isdir()` and the whole reap died with a traceback
before judging anything. There is a daemon on this machine that serves
exactly that payload; the probe now stands one up on purpose. The block as written asserted `would stop` on a daemon it had started
seconds earlier, which `REAP_GRACE_S` correctly refuses, and then ran a real
machine-wide reap to prove the stop — a command that with the grace stood
down would reach a neighbouring session's just-started daemon.

Three rules the implementation must keep, because breaking any of them is
worse than the leak. A daemon watching **one** board still on disk is kept,
whatever port it is on and whoever started it — the board's own directory is
the whole test, and it is the one test no neighbouring session can move under
us. A daemon whose `/status` reports a different pid than the one asked about
is kept, not stopped: the port was inherited or reused and the answer is not
about it. And a daemon younger than `PEARDE_REAP_GRACE_S` (default 60s) is
kept before either of those is even asked — `a-session-start-brings-the-board-up`
landed a `SessionStart` hook that runs `serve.py ensure`, so a daemon somebody
very much wants, watching nothing until its `/register` arrives, is normal
behaviour on this machine, and spec03 has `doctor.sh` end every sweep with a
reap. The two meet routinely and the grace is what keeps that safe.

That grace is also why `reap` takes `--pid`. A check cannot reach the stranded
judgement on a daemon it just started without standing the grace down, and a
grace-less sweep over the whole process table would stop a neighbouring
session's daemon in exactly the window the grace protects. `--pid` narrows the
sweep to the pids a check started; the sweep `doctor.sh` runs names no pid and
keeps the shipped grace.

Note for the implementer: `restart()` re-execs as `run <board>…`, so a
hot-reloaded daemon's argv does **not** end in `run`. A matcher anchored on
`serve\.py run$` sees no daemon at all on a machine whose service has ever
reloaded. `daemon_pids()` matches argv position, not the end of the line.

## Acceptance

- [x] `python3 resources/board/serve.py reap --dry-run` prints one line per other `serve.py run` pid, each `keeping` or `would stop`, and a final `serve: <n> of <m> stranded`
- [x] at the shipped `PEARDE_REAP_GRACE_S`, `reap` prints `keeping` for a daemon this check started seconds ago — the shape a `SessionStart` hook's `ensure` leaves between its bind and the board's first `/register`, which `doctor.sh`'s end-of-sweep reap meets routinely
- [x] with `PEARDE_REAP_GRACE_S=0` and `--pid` naming only this check's own pids, `reap` stops the daemon that watches no board at all — the fixture that died between `run` and its first `/register` — named by that pid
- [x] `reap` prints `keeping` for a daemon this check started whose board directory still exists, and that pid is still alive afterwards
- [x] `reap` prints `keeping` for the machine's registered service while it watches a board on disk, and never stops it
- [x] `reap` finds a daemon whose argv is `run <board>` and not bare `run` — the shape `restart()` leaves behind
- [x] `reap --pid` refuses a value that is not a process id — `abc`, an empty string, `--`, `12x`, `0` — with a non-zero exit and no judgement printed about any daemon, so a `--pid "$VAR"` with `VAR` unset can never widen into the machine-wide sweep the flag exists to prevent
- [x] `python3 resources/pearde.py view reap --dry-run` reaches the same code and prints the same final line
- [x] `stranded()` judges a `/status` payload whose board entry carries a null `path` instead of raising `TypeError` — one malformed neighbour must not take the whole reap down, because a reaper that tracebacks reaps nothing at all
- [x] `references/parts/view.md` names `reap` among the verbs

## Verify and Proof

Run under `bash -e -o pipefail` — that is how `pearde collect` runs it
(`collect.py:1057`). `reap` is a machine-wide action, so every assertion below
is scoped to a pid this block started or to a board path it made; no line
counts `serve.py run` on the machine.

```sh
cd /Users/feb/dev/infra/pearde
python3 resources/pearde.py view reap --dry-run >/dev/null
grep -q 'reap' references/parts/view.md

T=$(mktemp -d /tmp/pearde-s02.XXXXXX)
S=/Users/feb/dev/infra/pearde/resources/board/serve.py
mkdir -p "$T/kept/.pearde/prds"
spare() { python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()'; }
PA=$(spare); PB=$(spare)
# A watches nothing — the fixture that died between `run` and its first
# `/register`, the case spec01's rules cannot reach. B is handed a board on
# its argv, the shape `restart()` leaves behind, and that board stays on disk.
# IDLE_EXIT_S is parked high so this block measures `reap` and not spec01.
PEARDE_IDLE_EXIT_S=9999 PEARDE_PORT="$PA" python3 "$S" run >"$T/a.log" 2>&1 &
A=$!
PEARDE_IDLE_EXIT_S=9999 PEARDE_PORT="$PB" python3 "$S" run "$T/kept/.pearde" >"$T/b.log" 2>&1 &
B=$!
trap 'kill -9 "$A" "$B" 2>/dev/null; rm -rf "$T"' EXIT
# poll rather than sleep: a fixed wait races the daemon's bind, and a check
# that reaps a daemon which has not yet registered proves nothing
up=0
for _ in $(seq 1 80); do
  if curl -fsS -m 1 "http://127.0.0.1:$PA/status" >/dev/null 2>&1 \
     && curl -fsS -m 1 "http://127.0.0.1:$PB/status" 2>/dev/null | grep -q '"kept"'; then
    up=1; break
  fi
  sleep 0.25
done
[ "$up" = 1 ]

# First at the shipped grace, and this is the assertion that matters most: A
# is seconds old and watches nothing, which is exactly the shape a
# `SessionStart` hook's `ensure` leaves behind between its bind and the
# board's first `/register`. `doctor.sh` ends every sweep with a reap, so the
# two meet on this machine routinely. Neither may be touched.
YOUNG="$(python3 "$S" reap --dry-run 2>&1)"
printf '%s\n' "$YOUNG"
printf '%s' "$YOUNG" | grep -q "keeping pid $A"
printf '%s' "$YOUNG" | grep -q "keeping pid $B"

# and now with the grace stood down, which is the only way to reach the
# stranded judgement itself on a daemon this block just started. `--pid`
# scopes it: a grace-less sweep over the whole process table would stop a
# neighbouring session's daemon inside the window the grace protects, which
# is the leak this PRD closes, manufactured by its own check.
DRY="$(PEARDE_REAP_GRACE_S=0 python3 "$S" reap --dry-run --pid "$A" --pid "$B" 2>&1)"
printf '%s\n' "$DRY"
printf '%s' "$DRY" | grep -q "would stop pid $A"
printf '%s' "$DRY" | grep -q "keeping pid $B"
printf '%s' "$DRY" | grep -qE '^serve: [0-9]+ of [0-9]+ stranded$'

# and a `--pid` it cannot read must REFUSE, not fall back to every daemon on
# the machine. An empty filter means "sweep everything", so a dropped bad
# value would turn `--pid "$VAR"` with VAR unset into the grace-less
# machine-wide sweep this flag exists to prevent.
for bad in abc "" -- 12x 0; do
  # an assignment inside `if` is the one form `set -e` does not abort on, and
  # a refusal exits non-zero by design
  if OUT="$(python3 "$S" reap --dry-run --pid "$bad" 2>&1)"; then RC=0; else RC=$?; fi
  echo "  --pid '$bad' -> exit $RC"
  [ "$RC" != 0 ]
  if printf '%s' "$OUT" | grep -q 'keeping pid\|would stop pid\|stopped pid'; then
    echo "reap --pid '$bad' judged a daemon instead of refusing"; false
  fi
done

PEARDE_REAP_GRACE_S=0 python3 "$S" reap --pid "$A" --pid "$B" >/dev/null 2>&1
sleep 2
STRANDED_GONE=1; kill -0 "$A" 2>/dev/null && STRANDED_GONE=0
KEPT_ALIVE=0;    kill -0 "$B" 2>/dev/null && KEPT_ALIVE=1
echo "stranded stopped=$STRANDED_GONE (pid $A) · live-board daemon kept=$KEPT_ALIVE (pid $B)"
[ "$STRANDED_GONE" = 1 ] && [ "$KEPT_ALIVE" = 1 ]
```

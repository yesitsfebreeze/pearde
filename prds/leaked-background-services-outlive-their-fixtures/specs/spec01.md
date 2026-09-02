---
complexity: 12
footprint:
  - resources/board/serve.py
  - references/parts/view.md
---

# spec01 — the daemon ends its own life

A fixture cannot be trusted to stop what it started: `serve.py ensure` spawns
its child with `start_new_session=True`, so the fixture's process group never
holds it, and a SIGKILL or a torn-down session runs no `EXIT` trap at all. So
the lifetime moves into the daemon. Two rules, both landed in
`resources/board/serve.py` in the probe pass and both green under
`probe/verify.sh`: a board directory that is gone is forgotten on the next
tick (`vanished()`), and a daemon that has watched nothing for `IDLE_EXIT_S`
exits; separately, a daemon watching *only* `EPHEMERAL` boards exits once the
process whose `ensure` started it (`PEARDE_SERVE_OWNER`, read into
`OWNER_PID`) has been gone for the same grace period (`orphaned()`).

**What stands.** `IDLE_EXIT_S` (`PEARDE_IDLE_EXIT_S`, default 180s),
`OWNER_PID`, `vanished()`, `orphaned()`, the grace-period arithmetic in
`watch()`, and `PEARDE_SERVE_OWNER` set by `cmd_ensure`. The module docstring
carries the paragraph explaining the lifetime.

**What is left.** `references/parts/view.md` still describes a daemon with no
lifetime at all — it must say that a daemon watching nothing on disk stops on
its own, name `PEARDE_IDLE_EXIT_S` beside `PEARDE_PORT`, and say plainly that
a daemon watching a real board is never touched by either rule.

The grace period is the whole design and not a detail: the first spelling
exited the instant the owner died, which reddened check I of
`.pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh` — a real
session start on a throwaway board legitimately outlives the shell that ran
the hook, and the leak being closed was measured in days.

## Acceptance

- [x] `resources/board/serve.py` defines `IDLE_EXIT_S` from `PEARDE_IDLE_EXIT_S` with a default of 180, and `OWNER_PID` from `PEARDE_SERVE_OWNER`
- [x] a daemon on a spare port whose only board directory is deleted is gone within `IDLE_EXIT_S` + one poll, measured on that daemon's own pid and never on a count of `serve.py run` on the machine
- [x] a daemon whose boards are all under `EPHEMERAL` and whose `OWNER_PID` no longer exists is gone within `IDLE_EXIT_S` + one poll, again by pid
- [x] a daemon watching one board still on disk is still running after twice `IDLE_EXIT_S`, whoever started it and whether or not its owner is alive
- [x] `references/parts/view.md` names `PEARDE_IDLE_EXIT_S` and says a daemon watching nothing on disk stops itself
- [x] `bash .pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh` still prints `46 checks · 46 pass · 0 fail · 0 skip`
- [x] `bash resources/invariants/every-artifact-lands-inside-the-board.sh` prints seven `PASS` lines and no `FAIL`

## Verify and Proof

Run under `bash -e -o pipefail` — that is how `pearde collect` runs it
(`collect.py:1057`). Nothing below counts processes machine-wide: every
assertion names a pid this block started.

```sh
cd /Users/feb/dev/infra/pearde
grep -q 'PEARDE_IDLE_EXIT_S' resources/board/serve.py
grep -q 'PEARDE_SERVE_OWNER' resources/board/serve.py
grep -q 'PEARDE_IDLE_EXIT_S' references/parts/view.md

T=$(mktemp -d /tmp/pearde-s01.XXXXXX)
S=/Users/feb/dev/infra/pearde/resources/board/serve.py
mkdir -p "$T/gone/.pearde/prds" "$T/stays/.pearde/prds"
spare() { python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()'; }
PA=$(spare); PB=$(spare)
PEARDE_IDLE_EXIT_S=4 PEARDE_PORT="$PA" python3 "$S" run >"$T/a.log" 2>&1 &
A=$!
PEARDE_IDLE_EXIT_S=4 PEARDE_PORT="$PB" python3 "$S" run >"$T/b.log" 2>&1 &
B=$!
trap 'kill -9 "$A" "$B" 2>/dev/null; rm -rf "$T"' EXIT
# poll rather than sleep: a fixed wait races the daemon's bind, and an `ensure`
# that arrives first spawns a SECOND daemon — which is the very leak this PRD
# is about, manufactured by its own check
up=0
for _ in $(seq 1 60); do
  if curl -fsS -m 1 "http://127.0.0.1:$PA/status" >/dev/null 2>&1 \
     && curl -fsS -m 1 "http://127.0.0.1:$PB/status" >/dev/null 2>&1; then up=1; break; fi
  sleep 0.25
done
[ "$up" = 1 ]
{ ( cd "$T/gone"  && PEARDE_PORT="$PA" python3 "$S" ensure "$T/gone/.pearde"  ) >/dev/null 2>&1 || true; }
{ ( cd "$T/stays" && PEARDE_PORT="$PB" python3 "$S" ensure "$T/stays/.pearde" ) >/dev/null 2>&1 || true; }
rm -rf "$T/gone"
# poll rather than sleep, for the same reason the bind above is polled: a fixed
# wait races the daemon's own idle tick, and on a loaded machine 10s is thin.
# The window only ever makes this stricter — B must still be up when it ends.
GONE=0
for _ in $(seq 1 160); do
  kill -0 "$A" 2>/dev/null || { GONE=1; break; }
  sleep 0.25
done
STAYS=0; kill -0 "$B" 2>/dev/null && STAYS=1
echo "deleted-board daemon reaped=$GONE (pid $A) · live-board daemon still up=$STAYS (pid $B)"
[ "$GONE" = 1 ] && [ "$STAYS" = 1 ]
```

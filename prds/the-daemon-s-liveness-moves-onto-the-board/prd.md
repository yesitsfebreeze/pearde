---
state: done
origin: requested
priority: 45
complexity: 18
blast-radius: mid
workflow: probe-then-spec
actual: 1.4h
commit: c456baa
---

# The daemon's liveness moves onto the board

*Source: `docs/content/docs/improvements/view-daemon-liveness.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** view · **Axis:** integration (5 → 7) · **Pulls the score up by
~6 points**

## Why now

The view daemon is registered nowhere the board owns: its port is an env
default, its pid sits in the process table, its liveness is judged by a
sweep (`serve.py reap`) that must distinguish a leak from a daemon a
`SessionStart` hook just brought up — which is why a grace window, a
`--pid` narrowing and a shipped grace constant all exist. Three safety rules
since are each the debt of one window: between `ensure` binding its port and
the board's first `/register`, the truth lives nowhere but the process
table.

## The change

The board's own directory learns the daemon: `serve.py ensure` writes
`.pearde/.state/view.json` — pid, port, started-at, the board it serves —
and a dead pid (checked through the process table, the one read `reap`
already does) means the file is stale, so the next `ensure` rewrites it.
`reap` keeps its sweep for the pre-rule daemons but treats a file-backed
daemon as *named*: no grace heuristics, no pid narrowing — a daemon with a
file is known, a daemon without is a candidate, same as today.

## Done when

- After `pearde view`, the board holds `.state/view.json` naming the pid and
  port `pearde view status` reports; deleting the board directory makes the
  next `status` say forgotten, as today.
- `reap --dry-run` never names a daemon whose file reads live.
- `doctor.sh --harnesses` ends with the same `reap` it runs today — the
  shipped grace kept — and the harness sweep passes unchanged.

## Fails when

- Two sessions on one board: both write the file, one pid wins. The writer
  takes the file only under the same lock the state writes take
  (@@pass), and a loser reads the winner's file rather than overwriting.

## What stays out

No change to the daemon's idle self-termination or the vanished-board
forgetting — those rules already end the right lives. This page only moves
*where the truth is kept*.

## Report

spec01: exit 0
== 1. ensure ==
serve: started on http://127.0.0.1:8543
serve: registered project · /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.pJul3bpZUy/project/.pearde · live view http://127.0.0.1:8543/board/project
PASS 1a ensure wrote .state/view.json
{
 "pid": 81960,
 "port": 8543,
 "started_at": "2026-09-03T18:57:48",
 "board": "project"
}
serve: up on http://127.0.0.1:8543 · pid 81960
  project          synced 0s ago · /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.pJul3bpZUy/project/.pearde
  all              synced never · None · master of 1: project
PASS 1b status names the same pid
PASS 1c status names the same port
PASS 1d a second ensure read the file, did not overwrite it
== 1. reap --dry-run (should keep, file-backed) ==
serve: keeping pid 81960 · port 8543 — named by project's .state/view.json — file-backed, no grace needed
serve: 0 of 1 stranded
PASS 1e kept
PASS 1f kept because of the file, not the grace
== 2. ensure, then delete the board ==
serve: started on http://127.0.0.1:8544
serve: registered project · /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bNDQsqAVgv/project/.pearde · live view http://127.0.0.1:8544/board/project
serve: would stop pid 83239 · port 8544 — watching no board
serve: 1 of 1 stranded
PASS 2a the pre-rule sweep still names it
PASS 2b and for the pre-rule reason
PASS 2c probe left no daemon behind
probe: 9 passed, 0 failed
serve: keeping pid 59189 · port 8443 — watching 1 live board(s): pearde
serve: keeping pid 79974 · port 64206 — started 22s ago — inside the 60s grace a session start needs to register its board
serve: 0 of 2 stranded
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk

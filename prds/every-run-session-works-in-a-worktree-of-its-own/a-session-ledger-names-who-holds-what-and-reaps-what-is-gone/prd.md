---
state: done
origin: requested
priority: 90
complexity: 29
blast-radius: high
workflow: probe-then-spec
actual: 2.75h
---

# a-session-ledger-names-who-holds-what-and-reaps-what-is-gone — pearde session take/list/reap/owns` stands: every run session gets a worktree of its own under the board, a ledger names who holds which and how to tell it is alive, and a reaper removes a dead session's tree only after stashing everything it left, untracked files included

pearde session take/list/reap/owns` stands: every run session gets a worktree of its own under the board, a ledger names who holds which and how to tell it is alive, and a reaper removes a dead session's tree only after stashing everything it left, untracked files included

## Report

spec01: exit 0
probe: a session ledger names who holds what and reaps what is gone — tree /Users/feb/dev/infra/pearde

== take — session A gets a worktree of its own
session s89222 · took /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/pearde-session-probe.npZJwn/repo/pearde/.sessions/s89222 · session/s89222
  ok   worktree at .sessions/s89222
  ok   ledger written
  ok   branch session/s89222 cut
  ok   the board is excluded from the session tree

== take is idempotent
  ok   a second take holds, not takes
  ok   one row, not two

== take — session B gets a different worktree
  ok   worktree at .sessions/s89223

== owns — each session owns its own tree and not the other's
  ok   A owns A
  ok   A does not own B
  ok   nobody owns the main checkout

== the work a dying session leaves

== reap — a LIVE session is never touched
  keep   s89222     this session
  keep   s89223     alive: pid 89223 running since Wed Sep  2 22:59:00 2026
reaped 0, 2 left on the ledger
  ok   B's tree survives while B is alive
  ok   B reported kept

== reap — a DEAD session's tree goes, its work first
  keep   s89222     this session
  reap   s89223     pid 89223 is gone
1 to reap — `pearde session reap --apply` does it
  ok   dry run removed nothing
  keep   s89222     this session
  reap   s89223     pid 89223 is gone · snapshot 374cd00e487c (4 files) at refs/pearde/reaped/s89223
reaped 1, 1 left on the ledger
  ok   dead session's tree removed
  ok   the live session's tree is untouched

== the snapshot holds everything, untracked included
  ok   snapshot ref exists
  ok   snapshot holds renamed.txt
  ok   snapshot holds new.txt
  ok   snapshot holds sub/deep.txt
  ok   the content of the edit is in the object store
  ok   the gitignored board stayed out of the snapshot

== the branch survives the reap
  ok   session/s89223 kept

== unknown liveness never reaps — a running pid whose start time is unrecorded
  keep   s89222     this session
  keep   sC         unknown: pid 89339 runs, and the row records no start time
reaped 0, 2 left on the ledger
  ok   a running pid with no recorded start time is kept, not reaped
  ok   its directory survives

== a reused pid reads as dead
  keep   s89222     alive: pid 89222 running since Wed Sep  2 22:59:00 2026
  reap   sC         pid 89222 was reused — started Wed Sep  2 22:59:00 2026, not Mon Jan  1 00:00:00 1990
1 to reap — `pearde session reap --apply` does it
  ok   a pid whose start time does not match is dead

== the running session's own tree is never reaped, whatever the ledger says
  keep   s89222     this session
  keep   sC         this session
reaped 0, 2 left on the ledger
  ok   a row this session holds is kept, dead ledger row and all
  ok   the running session's own tree survives

== the snapshot leaves the worktree byte-identical
  ok   the worktree is byte-identical across the snapshot
  ok   and the snapshot it took holds the untracked file

== list
* s89222     alive    pid 89222 running since Wed Sep  2 22:59:00 2026
    /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/pearde-session-probe.npZJwn/repo/pearde/.sessions/s89222
* sC         dead     pid 89222 was reused — started Wed Sep  2 22:59:00 2026, not Mon Jan  1 00:00:00 1990
    /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T//pearde-session-probe.npZJwn/repo/pearde/.sessions/sC

29 passed, 0 failed
PROBE GREEN
pearde session: takes take, list, reap, owns

spec02: exit 0
  index       broken  1 problem

spec03: exit 0
.gitignore:17:.sessions/	.sessions/
.gitignore:40:.state/sessions.json	.state/sessions.json

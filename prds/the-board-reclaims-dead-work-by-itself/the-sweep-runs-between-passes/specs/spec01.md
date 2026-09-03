---
complexity: 16
footprint:
  - resources/board/transitions.py
  - resources/board/serve.py
---

# spec01 — the view daemon ticks the sweep on its own, and only a confirmed-dead claim moves unattended

Between passes nothing ever calls `sweep`, so a ghost claim survives until
somebody happens to open one — the four ghosts of 2026-09-03 sat claimed for
42 minutes with `claim-ttl` long expired, because nothing was running to
notice. This unit picks the carrier and builds the safety the contract
requires before it may act with nobody watching.

**Carrier: the view daemon's own tick**, not a scheduled run.
`resources/board/serve.py`'s `watch()` loop already polls every watched
board every `POLL_S` (1s) for the life of the process, and that process is
already running wherever a pass or `pearde view` is — a scheduled run
(cron/launchd) would need a second, OS-specific, per-machine job installed
outside this Python-stdlib-only tree, with no board state or socket to
share with the daemon already up, and it would need its own idle-exit and
liveness story that `serve.py` has already paid for. Cost of the daemon
tick: one attribute per `Board` and one guarded call in a loop that already
runs.

**Only a confirmed-dead claim ever moves with nobody watching.** Running
the existing mtime rule (`silent_of`/`claim-ttl`) more often is a
regression, not a fix — a worker legitimately silent for `claim-ttl` while
thinking is now caught every time instead of by the luck of when a pass
next opened. `claim_liveness(who)` asks the one thing that already exists to
ask: `session.py`'s pid check, on a `who` shaped like its own `sid()`
(`s<pid>`). `pearde claim` writes a claim's `who` as a worker NAME today —
`a-claim-names-the-process-that-holds-it` is what gives it a resolvable
shape — so `claim_liveness` answers UNKNOWN for every claim on this board
right now, and `tick_sweep` leaves UNKNOWN and ALIVE exactly as `sweep`
without `--apply` would. It is wired and inert: the day a claim's `who`
resolves to a pid, this starts reclaiming the dead ones with no further
edit here, and until then it reclaims nothing that today's tree could not
already tell was dead by a stronger signal than mtime.

What already stands (built and probed in this pass, uncommitted in the
lane):

- `transitions.claim_liveness(who)` — `(verdict, why)`, `session.DEAD` only
  for a `who` matching `s<pid>` whose pid `ps` reports gone.
- `transitions.tick_sweep(board, out=print)` — every row `sweep_rows`
  already computes (so `prds/.pass.md` names and an analyzing PRD with
  specs on disk are already left alone, unchanged), reclaimed only where
  `claim_liveness` answers DEAD: the lane is committed
  (`lanes.commit_all`) before `drop_lane` removes the worktree, the
  `## Failure` section is appended naming the branch, and the state moves
  as `sweep --apply` would, `as sweep` on the progress line.
- `serve.py` `SWEEP_S` (`PEARDE_SWEEP_S`, default `0` — disabled) and
  `Board.last_sweep`: the watch loop calls `tick_sweep` on a board at most
  once every `SWEEP_S` seconds, wrapped so one board's exception is logged
  and never stops the loop watching the rest.

## Acceptance

- [ ] `claim_liveness("s<pid>")` for a pid that is gone answers `("dead", …)`; for a pid still running answers `("alive", …)`; for any `who` not shaped `s<digits>` — every claim `pearde claim` writes today — answers `("unknown", …)`
- [ ] `tick_sweep` reclaims a claim only when `claim_liveness` answers `"dead"`; a claim silent past `claim-ttl` naming a live pid, or naming no process at all, is left `claimed`/`analyzing` untouched
- [ ] a reclaim commits every uncommitted path standing in the lane to `lane/<rel>` (printed `… committed as <sha>`) before the worktree is removed, and the committed bytes are recoverable with `git show lane/<rel>:<path>` after the worktree is gone
- [ ] the reclaimed PRD's `## Failure` section names the kept branch, and the daemon's log line says `reclaiming without a pass`
- [ ] `SWEEP_S` defaults to `0`; with it unset or `0`, no watched board is ever ticked by `tick_sweep`, whatever the mtime and pid say
- [ ] with `PEARDE_SWEEP_S` set, `watch()` calls `tick_sweep` on each watched board at most once per `SWEEP_S` seconds, and an exception it raises for one board is printed to the daemon's log and does not stop the loop watching the others

## Verify and Proof

```sh
LANE="<the lane or checkout holding this unit's build>"
SKILL="$LANE" PEARDE_SWEEP_S=2 bash \
  /Users/feb/dev/infra/pearde/.pearde/prds/the-board-reclaims-dead-work-by-itself/the-sweep-runs-between-passes/probe/tick.sh
```

Run three times in a row: 7 checks, 7 pass, 0 fail each time — a dead pid's
claim reclaimed (lane committed, worktree gone, `## Failure` naming the
branch, log line `reclaiming without a pass`), a live pid's claim and a
claim naming no process both left `claimed`, silent past `claim-ttl` or not.

Regression: `bash /Users/feb/dev/infra/pearde/.pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh`
— 74 checks, 67 pass, 7 fail before and after this unit (same 7, unrelated
to `sweep`/`tick_sweep`: `add`'s template-comment box, three memory-log
boxes and one master-board box — all pre-existing, confirmed by running the
same harness with this unit's two files stashed out).

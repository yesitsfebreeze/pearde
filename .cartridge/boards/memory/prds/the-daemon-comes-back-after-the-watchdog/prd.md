---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the watchdog exits the process on a 30-second stall and nothing starts another — two daemons died inside seven minutes each, and every tool then answers `no daemon serving this directory`

## Do

`spawn_watchdog` (`src/commands/src/commands_serve.rs:454`, spawned from
`bootstrap` at `:172`) beats once a second, and six
missed checks — 30 seconds of no async progress — attempt a bounded flush and
then `std::process::exit(101)` (`:495`), "exiting anyway so a peer can take the
hub". There is no peer. Measured 2026-09-06 on this repo: two daemons started by hand
each died within about seven minutes, the second with

```
memory watchdog: async runtime stalled ~30s (graph deadlock or worker starvation)
 — guarded flush blocked past 5s, exiting anyway so a peer can take the hub
```

and every MCP tool answered `no daemon serving this directory — start it with
memory daemon` until a human started one again. The MCP adapter has no reconnect
and no retry: one exit ends the session's memory.

Two halves, and the second is the one that matters. The stall itself is real —
the same run logged `refused to flush a stale snapshot — disk advanced under us
(another writer)` twice against `.memory/data`, which is two daemons on one store
and a lock order worth reading before assuming worker starvation. And whatever
the cause, an exit needs a successor: the hub already supervises per machine
(`wire`), knows the root and can restart the node it adopted, which is what
"so a peer can take the hub" assumes and nothing implements.

Re-read 2026-09-07 against the split that moved the daemon out of `lib.rs`
([[the-commands-split-left-eight-anchors-past-the-end]]): the watchdog moved
whole, so every sentence above still holds — only the file it lives in changed,
and the anchor a runner follows is now the one in the first line.

Half landed 2026-09-07. `hand_the_hub_to_a_successor`
(`src/commands/src/commands_serve.rs`) runs on the watchdog's terminal path,
after the bounded flush and before `exit(101)`: it takes the listener clone
`run_server` published in `HANDOVER_FD` and hands it to
`identity::spawn_successor`, the same call the orderly hot reload makes at
`:402`, so the successor adopts the bound socket as fd 0 and no client sees it
go away. The watchdog thread is spawned in `bootstrap`, before a socket exists,
which is why the fd travels through a process-global slot rather than an
argument. Measured on a build whose beat task stops after two ticks: the stalled
daemon printed `guarded flush landed, handed the socket to a successor (watchdog
restart 1)` and exited; twenty-three seconds later `memory health` answered over
the socket with the daemon's own `tick:` and `degraded:` lines, no human
involved. `identity::RESTARTS_ENV` carries the count into the successor's
environment, so a daemon dying in a loop reads as a climbing restart number in
one inherited log.

Second half landed 2026-09-07, and the count now reaches the surface an agent
reads first. `HealthRes` carries `watchdog_restarts`
(`src/transport/src/memory_rpc.rs`), `#[serde(default)]` like every neighbour so
an older daemon reads 0; the daemon emits `identity::watchdog_restarts()` into
the health JSON beside `ingest_tombstoned` (`src/rpc/src/server.rs`), read from
its own environment because no graph and no store carries a generation number;
and `degradation_lines` (`src/commands/src/commands_admin.rs`) prints
`restarts:    N watchdog restarts — this daemon succeeded a stalled one` when
the daemon's count is nonzero. It is its own line and stays out of the degraded
sum, the shape `deleted:` already holds: a restart is the supervision working,
not a dropped row. Only a serving daemon can answer — the CLI's own environment
carries nothing — so the offline path prints no restart line at all.
`a_watchdog_restart_reaches_the_operator_and_stays_out_of_the_degraded_sum`
(`src/commands/src/tests/commands_admin_test.rs`) is the check, and it passes:
the count crosses the RPC boundary, prints, and does not move the degraded sum.

## Acceptance
Kill a daemon's runtime with a stall the watchdog fires on, and within a minute
`memory health` answers over the socket again without a human typing `memory
daemon`. The `degraded:` line counts the restart, so a daemon that dies in a
loop is visible instead of silent.

---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "2h"
---

# `ingest_intake_status::scan` lists only the intake's top level, so `direct/*.json` never counts as pending — `memory intake status` shows `pending=0` over a parked payload and `memory intake drain` returns "nothing pending" before it can reach `drain_locally`; make `scan` count `direct/`

Two paths drain the intake and only one of them can see `direct/`.

The daemon's loop calls `drain_once` (`src/ingest/src/ingest_intake.rs:329-357`)
every interval; it drains the top-level deltas, then calls
`ingest_direct::drain_direct_once(&intake_dir.join("direct"), ..)` at `:354`,
then prunes both `done/` dirs. `memory intake drain`
(`src/commands/src/commands_intake_cmd.rs:75-103`) reaches the same
`drain_once` through `intake::drain_now` (`:131`, via `drain_locally`) — but
only after `scan(dir, now)` at `:76` and the early return at `:81-84`:
`if before.pending.is_empty() { println!("nothing pending"); return; }`. That
return sits *before* `route("intake_drain")` at `:86`, so it fires whether or
not a daemon is up. And `scan` (`src/ingest/src/ingest_intake_status.rs:82-107`)
builds `pending` from `names_in(intake_dir)`, which is `read_dir` filtered to
`is_file()`: `direct/` is a directory, so its `*.json` are never listed.
Every direct payload is parked from inside the daemon — the MCP `ingest` tool
(`src/rpc/src/server.rs:1812`) and the file watcher sink
(`src/ingest/src/ingest_file_watcher.rs:88`) both call `intake_direct` — so a
payload parked, then the daemon stopped or crashed before its next pass, waits
for the next daemon boot and nothing else. Meanwhile `memory intake status`
prints `pending=0` over it, while the `ingest` tool's own miss text
(`server.rs:1793-1797`) tells the caller that same id "is an intake job still
waiting". The record already noted this as [[@prd/note/memory--open-work.md]] item 23; this memo
is its spec. [[the-intake-refuses-one-thing-permanently-and-retries-the-rest-forever]]
covers what the top-level drain does once it runs; this is the case where it
never starts.

Done 2026-09-08: `scan` (`src/ingest/src/ingest_intake_status.rs:82`) now
chains `direct/*.json` onto the top-level pending list as `direct/<file>`, so
`memory intake status` prints the parked payload and `memory intake drain` reaches
`drain_locally` instead of returning "nothing pending".

## Do

Fix the scanner, not the caller: `scan` is the one function both `status`
and `drain` read, and the early return at `commands_intake_cmd.rs:81` is
correct once `pending` tells the truth. In
`src/ingest/src/ingest_intake_status.rs::scan`, after the top-level `pending`
is built, extend it with `names_in(&intake_dir.join("direct"))` filtered to
`.json` (`.tmp` is `intake_direct`'s half-written file), each as a `Pending`
whose `name` is `direct/<file>` — the same relative path `metadata` and
`last_failure` already resolve against `intake_dir`, and `direct/done` is a
directory so `names_in`'s `is_file()` filter leaves it out. Nothing else
changes: `drain_locally`'s `.txt` test at `:116` does not match `direct/*.json`,
and the `ingest` tool's `scan(&direct_dir, ..)` at `server.rs:1815` still
counts the same files (a `direct/direct/` never exists). The alternative —
`drain` dropping the early return and always running one pass — leaves
`memory intake status` lying, so it is not taken.

## Acceptance
- `cargo test -p ingest ingest_intake_status` passes with a new case in
  `src/ingest/src/tests/ingest_intake_status_test.rs`: an intake dir holding
  `direct/abc.json`, `direct/x.123.tmp` and `direct/done/old.json` scans to
  `pending == ["direct/abc.json"]`, `stuck() == 0`.
- With the daemon stopped and one payload at `.memory/intake/direct/<id>.json`
  (park one through the `ingest` tool, then `memory stop`), `memory intake status`
  prints `pending=1` with a `wait direct/<id>.json` row, and
  `memory intake drain` prints `drained 1 of 1 pending`, not
  `intake .memory/intake: nothing pending`; the file is then under
  `.memory/intake/direct/done/`.

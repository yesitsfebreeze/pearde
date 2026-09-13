---

kind: work
level: 10
status: open
claim: session-adcf486f 2026-09-09 02:42
estimate: 1h
description: "`cmd_health` calls `load_graph` before it asks the daemon anything, so `memory health` pays a full store load — 85 s on the record — even when a daemon serving that store already holds every count it prints"
read_when: "timing a memory CLI call, or asking why health is slow against a warm daemon"
---

# memory-health-loads-its-own-graph-beside-the-daemon

`commands_health.rs` opens with `let g = load_graph(cfg);` and only then calls
`daemon_health()`. So `memory health` against a store a daemon is already
serving builds a second whole graph in the CLI process — 85 s on the record,
measured 2026-09-09 beside a warm daemon — to print counts the daemon holds in
RAM. The daemon's own lines (queues, presets, degradation) already come over
RPC; only the store stats take the slow road.

Found while checking
[[a-lane-daemon-pays-twelve-minutes-to-open-its-eyes]], whose Check names
`memory health` as the probe for a daemon being up and cannot distinguish the
daemon's 82 s boot from the CLI's own load. It is the same load
[[every-cli-invocation-pays-a-minute]] measured, here with a daemon standing
right next to it holding the answer.

## Do

When a daemon answers for this store, take the entity, memory and reason counts
from it over RPC and skip `load_graph`. No daemon serving keeps the current
in-process path — a read-only CLI on a store nobody serves has no other
source.

## Check

`memory health` against a served store answers in under a second and prints the
same memory, thought and reason counts as the in-process path on the same store;
against an unserved store it still answers with the counts.

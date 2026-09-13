---

kind: work
level: 10
status: done
description: "`map` answers 10,827,874 characters — about 2.7M tokens — an answer no agent can hold, so it costs every agent host a tool slot it can never spend; the row left `TOOLS` and the arm left the dispatch table with the clients"
read_when: "deciding what belongs on the tool surface"
---

# map-leaves-the-agent-surface

## Do

`map` is row 6 of `TOOLS` (`src/commands/src/commands_mcp.rs:28`). Called once
against this repo's store on 2026-09-06 it answered **10,827,874 characters** —
every hot thought with its coordinates and every reason edge. No agent can hold
that; the answer is two orders of magnitude past the largest context window,
and there is no argument that narrows it below the whole graph.

The reflex ledger, read the same day, held 470 `map` invocations of 506, every
one a client's 30-second poll and none drawn for evaluation; no agent turn
called it, so removing the row cost nothing.

Drop the `map` row from `TOOLS`; the dispatch test that invokes every tool name
reads the table, not this list.

Landed 2026-09-06: the row is gone. `tools/list` answered 23 tools with no
`map` among them — the 22 the probe counted gained `part` and `ask` in
6ac36992, so the 21 this Check predicted is 23 — and the dispatch test no
longer demands a 1:1 count: every tool is an arm, every arm is a tool. The arm
itself went on 2026-09-09 with the clients that polled it
([[memory-is-consumed-not-a-ui-host]]): `src/rpc/src/server.rs` has no `map`
operation, and the dispatch test names no exemption.

## Check

`tools/list` over `memory mcp` answers no `map`, `rg -n '"map"'
src/rpc/src/server.rs` returns nothing, and `cargo test -p commands` stays
green.

---
kind: work
level: 10
status: done
description: "`memory unnamed promote` writes the store locally and is undone by the daemon's next flush — it routes to the daemon like its graviton siblings"
read_when: "picking up the naming work"
---

# unnamed-promote-routes-to-the-daemon

## Do

`unnamed-promote-is-clobbered` names the defect: the `Promote` arm in
`src/commands/src/commands_unnamed.rs:36-86` embeds the seed, then writes the
store through `with_graph` (`load_graph` + `save_graph_unguarded`) while the
daemon holds the same graph in memory, so the daemon's next flush restores the
memory to unnamed and the command still prints success. `GravitonAction::Add`
and `::Remove` in the same file (`:712`, `:763`) already `route_to` the daemon
first; `Promote` takes the same shape, embedding client-side the way `Add`
does and sending the resolved memory id, name, vector and mass. A promotion that
cannot reach the daemon fails loudly rather than writing under it.

**The routing landed 2026-09-06.** `unnamed promote` routes before the embed
exactly like `graviton add`: `tool_graviton` gains a `promote` arm taking
`{id, name, text, mass}` (`src/rpc/src/server.rs`), resolving the short id
server-side, and `add` and `promote` now share one `embed_seed`. The CLI arm
(`src/commands/src/commands_admin.rs`) sends it and falls back to the local
write only on `NoDaemon`. Held by
`unnamed_promote_reaches_the_daemon_instead_of_the_callers_store` and
`unnamed_promote_still_writes_locally_with_no_daemon`
(`tests/e2e/focus_routing.rs`), which live beside the two graviton tests
they share their blinding with rather than in `cli_surface.rs`.

The item stays open on its `Check`, which the routing cannot satisfy alone:
the only memory `unnamed list` offers on a fresh store is the root, and a
promoted root never comes back from disk named
(`a-promoted-root-does-not-persist`).

## Check

An e2e test: against a running daemon, `unnamed promote` on a memory from
`unnamed list` leaves the memory named after the daemon's next flush.

**Check read 2026-09-07 and it is false.** `tests/e2e/focus_routing.rs` is
the only file that touches this path, and it holds two tests of it.
`unnamed_promote_reaches_the_daemon_instead_of_the_callers_store` starts a
daemon, promotes, then points the CLI at an empty `BLIND` data dir and asserts
`memory list` does **not** contain the new name — it proves the write left the
caller's store, which is the routing. `unnamed_promote_still_writes_locally_with_no_daemon`
proves the `NoDaemon` fallback. Neither asserts the other side: no test reads
the memory back named after the daemon's next flush, which is the whole clause.

The gap is not an oversight, it is the two questions below — a fresh e2e store
offers only the root to promote, and a promoted root does not come back from
disk named (`a-promoted-root-does-not-persist`). Until one of them is answered
there is nothing to assert against, so this part was open correctly and its
next move was the drill, not the test file ([[the-eight-unread-work-checks]]).

**Drilled 2026-09-07; the surface half landed, the flush half split out.** Q2
answered no: `unnamed list` drops the root (`k.id != g.root.id` in the `List`
arm of `src/commands/src/commands_admin.rs`), so the listing names only what a
promotion can hold. Held by `unnamed_list_does_not_offer_the_root`, and the two
routing tests now name the root by its literal id instead of reading it back
out of a listing that no longer offers it
(`tests/e2e/focus_routing.rs`). Q1 answered: no CLI handle reaches the one site
that mints an unnamed child, so the flush half stays unmeasurable — it waits on
a `memory pulse` subcommand, which is its own item and not written here. The item
stays open on that.

`subwork:` [[@prd/work/memory--pulse-is-a-subcommand.md]] — that handle, written and landed
2026-09-07: `memory pulse` routes a clustering pass to the daemon's tick queue.

**Done 2026-09-07: the flush half is measured and green.** With the pulse in
hand the residual risk — that no CLI-reachable fact splits — is answered: the
splittable fixture is the `generic` catch-all itself. It is named, so
`select_spawn_clusters` will spawn from it, and its `focus_vec` is empty, so
`is_core_cluster` never holds a cluster back; twelve facts sharing an
eight-word stem sit at cosine ~0.8 under the fake embedder, above
`MEMORY_COHESION_THRESHOLD` (0.60) and below `INGEST_DEDUP_THRESHOLD` (0.95), so
they survive ingest as twelve entities and cluster as one. `memory pulse` on a
daemon with `tick.interval_secs = 0` splits them into an unnamed child, the
child stays unnamed because the fake chat echoes the naming prompt and
`is_name_shaped` refuses a document, and the promotion of that child is still
there after a second routed write flushes the daemon's whole graph. Held by
`a_promoted_child_survives_the_daemons_next_flush` (`tests/e2e/focus_routing.rs`).
`memory list` prints every thought's text under its memory, so the read-back names
the memory `dockwork` — a word no fact says — and asserts the label `memory:dockwork`
absent before the promotion and present after, which makes the same expression
the control and the measurement.

----
Q: What makes a genuine unnamed child memory in an e2e store, so the flush half
can be measured at all? Three and then eight varied facts, with and without a
graviton present, all landed in `generic`, and there is no `pulse` subcommand
on the CLI to force a clustering pass.
A: Nothing the CLI can reach, so the fixture is not this item's to invent.
One site mints an unnamed child — `spawn_child_clusters`
(`src/tick_loop/src/tick.rs:339`) inside the daemon's `Cluster` task, enqueued
by `tick_pulse::pulse` on the daemon's own tick
(`src/commands/src/commands_serve.rs:719`). The only handle on that pass is the
MCP `pulse` tool (`src/commands/src/commands_mcp.rs:62`); the CLI's subcommand
list (`src/commands/src/lib.rs:162-664`) has no `pulse`, so a test driving the
CLI cannot force one, and waiting on the tick needs facts that cluster — the
ones measured all land in `generic` and split nothing. Splitting out: a
`memory pulse` subcommand is its own level-10 item, and the flush half of this
Check waits on it.

----
Q: Is promoting the root a thing the command should offer? `unnamed list`
prints it because `is_unnamed` reads an empty `graviton_text`, and the promote
succeeds and vanishes. Refusing the root would make the surface honest without
answering the persistence question behind it.
A: No — `unnamed list` stops offering it. One predicate, `k.id != g.root.id`
in the `List` arm (`src/commands/src/commands_unnamed.rs:19-24`): the listing
names only what a promotion can hold. `promote` itself still takes an explicit
`root` id, which is deliberate — it is the only probe the two routing tests
have, and refusing it belongs with the fix for why it evaporates
([[the-root-memory-exists-twice]]), not with the listing.

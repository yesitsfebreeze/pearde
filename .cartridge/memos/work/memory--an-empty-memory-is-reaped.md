---
kind: work
level: 10
status: done
description: 21 of the store's 50 memories hold nothing after a bulk removal, and `gc` — whose contract is a live reap of empty and orphan memories — leaves them
read_when: "reading health, or after a bulk forget"
---

# an-empty-memory-is-reaped

## Do

Measured 2026-09-06 after the bulk cleanup: 21 empty unnamed memories out of 50.
The `gc` operation is documented as "Live reap of empty and orphan memories"
(`src/commands/src/commands_mcp.rs:64`) and this is exactly its case, so either
it does not run without a caller asking, or its emptiness test does not match a
memory emptied by removal rather than never filled. Find which before changing
anything.

An empty memory is not free: `health` lists every one of them, which is the
surface an agent reads first, and the naming pass keeps them as `[unnamed]`
candidates forever. The store also carries names written before the bound
([[@prd/work/memory--rename-the-memories-named-before-the-bound.md]]) — the two passes are neighbours
and should not be one part.

**Done 2026-09-06, and it was the first option.** The reap does run — at daemon
start (`reap_empty_memories`, `src/commands/src/commands_serve.rs:81`, called at
`:174`) and again in the bloat self-heal (`maybe_self_heal_store`, `:32`),
printing `reaped 5 empty memories (36 -> 31)` on a restart the same night. Nothing reaps between starts, so the 21 empties were made by the bulk
removal minutes after a boot and waited for the next one.
`tool_forget_by_source` now reaps after a removal that took anything and
answers `reaped_memories`; the no-daemon path does the same.

**The Check was narrowed, deliberately.** "No memory with zero thoughts and zero
reasons" would reap a *named* empty memory, and a named empty memory is a declared
attractor — `graviton add docs <seed>` creates exactly one, holding nothing
until placement fills it. Satisfying the Check literally would delete a
curator's graviton. The rule kept is the one `gc_empty_memories` already encodes:
unnamed and empty is residue, named and empty is a declaration.

One ordering worth marking, because nothing else does. `gc_empty_memories` tests
`entities.is_empty()` and ignores `reasons`, so a memory holding no thoughts and
837 edges — `health` showed one — is reaped with those edges. That is correct
only now that removal cascades across memories
(`an-edge-lives-in-one-memory-so-removal-scans-them-all`); before that landed,
the same reap was a silent edge-deletion path, and it had been one for as long
as the liveness test existed. The fix that made the reap safe landed after the
reap did.

## Check

After a bulk `forget` that empties an unnamed memory, the memory is gone rather
than left for the next daemon start, and a named memory holding nothing survives.
Held by `a_bulk_forget_reaps_the_memories_it_empties_and_keeps_the_named_one`
(`src/rpc/src/tests/server_mutate_test.rs`), with
`a_routed_forget_by_source_mutates_the_serving_daemons_graph` updated to assert
the emptied memory is gone rather than empty; the suite read 1,234 passed.

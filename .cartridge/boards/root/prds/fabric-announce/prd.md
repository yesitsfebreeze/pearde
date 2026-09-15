---
repo: /Users/feb/dev/cartridge
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
---

# Invert fabric composition from memo scraping the host to core firing an announce event every active cartridge answers, and serve the resulting graph to any cartridge

## Outcome

The graph is built from what the active composition announces about itself, not
from one cartridge reaching out and scraping the others, and any cartridge can
ask for it.

Core fires one announce event; every cartridge that has something to contribute
answers with its nodes and edges; core folds the answers into one graph and
serves it on the wire. Which cartridges are loaded is therefore what the graph
is — an entry that is not loaded is not asked, and one that is loaded
contributes without core knowing what it is.

[[the-fabric-owns-the-graph]] already settled that there is no fabric tool and
no fabric process. What changed here is the direction of collection, who can
reach the result, and — in the same pass — where the code lives at all: the
separate library is gone, absorbed per [[the-fabric-lives-in-core]].

### Scope boundaries

- The graph stays derived state, rebuilt per ask, with no durable copy.
- `tool.memo`'s operation keeps its response shape. It became a client of the
  announce-built graph instead of its builder.

## Context

Composition was a pull: memo asked the host for the snapshot, looped every
`tool.*` key **it** injected calling `{"op":"describe"}`, surveyed the record,
and composed the three lists itself. Three consequences: only cartridges memo
injected could contribute; only the three kinds that loop knew about existed;
and only memo could reach the graph, because only memo built it.

Core already had the event wire, including the reply path — a Lua listener
returns a value and a process cartridge's `on` handler reply travels back over
the wire. What was missing was a dispatch that keeps those replies: `emit`
discards them, `bail` takes the first, `parallel` keeps only errors.

This is the first concrete event of [event-fabric](../event-fabric/prd.md) and a deliberate pilot for
it: request/reply shaped, so it exercises envelope and provenance without the
memory-addressing design having to be settled first.

## Approach

1. **`Ctx::gather`** — `cartridge.ctg/src/runtime.rs`, beside `bail` and
   `parallel`: run every listener, keep every non-null answer with the `Uid` of
   the fiber that gave it. A listener that fails fails its own fiber, as `emit`
   does, so one cartridge that cannot answer never costs the caller the rest of
   the composition's answers. Exposed to Lua as `ctx:gather(name, payload)`,
   returning `{from = <entry id>, data = <answer>}` rows.

2. **The announce** — `fabric.announce`, fired by `Host::graph(scope)` in
   `cartridge.ctg/src/fabric.rs`. An answer is `{"nodes":[…],"edges":[…]}`
   in the shapes `src/graph.rs` reads. `Node.kind` is a free string, so a cartridge
   announces kinds nobody enumerated. `scope` is the asking side's context,
   passed to every contributor, since core has no session of its own.

3. **Core folds and serves** — core states the entries and their
   `provide`/`inject` edges itself, then folds the answers on top in entry-id
   order so the winner between two contributors is the same on every call. Each
   node carries `from`: the registry's name for the answering fiber, stamped by
   the host and never read out of the answer; core's own rows carry `from:
   null`. `{"graph": scope}` on the wire, `sdk::Host::graph` in the SDK,
   forwarded by nested sub-hosts like every other host verb.

4. **The SDK answers for every cartridge** — `Host::announcement` reports the
   tools this cartridge provides, as each describes itself, read from its own
   service handlers in process. No injection, no cross-process describe loop,
   and no edit in the tool cartridges: `docs`, `fs`, `gitfs`, `memory` and
   `pty` announce their tools without a line changed in any of them.
   `Host::announce(f)` adds what only that cartridge knows.

5. **Memo became a client** — its `descriptors()` scrape is deleted. It
   announces the record through its own `graph::record` and reads the announced
   graph back through `cartridge::fabric::graph::grown`; ranking and the journal
   counts are unchanged. `prd` speaks the wire directly and announces
   `tool.prd` in the same shape.

## Acceptance
- [x] `Ctx::gather` keeps every non-null answer attributed to its fiber; a
      silent listener contributes nothing and a failing one fails only itself.
      Evidence: `tests::lifecycle::gather_keeps_every_answer_with_its_fiber`.
- [x] Core fires `fabric.announce` and folds the answers into a graph whose
      nodes carry the answering entry's id, taken from the registry — a node
      that signs itself as another cartridge is corrected. A malformed row is
      dropped rather than failing the graph, and the scope reaches contributors.
      Evidence: `tests::fabric::the_graph_is_what_the_composition_announces`.
- [x] A cartridge that registered no announce listener still contributes the
      tools it provides, and its hook's own nodes arrive with them.
      Evidence: `tests::fabric::a_cartridge_announces_the_tools_it_provides`
      over the real process wire, with `tool_fixture` as the peer.
- [x] A cartridge that is not composed contributes nothing; disposing one
      removes its contribution from the next ask. Evidence: same two tests.
- [x] `grown` ranks every kind the composition contributed, and `record` is the
      memo record's own contribution. Evidence: `graph::tests` in `memo.ctg`
      (`the_announced_graph_ranks_every_kind_the_composition_contributed`,
      `malformed_contributions_are_dropped_not_grown`,
      `composed_memo_links_respect_cartridge_namespaces`).
- [x] `tool.memo`'s `fabric` op serves the announce-built graph with its
      response shape unchanged, and no longer loops `describe` itself.
      Evidence: `cargo test -p memo_cartridge` — 84 passed; memo's
      `inventory.test.ts` integration suite — 3 passed, its fake host now
      answering the `graph` frame and no longer asked for `injections`.
- [x] `prd` announces its tool over the raw wire. Evidence:
      `prd.ctg/.cartridge/tests/service.test.ts` — 11 passed.
- [x] End to end on the real binaries, one composition, no fake host:
      `cartridge --dir <profile> run memo '{"op":"graph","cwd":…}'` returns
      `tool.docs` (`from: docs`) and `tool.memo` (`from: memo`) beside six
      cartridge rows with `from: null` and 18 record memos announced by memo,
      including the `@docs/…` memos docs ships. `docs.ctg` was not edited for
      this. With a `query`, the same op ranks that graph and names what each hit
      connects to.

## Result

Delivered. The pull is gone: nothing scrapes anything, one path builds the
graph, and a cartridge reaches it with `sdk::Host::graph`.

Two things a later pass should know.

The digests pinning `prd.ctg/src/service.ts` were revalidated in `memo.ctg`'s
`sources/search.rs` and `sources/census.rs` fixtures and in its
`source-search.test.ts`, since announcing changed that file. The
board evidence records under `prd.ctg/.cartridge/boards` still name the older
revision; they are historical proof of what was true then and were left alone.

This work landed while another session was refactoring `cartridge.ctg`'s
constants into a new `src/settings.rs` and restructuring the submodule tree.
Unrelated failures observed in that tree at the time, each reproduced with
every change of this memo's reverted: six core unit tests asserting queue
bounds, size caps and deadlines that moved into settings
(`stream::a_full_replay_and_gap_leave_the_subscription_live`,
`stream::history_is_bounded_and_an_old_cursor_receives_a_gap`,
`sdk::tests::slow_stream_handlers_have_bounded_queues_and_receive_a_gap`,
`observation::tests::actual_descriptor_shapes_are_hashed…`,
`process::a_child_that_stays_alive_without_ready_times_out_and_is_reaped`,
`wire::stdout_closed_live_children_obey_each_host_deadline_and_are_reaped`);
`stream::a_slow_subscriber_gets_a_gap_and_closes_without_blocking_publishers`,
which hangs rather than fails, since a subscriber bounded by settings no longer
overflows; and eleven tests that came across with the absorbed library and now
fail inside `memo`, all from the same unfinished migration — the source budgets
now read `cartridge.json`'s declaration through `Budget::declared()` instead of
a Rust `Default`, and the in-code range checks those tests assert
(`(4096..=MIB).contains(&max_search_bytes)`, `(1..=2000).contains(&deadline_ms)`)
were deleted in favour of declared bounds. The saved diff at
`landscape-preremame.diff` shows both changes. Two of the eleven,
`sources::census::tests::actual_native_prd_callback…` and
`sources::search::tests::actual_native_owner_search…`, fail for a different
reason: `cartridge run` of a cartridge with a dependency exits 1 with no output
in that tree — the same failure a plain `memo` `index` call shows with `fs`
composed, and one that reproduces with every change of this memo reverted.

Unresolved prerequisites at migration: `[[the-fabric-owns-the-graph]]`.

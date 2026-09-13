---
kind: work
level: 10
status: done
description: four `pub fn`s are referenced nowhere but their own definition — the tree's no-uncalled-export law names them for deletion
read_when: "picking up work, or running the duplication probe"
---

# four-exported-functions-have-no-caller

## Do

A scan of every `.rs` file under `src/` and `tests/` for
each of the 583 `pub fn` names found six whose name occurs only at its own
definition. Two of them, `Client::for_eval` and `Client::with_temperature`, are
not dead code but an unreached knob and are held by
[[nothing-seeds-the-completion-client]]. Delete the other four:

- `MemoryRpcClient::connect_local` (`src/transport/src/memory_rpc.rs:24`) — a
  one-line wrapper over `connect_endpoint(&Endpoint::memory())`; every caller
  builds the endpoint itself.
- `GraphGnn::observe_lamport` (`src/graph/src/graph.rs:712`) — the receiving
  half of a Lamport clock. `bump_lamport` above it is called; nothing observes
  a remote counter, because network federation was removed 2026-08-16 and there
  is no remote writer ([[recall-pipeline]]).
- `rpc::test_helpers::server_with_config` (`src/rpc/src/test_helpers.rs`, at
  line 47 before the deletion shortened the file) —
  a rig variant no test takes.
- `test_support::tool_text` (`src/test_support/src/lib.rs:53`) — a
  `content[0].text` extractor no test takes.

`LinearLayer::new` (`src/gnn/src/gnn.rs:97`) and `GCNLayer::new` (`:224`) are
two more, found separately ([[the-gnn-is-deterministic-per-corpus]]) and worth
deleting in the same change — they are the crate's last unseeded `rand::rng()`
sites. They were missed by the scan above, which is its known limit: a name as
common as `new` occurs everywhere, so the occurs-only-at-its-definition test
cannot see it. The scan finds uniquely-named exports and nothing else.

[[SYSTEM]]'s frontier law is the whole reason: no code without a caller, an
exported function nothing calls is deleted. Git holds them.

## Check

Each of the four names returns nothing from `rg -w <name> src tests`,
and `just check` and `just test` are green.

**Done 2026-09-06.** All six deleted, each re-verified uncalled with the
word-boundary form before removal rather than on this part's scan. `rg -w`
answers 0 for `connect_local`, `observe_lamport`, `server_with_config` and
`tool_text`; `LinearLayer::new` and `GCNLayer::new` are gone with them. No
unused-import fallout — `Endpoint` still serves `connect_endpoint` in the same
file.

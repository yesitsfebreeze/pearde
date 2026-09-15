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

# `tool_setup` calls `graph_health_stats`, which collects every resident entity's access count into a `Vec` and sorts it for a Gini — and uses three cheap fields from the result, discarding the number that cost the pass

This completed work is historical. The 2026-09-10 memory-engine-and-CLI scope
removed the setup operation and its host wiring instructions; see [[vision]].

## Do

`setup` is the tool an agent host calls to get "idempotent wiring instructions"
(`commands_mcp.rs:67`), and it is the first thing a session invokes. Its body
(the former setup implementation in `src/rpc/src/server.rs`, before `ced70eb8`) takes the graph read lock and calls
`::health::graph_health_stats(&g)` for exactly three values: `h.gravitons`,
`h.entities`, and `g.root.claim_kinds.len()` — which it does not take from the
stats at all.

`graph_health_stats` does considerably more than count.
`src/health/src/lib.rs:136-142` builds `access_counts: Vec<u64>` from
`g.all().flat_map(|k| k.entities.values().map(|e| e.access_count.value()))` —
one `u64` per resident entity, 49,635 of them on this store — and hands it to
`gini_over_access`, which sorts it. [gini-answers-in-one-sort](../gini-answers-in-one-sort/prd.md) is what made
that one sort rather than the N² pass [[health-is-quadratic-in-entity-count]]
measured; it is still an allocation and a sort of the whole store, under a read
guard, and `setup` reads none of it.

The two fields it does use are sums the same function already computes on the
way past: `entities` accumulates `k.entities.len()` in the loop at `:123-125`,
and `gravitons` is `root_graviton_ids` mapped over loaded children (`:130-133`),
which touches the root's direct children only
([[the-graviton-list-is-the-roots-children-only]]).

Give `setup` those directly rather than the whole stats pass — a count of
entities, the graviton names, and the claim-kind count it already reads off the
root. `health` keeps `graph_health_stats` unchanged; it is the caller that
wants three numbers, not the function that is wrong to compute the rest.

## Acceptance
`setup` no longer calls `graph_health_stats`; its answer is unchanged field for
field against a store with more than one memory; and `just all` is green.

Landed in `tool_setup` (`src/rpc/src/server.rs`, lane `herd-drive-p3-3`,
commit `ced70eb8`): the call is gone; `focuses` is `root_focus_ids` mapped
through `g.loaded(..).focus_text` and `thoughts` is the entity-count sum over
`g.all()`. HEAD names the field `focuses`, not `gravitons`. A throwaway test on
a two-memory, two-focus store with one claim kind compared the rendered
instructions against `render_setup` fed from `graph_health_stats` and found
them identical; the three `server_setup_tests` pass. `just all` runs at land.

---
kind: work
level: 10
status: done
read_when: "asking whether every add_reason site registers its edge"
description: "Landed `1191a75a`: four registrations, in the spelling each site's neighbours already use, and `tests/reason_ownership.r..."
sources:
  - four-production-sites-mint-an-edge-nothing-can-find
---

# four production sites mint an edge nothing can find

Landed `1191a75a`: four registrations, in the spelling each site's neighbours already use, and `tests/reason_ownership.rs` so it cannot drift back — it walks `src/`, skips a test module however its `cfg` is spelled, and fails on an `add_reason` with no registration in its own block. Nine production sites, every one registered; the two that leave the index to someone else are named in the gate with their reason rather than exempted by shape. The two tick sites register only where the edge actually landed, because an index entry for a memory that does not hold the reason sends `find_reason` somewhere worse than nowhere. `a_linked_edge_is_findable_without_a_scan` holds the sharpest case: after `link_entities`, `memory_of_reason` answers the memory that holds it.

[[the-reason-ownership-index-is-partial]] counts the ratio — 5 of 13 sites register — and [[move-entity-is-the-written-form-of-the-index-discipline]] says what registering means. This is the audit that names the gap, run 2026-09-06 over every `add_reason` call outside `/tests/`, accepting **both** spellings a site may use: `g.index_reason(rid, memory)` and a direct `self.reason_memory.insert(rid, memory)`.

Fourteen sites. Four register through `index_reason` — `commit_reason`, `stamp_superseded`, `move_entity`, `do_resolve`. One registers by direct insert and would have been a false flag on the narrower search: `gc_empty_memories` (`graph.rs:957-959`), the rehoming `08b30e2a` added hours earlier. Two are test fixtures (`commands_route.rs:103-104` inside `mod tests` at `:90`, and `server.rs:1021`). Two are already recorded — `absorb_graph` ([[an-absorb-fills-some-indexes-and-not-others]]) and `rekey_memory`, whose caller rebuilds separately.

The four that remain mint an edge and register nothing:

| site | what it mints |
|---|---|
| `graph_ops.rs:279` `link_entities` | the `link` operation's edge — an agent-facing tool that returns the id it just made unfindable |
| `accept.rs:463` `merge_duplicate` | the Rephrase edge on every dedup, so this is the write path |
| `tick_tasks.rs:127` `do_seed_questions` | Question edges from the tick |
| `tick_tasks.rs:308` `do_name` | the spawn edge on a naming pass |

The cost is the one that part already states and this makes concrete: `memory_of_reason` cannot name these edges, so `find_reason` pays a full scan across every memory to locate one, and `seed_by_reason` drops a hit it cannot resolve without a word. An edge made by `link` is the sharpest case — a caller is handed `edge_id` for a row the index does not know.

Add the registration at each of the four, in whichever spelling the surrounding code already uses. All four hold the graph — two as `&mut GraphGnn`, two as `&Arc<RwLock<GraphGnn>>` — so this is four lines and not a refactor ([[the-signature-is-not-what-stops-the-ownership-write]]).

## Check

Every production `add_reason` call is followed by `index_reason` or a direct `reason_memory` insert for the same id — the audit above re-run answers zero unregistered sites outside `/tests/` — and `find_reason` locates a freshly-`link`ed edge without scanning; `just all` green.

---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
needs:
- "@memory/behaviour-is-a-space-field"
---

# a graviton is declared by a part — its leaf name the handle, its text and mass in a `toml` block — so focus attractors are reviewable in the record instead of typed once into a socket

**Needs [behaviour-is-a-space-field](../behaviour-is-a-space-field/prd.md)** and nothing else: the payload shape
is settled — `name` retires for the leaf name, and the attractor text and
optional `mass` ride in the part's first fenced `toml` block
([[a-declaration-carries-its-payload-in-a-toml-block]]).

## Do

A part declares a graviton: its leaf name is the handle, the attractor text
and optional `mass` its `toml` block. The
store loads declared gravitons from the graph; the `graviton` operation keeps
its list/add/remove arms for a caller with no record.

Landed. `register_declared_graviton` (`src/ingest/src/ingest_worker.rs`) is the
analogue of `register_declared_kind`: on every offer of a `kind: focus` part
it reads the block, embeds the seed lines through the worker's own embedder,
mean-pools them and calls `add_graviton_with_mass` under the part's leaf name.
`graviton {action: list}` needed no edit — it already read `graviton_rows` off
the graph, so a registered part is a listed attractor. `system/focus.md`
declares the kind and `memos/focus/` carries three: [[decisions]],
[[mechanism]] and [[practice]].

The payload reader is one function, not two: `toml_block` lives in
`src/ingest/src/ingest_worker.rs`, which `rpc` already depends on, so every
registry reads a declaration's block through the same three lines.

## Acceptance
`just test` green, plus: a store whose record declares a graviton lists it
through `graviton {action: list}` with no add call, and placement uses it.

`a_declared_graviton_part_becomes_an_attractor_with_its_mass`
(`src/ingest/src/tests/ingest_file_watcher_test.rs`) offers a `kind: focus`
part carrying `mass = 2.5` and reads the attractor back out of
`graph_ops::graviton_rows` — the rows `graviton {action: list}` answers with —
under the leaf name, with no add call anywhere in the test.

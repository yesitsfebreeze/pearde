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

# `ingest` accepts `user_id`, `agent_id` and `session_id`, every entity persists them, the filter reads them — and no query surface has ever filled the filter, so the fields are the caller identity [[no-per-row-acl]] says was removed wholesale

## Do

The `Scoping` struct (`src/base/src/base_types.rs:323`) carries three
`Option<String>`s. Measured 2026-09-06, working tree and `HEAD` agreeing:

- **Written.** The daemon's ingest arm (`src/rpc/src/server.rs:1575-1579`)
  deserializes the three from the request, builds a `Scoping`
  (`:1681-1685`), and `ingest_place.rs:91-93` copies it onto every entity.
  The `ingest` tool (`src/commands/src/commands_mcp.rs:36`) advertises all
  three as string properties.
- **Persisted.** `Entity.user_id`/`agent_id`/`session_id`
  (`base_types.rs:361-363`) are bincode fields since format v8 — commit
  `5ee8e448`, 2026-07-23 — and `legacy.rs:82-83,135-136` carries them through
  the one-hop migration.
- **Read by nothing.** `QueryOptions` has the three filters
  (`retrieval_score.rs:57-59`) and `passes_filters` tests them
  (`:283-296`), but every construction of `QueryOptions` in the tree —
  `build_query_options` (`server.rs:353`), the report arm (`:1317`),
  `commands_query.rs:90`, `commands_graph_ops.rs:192` — leaves them at
  `..Default::default()`. `git log -S'opts.user_id'` finds one commit: the
  one that added the check. The commit that promised "filterable user
  dimension" wired the ingest side only; the query side never existed.

So a caller can stamp an identity on a row and can never ask for it back.
That is not a half-built feature: [[no-per-row-acl]] landed as `80ce7a93` on 2026-07-22, one day
before `5ee8e448`, settling that memory carries "no user scoping, no caller identity",
and its consequence line says such guards are "deleted, not kept dead". The
`Acl` field went; the trio it would have keyed on stayed, and
`60157404` — the commit [[one-deletion-commit-left-four-residues]] audits —
touched `server.rs` around it and left it. This is a fifth residue, and
[[an-empty-source-field-reads-as-no-constraint]] describes exactly its
reading: three fields that are `None` on every row ever written, so every
consumer treats them as "unconstrained".

Delete it, as the decision instructs: `Scoping` and its three `Entity`
fields, the three `QueryOptions` fields and their `passes_filters` and
`is_active` branches, the three properties on the `ingest` tool schema, the
three request fields and the `Scoping` construction in the ingest arm, the
`scoping` parameters threaded through `ingest_direct.rs`, `ingest_worker.rs`,
`ingest_place.rs`, `ingest_file_watcher.rs` and `tick_tasks.rs:204`. Removing
three positional bincode fields from `Entity` is a persisted-layout change:
move `FORMAT_VERSION` (`src/store_core/src/lib.rs`) to 14 — `Entity.space`
took 13 after this part was written — keep v13 readable in `legacy.rs` by
consuming the three slots and throwing them away, and pin the new layout in
the layout guard ([[format-version]],
[the-layout-guard-misses-the-two-meta-rows](../the-layout-guard-misses-the-two-meta-rows/prd.md)). Nothing under `tests/` names
any of the three, so no e2e moves.

If instead a host wants the filter — one memory per trust domain is the
decision's answer, and re-adding a query-side `user_id` is the "re-litigating
every read surface" the decision forbids. Wiring the read side is not an
option this part offers.

## Acceptance
`rg -n 'user_id|agent_id|Scoping' src` answers only `store_core`'s frozen
v13 snapshot and its test mirror, which is what keeping v13 readable means;
`rg -n 'session_id' src` answers only `Source::Session`; `just check` and
`cargo test --workspace` green, the layout guard among them; a v13 store
opened by the new binary loads with every entity and every edge it had.

Landed 2026-09-07. `FORMAT_VERSION` is 14, `legacy::EntityV13` carries the
three dropped slots as one unread tuple so every field after them still lands
where it was written, and `legacy_test` decodes v13 bytes to prove it.

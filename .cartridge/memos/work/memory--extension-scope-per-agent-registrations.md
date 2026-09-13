---
kind: work
level: 10
status: done
estimate: 4h
needs: ["@prd/work/memory--extension-events-four-dispatch-modes.md"]
description: a minted scope tags a context so registrations through it are scope-visible and scope-lifetime, events route up the parent chain, and `ScopedLayers` merges registry layers nearest-first
read_when: "isolating registrations per agent or per group, or building a registry on the compose crate"
---

# extension-scope-per-agent-registrations

## Do

Build `extension::scope`:

- `ScopeKey = u64` minted by `Scope::key()`. `Scope::mint(ctx, key, parent: Option<ScopeKey>) -> Scope { ctx, fiber }`
  mounts a no-op plugin and derives its context with the tag; `scope.dispose().await`
  unwinds every registration made through `scope.ctx` (it is the fiber's
  disposal); `scope_of(ctx) -> Option<ScopeKey>`.
- Parent chain: `bind_scope_parent(key, parent)` once, cycle-checked,
  returning the only handle that may `rebind`; `scope_chain_of(key)` nearest
  first.
- `scope_target(base: &Context, key: Option<ScopeKey>) -> Context` derives
  a dispatch target whose filter admits an untagged listener always and a
  tagged listener when its tag is `key` or an ancestor of `key`; `None`
  admits untagged listeners only. `global` listeners bypass it.
- `ScopedLayers<L>`: one eager global layer plus lazily created per-scope
  layers; `merge(key)` walks the chain nearest-first so a nearer named entry
  shadows a farther one; `effect(ctx, action, label)` derives the layer from
  `scope_of(ctx)`, runs `action` returning an undo, registers the undo as an
  effect of `ctx`'s fiber, reclaims an emptied layer, and fires `on_change`.
  `NamedEntries<V>` keeps insertion order; `AnonymousEntries<V>` appends.

## Check

`cargo nextest run -p extension` passes with tests proving: a registration
through a scoped context is absent from the global layer and present in
`merge(key)`; disposing the scope removes it and reclaims the layer; a
listener tagged with a parent scope receives an event dispatched to the
child's target and a listener tagged with the child does not receive the
parent's; binding a parent twice or into a cycle returns an error; a named
entry in a child layer shadows the global entry of the same name in
`merge(child)` and not in `merge(None)`.

Held by `src/extension/src/scope.rs` and `src/extension/src/tests/scope_test.rs`.
The tag rides a `scope: Option<ScopeKey>` field on `Context`, inherited by
every derivation, so `scope_of` is one read rather than a walk; `ScopeKey` is a
minted `u64` and the parent relation a process-global table, a `WeakMap`
without the weakness — an entry outlives its scope's disposal.
`merge` and the entry tables hand back cloned snapshots, because a Rust caller
cannot hold a borrow into a locked table across a dispatch. Both halves of the
routing claim are red-proofed: admitting every tagged listener makes the
parent-target dispatch answer `child`, and dropping the chain's reversal makes
`merge(child)` answer `parent`. `cargo nextest run -p extension` runs 22 and
passes 22, the seventeen bus and lifecycle tests included.

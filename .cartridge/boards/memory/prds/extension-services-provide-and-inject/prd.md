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
- "@memory/extension-context-and-fiber"
estimate: "2d"
---

# the reflect store — `provide`, `get`, `set`, `inject`, realms through `isolate`, metadata through `intercept` — and the reactive lifecycle it drives: target views, notify, the L-Unload guard, the committed view

## Do

- `Root.store: RwLock<HashMap<Realm, Impl>>` where `Realm = u64` and
  `Impl { name: String, fiber_uid: u64, fiber: Weak<Fiber>, value: Arc<dyn Any + Send + Sync>, check: Option<Arc<dyn Fn() -> bool + Send + Sync>> }`.
  `ContextInner` gains `isolate: Arc<HashMap<String, Realm>>` and
  `intercept: Arc<HashMap<String, serde_json::Value>>`, inherited by
  `extend()`; `ctx.isolate(name, realm: Option<Realm>)` and
  `ctx.intercept(name, value)` derive a child with one entry overridden
  (Definition 25, 27). A name with no realm entry resolves to a realm minted
  once at the root (`Symbol(name)` in Cordis).
- `ctx.provide(name, value)` per Algorithm 2 as an effect labelled
  `ctx.provide("name")`: error if the realm already holds the name; write
  the `Impl`, write `fiber.committed[name]`, `notify([name])`; the disposer
  removes the `Impl`, notifies, awaits the woken dependents' `settled()`, then
  removes the committed entry so the provider can read itself during its
  own teardown. `ctx.set(name, value)` overwrites only from the providing
  fiber. `ctx.get_any(name, strict) -> Option<Arc<dyn Any…>>` (strict: the
  provider fiber is `Active`); `ctx.get::<T>(name)` downcasts;
  `trait Service: Any + Send + Sync { const NAME: &'static str; }` and
  `ctx.service::<T>()` read by type.
- Resolution through the fiber chain per Algorithm 6: walk from `ctx.fiber()`
  upward; a fiber whose `committed` binds the name answers; a fiber whose
  `inject` names it but has not committed it errors `InactiveAccess`; the
  root errors `UndeclaredAccess`; the walk stops where the parent's realm for
  the name differs.
- `fiber.target: Mutex<Option<Vec<(String, u64)>>>` — for every injected
  name the uid of the `Active` provider in the fiber's realm, `None` when any
  is missing or the fiber is retired. `refresh(fiber)` per Algorithm 5:
  compare with the stored target; unchanged → return; a running inertia →
  return (the transition re-checks at its end); else spawn `reload` or
  `unload`. `reload` commits the view (`committed = resolve(inject)`), runs
  `apply` under the epoch guard, then `Active` and `notify(provided)`, or
  chains into `unload` when the target moved. `unload` first awaits every
  dependent `notify` woke, then runs the disposers LIFO, clears `committed`,
  and ends `Pending` or chains into `reload`.
- `notify(keys)` per Algorithm 3 walks the registry once per call and
  refreshes each fiber that injects a changed key in the same realm; it
  returns the fibers it woke. `Root.registry: RwLock<Vec<Weak<Fiber>>>`
  pruned on dispose.
- `Service::resolve_config(base, head)` merges the intercept entries from
  the root to the reading context (ancestor first), then `head`.

**Done 2026-09-09.** `src/extension/src/service.rs` holds the store, the realms,
`provide`, `set`, the resolution walk and `Service`; `context.rs` gains
`Root.store`, the symbol table, `ctx.isolate` and `ctx.intercept`; `fiber.rs`
gains `committed`, `provided`, `load` and `target`, and `dispose` now wakes the
dependents before it runs an inverse; `plugin.rs` holds Algorithm 5. Seven
shapes the `Do` names could not be written as written.

`get_any` returns `Result<Option<_>, Error>`. The `Do` gives it an `Option` and
two errors in one breath, and only the `Result` carries both. In the same
place, the walk does not error at the root — it falls through to the live
store, and `UndeclaredAccess` is raised when the realm holds nothing at all.
A context outside every provider's fiber chain is the ordinary case, the root
context included, and the Check's own `get_any(name, true)` reads from exactly
there; a walk that errored at the top could never answer it.

The registry stays the `HashMap<u64, Weak<Fiber>>` [extension-context-and-fiber](../extension-context-and-fiber/prd.md)
landed, not a `Vec<Weak<Fiber>>`: `forget(uid)` needs the key, `notify` walks
the values either way, and the pruning the `Do` asks for happens in
`live_fibers` — where the dead entries are already in hand.

A fiber carries what it loads (`load: Option<Load>`, the plugin and its config)
and rebuilds its own context from its parent, because a fiber holding its own
context would hold an `Arc` to itself. `refresh` reads the target and starts
the transition; the transition is one loop that re-reads the target after every
`reload` and `unload`, which is what the `Do` calls chaining, and it calls
`refresh` once more after clearing the inertia so a notification that arrived
during the last read is not dropped. `unload` awaiting its dependents is
`Fiber::wake_dependents`, shared with `dispose`: a fiber that is `Unloading` is
not `Active`, so every dependent's target has already fallen before the
notification goes out.

`intercept` merges at the derivation and not at the read. The map is inherited
whole by `extend()`, so a child holds one value per name and a read-time walk
of the parent chain cannot tell an inherited entry from an overriding one;
merging when the child is derived gives the same ancestor-first answer in a
lookup. `provide` takes and `get` returns an `Arc<T>`, so the store holds one
erased copy and hands it back downcast. And two refusals the `Do` does not
name: `NotProvider` for a `set` from a fiber that does not provide the name,
`WrongType` for a `get::<T>` whose downcast fails. `Impl.check` is carried and
read by `Impl::live`; nothing constructs a `Some` yet, since no caller in this
memo has a liveness condition beyond its provider's state.

Landed across [extension-scope-per-agent-registrations](../extension-scope-per-agent-registrations/prd.md), which reached main
first: its `Error::Duplicate(String)` is the same refusal this memo needed, so
`provide` raises that one rather than adding a second variant, and every
`Context` derivation — `extend`, `extend_with_filter`, `extend_scoped`,
`isolate`, `intercept`, `with_fiber` — became one `derive` that clones the
whole inner context and hands the caller the one field it came to change.
Seven inherited fields listed at six construction sites was the alternative.

## Acceptance
`cargo nextest run -p extension` passes with tests proving: a plugin injecting
`counter` stays `Pending` until a second plugin provides it, then goes
`Active`; disposing the provider unloads the dependent before the provider's
disposer runs, and the dependent's disposer still reads `counter` through its
committed view; replacing the provider with a new fiber restarts the
dependent exactly once and its new target carries the new uid; a dependent
mounted under `ctx.isolate("counter", None)` stays `Pending` while the
parent realm's provider is `Active`; two `intercept` entries on nested
contexts merge ancestor-first with `head` last; `get_any(name, true)`
answers `None` while the provider is `Loading` and `Some` once `Active`;
`provide` of a name already held in the realm returns an error and leaves
the first `Impl` in place.

Held by `src/extension/src/tests/service_test.rs`: the seven above plus two the
`Do` describes and the Check does not reach — `set` accepted from the providing
fiber and refused from another, and `internal/service` reaching a listener in
the realm that changed and not one in an isolated realm. `cargo nextest run -p
extension` runs 31 and passes 31 on the landed commit — the seventeen lifecycle
and event tests and the five [extension-scope-per-agent-registrations](../extension-scope-per-agent-registrations/prd.md) landed
alongside included; `cargo test --test layer_headers` still accepts the crate at L0, and
`extension` stays out of `[workspace.dependencies]` because no member inherits it
([the-extension-catalogue-row-has-no-member](../the-extension-catalogue-row-has-no-member/prd.md)). Red-proof: dropping
`wake_dependents` from `dispose` turns the disposal order to
`["provider", "dependent read Ok(Some(7))"]` and fails the second test.

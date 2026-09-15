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
estimate: "1d"
---

# the events service — typed events, `on`/`once` as fiber-owned effects, `emit`, `parallel`, `serial` and `waterfall` dispatch, filtered targets, and the `internal/*` events the lifecycle emits

## Do

- `pub trait Event: 'static { const NAME: &'static str; const MODE: Mode; type Args: Send + Sync + 'static; type Ret: Send + 'static; }`
  with `enum Mode { Emit, Parallel, Serial, Waterfall }`. A dispatch method
  refuses an event whose `MODE` is not its own with a `debug_assert` and a
  `tracing::warn`.
- Listener types: `Listener<E> = Arc<dyn Fn(E::Args) -> BoxFuture<'static, E::Ret> + Send + Sync>`
  and, for waterfalls, `Around<E> = Arc<dyn Fn(E::Args, Next<E>) -> BoxFuture<'static, E::Ret> + Send + Sync>`
  with `Next<E> = Box<dyn FnOnce(E::Args) -> BoxFuture<'static, E::Ret> + Send>`.
  `Hook { ctx: Context, fiber_uid: u64, prepend: bool, global: bool, callback: Box<dyn Any + Send + Sync> }`
  stored in `Root.events: RwLock<HashMap<&'static str, Vec<Hook>>>`.
- `ctx.on::<E>(listener, EventOptions { prepend, global }) -> Disposer`
  registers as an effect labelled `ctx.on("name")` of the current fiber, so
  the fiber's unload removes it; `once` wraps the listener with its own
  disposer. Registration dispatches `internal/listener`.
- Dispatch reads the hook list once under the lock, drops the lock, filters
  by the target context's filter (`Context::filter`: an
  `Option<Arc<dyn Fn(&Context) -> bool + Send + Sync>>` on `ContextInner`,
  set by `extend_with_filter`), admits `global` hooks always, then:
  `emit` spawns each listener's future with `tokio::spawn` and returns;
  `parallel` joins all and returns `Result<(), Vec<Error>>`;
  `serial` awaits in order and returns the first `Some(ret)` (the `bail`
  reading of [[composition-is-a-pillar-of-memory]]); `waterfall` builds the
  chain outermost-first around the dispatcher's own `inner` closure and
  returns the outermost result — a listener that never calls `next` vetoes.
  `ctx.emit::<E>(args)` targets `ctx` itself; `ctx.emit_to::<E>(target, args)`
  and the same for the other three carry an explicit target.
- Every dispatch of a name not starting with `internal/` first emits
  `internal/dispatch { mode, name }`. `Fiber` emits `internal/plugin` on
  creation and disposal and `internal/status { old, new }` on every state
  change; `provide` and its disposer emit `internal/service { name }` to a
  target filtered to the name's realm.

`events.rs` holds the trait, the four dispatch methods, the registration and
the `internal/*` declarations; `context.rs` gains `Root.events` and the target
filter; `fiber.rs` and `plugin.rs` emit. Six shapes the `Do` names could not be
written as written. A mode's return type is a bound on the event and not a
reading of `E::Ret`: `parallel` takes `E: Event<Ret = Result<(), Error>>` and
`serial` takes `E: Event<Ret = Option<T>>` and answers `Option<T>`, because no
generic dispatcher can look inside an opaque `E::Ret` for a `Some`. Every mode
that fans one argument out to several listeners bounds `E::Args: Clone`; only
`waterfall`, which threads one value through, does not. `on` returns the
`EffectHandle` that `ctx.effect` returns, the `Do`'s `Disposer` being what an
effect body hands *in*; `once` returns it inside an `Arc`, because the wrapper
needs its own handle to dispose itself on the first call. A waterfall listener
registers through `ctx.around`, not `ctx.on` — `MODE` is a const and cannot
choose a parameter type. `Hook` carries no id: the list holds `Arc<Hook>` and a
disposer removes its own by `Arc::ptr_eq`. And `internal/service` has no
emitter here, because `provide` does not exist yet; it lands with
[extension-services-provide-and-inject](../extension-services-provide-and-inject/prd.md), which writes the effect that emits it.

## Acceptance
`cargo nextest run -p extension` passes with tests proving: `emit` returns
before a listener that sleeps completes, and the listener still runs;
`parallel` runs three listeners concurrently, awaits all, and returns both
errors of two failing ones; `serial` calls listeners in registration order,
`prepend: true` puts one first, and the first `Some` stops the chain;
`waterfall` passes a value through two wrapping listeners into the inner
closure and back, and a listener that does not call `next` stops the inner
closure from running; a listener registered through a plugin's context is
gone after that plugin's fiber is disposed; a target with a filter admits a
listener whose context passes and skips one that fails while a `global`
listener always runs; `internal/status` reports `Pending → Loading → Active`
for a plugin.

Held by `src/extension/src/tests/events_test.rs`: the seven above plus two the
`Do` describes and the Check does not reach — a `once` listener that runs once
across two dispatches, and the veto half of the waterfall as its own test.
`cargo nextest run -p extension` runs 17 and passes 17, the eight lifecycle tests
included; `cargo test --test layer_headers` still accepts the crate at L0, and
`extension` stays out of `[workspace.dependencies]` because no member inherits it
([the-extension-catalogue-row-has-no-member](../the-extension-catalogue-row-has-no-member/prd.md)).

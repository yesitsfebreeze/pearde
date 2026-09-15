---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1d"
---

# the `extension` crate skeleton with `Context`, `Fiber`, `ctx.effect` and `ctx.plugin` — LIFO disposal, the six fiber states, inertia, and a failing plugin that installs nothing

## Do

- Add `src/extension` to `Cargo.toml` `members` and `workspace.dependencies`
  (`extension = { path = "src/extension" }`); `lib.rs` opens with
  `//! Layer: L0 · No Memory imports.` and the crate doc naming this memo's
  decision, [[composition-is-a-pillar-of-memory]].
- `Context`: `Arc<ContextInner { root: Weak<Root>, parent: Option<Context>, fiber: Arc<Fiber> }>`.
  `Context::root()` builds `Root` (the registry, the uid counter; the store
  and events come in later children) with a root fiber of uid 0 in state
  `Active`. `ctx.extend()` derives a child sharing the fiber; `ctx.fiber()`,
  `ctx.root()`.
- `Fiber`: `uid: AtomicU64` (0 root, `u64::MAX` once disposed), `parent:
  Context`, `state: Mutex<FiberState>` with `Pending | Loading | Active |
  Failed(Error) | Unloading | Disposed`, `disposables: Mutex<Vec<(Label, Disposer)>>`,
  `inertia: Mutex<Option<Shared<BoxFuture<()>>>>`. `Disposer = Box<dyn FnOnce() -> BoxFuture<'static, ()> + Send>`,
  `BoxFuture<T> = Pin<Box<dyn Future<Output = T> + Send>>`.
- `ctx.effect(label, body)` per Algorithm 1: `assert_active()` (error
  `InactiveEffect` when uid is cleared or state is `Unloading`), run `body`
  (an `async` returning `Result<Disposer, Error>`), push the disposer; the
  returned handle disposes once (second call a no-op) and settles when the
  disposer's future completes. If the fiber's epoch moved while `body` was
  awaited, the collected disposer runs immediately and the effect reports
  `Stale`.
- `trait Plugin: Send + Sync + 'static { fn name(&self) -> &str; fn inject(&self) -> &[&'static str] { &[] } fn apply(&self, ctx: Context, config: serde_json::Value) -> BoxFuture<'static, Result<(), Error>>; }`.
  `ctx.plugin(plugin: Arc<dyn Plugin>, config) -> Arc<Fiber>` per Algorithm 4:
  the child fiber is registered as an effect of the parent (so a parent unload
  retires its children first), then `refresh` runs — with no `inject` the
  target is satisfied and `reload` (Algorithm 5) spawns as the inertia:
  `Loading` → `apply` → `Active`, or `Failed` with every disposer collected so
  far already run (Corollary 69).
- `fiber.dispose().await`: clear uid, `unload` (disposers LIFO, each error
  logged through `tracing`, never propagated), `Disposed`; `fiber.settled().await`
  waits out the inertia and returns the startup error if any (Cordis `await`).
- Tests in `src/extension/src/tests/`.

**Done 2026-09-08.** The crate is `src/extension`, four files: `lib.rs` carries
the `Layer: L0` line, `Disposer`, `Label` and `Error`; `context.rs` the
`Context` handle, `extend`, `parent` and the `Root` registry; `fiber.rs` the
six states, the epoch, LIFO `unload`, `dispose`, `settled` and `ctx.effect`;
`plugin.rs` the `Plugin` trait, `ctx.plugin` and Algorithm 5. Three shapes the
`Do` names could not be written as written. `BoxFuture` is
`futures::future::BoxFuture<'a, T>` — already installed, already that type, and
the only spelling under which the `Do`'s own `BoxFuture<'static, ()>` compiles.
The root fiber's `parent` is `None`, because a root context cannot exist before
the fiber it holds. And `ctx.root()` is `ctx.registry()`, because Rust cannot
carry one name as both the constructor and the accessor the `Do` asks for;
`ContextInner.root` is a strong `Arc` for the same reason, nothing else in the
crate owns the `Root`.

## Acceptance
`cargo nextest run -p extension` passes with tests proving: three effects
dispose in reverse registration order; `effect` after `dispose` returns
`InactiveEffect`; a plugin whose `apply` returns `Err` ends `Failed` and its
two earlier disposers have run; disposing a parent fiber disposes a child
plugin's fiber before the parent's own disposers; a plugin with no inject
goes `Pending → Loading → Active` and `settled()` returns `Ok`.
`cargo test --test layer_headers` passes.

Held by `src/extension/src/tests/lifecycle_test.rs`: the five above plus three
more the `Do` describes and the five do not reach — a handle disposing its own
effect once, a body awaited across a transition reporting `Stale` with its
inverse already run, and an extended context sharing its parent's fiber. Eight
run, eight passed; `cargo test --test layer_headers` 3 passed.

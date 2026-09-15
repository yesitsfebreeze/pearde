---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: memory-daemon-boots-a-root-context
needs:
- "@memory/extension-services-provide-and-inject"
- "@memory/extension-events-four-dispatch-modes"
- "@runtime/extension-inspect"
---

# Memory's owner refuses writes while draining and survives a failed replacement

Memory owns its store through two lifecycles: the CLI daemon (`run_server` in `src/commands/src/commands_serve.rs`) and the transport cartridge (`on_dispose` in `src/cartridge.rs`). Three gaps are visible at `c25af4d`:

- While shutdown runs, `invoke` refuses only model-dependent ops (`src/rpc/src/server.rs`). forget, degrade, move, promote, pulse and gc are still admitted while `save_fn` runs.
- A replacement daemon evicts its predecessor (`evict_predecessor`) before it knows it can boot, and continues "anyway" after a timeout.
- `ready` reports pid and draining state but not store state.

Outcome, owned by memory: fix only those three gaps. There is no plugin tree or root Context; memory decision `memory-is-a-plugin-tree` conflicts with the repository scope in `.cartridge/docs/AGENTS.md`.

## Acceptance

- [ ] Once shutdown begins, every mutating op is refused with a draining error. In-flight calls complete and their effects are included in the final save (`lifecycle_test.rs` plus a `server_admin_test.rs` case).
- [ ] A replacement whose config or store-directory validation fails exits without stopping the running owner, which keeps answering `health` with the same pid (`e2e/lifecycle.rs`).
- [ ] `ready` reports store state (opening, ready, draining or unavailable), consistent with cartridge `status`, and the cartridge `on_dispose` path follows the same admission rule.

## Proof and recovery

First probe: reproduce each gap in a disposable store with the existing e2e harness and record what happens. Gates, from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test`, `just e2e` (not run). Rollback: revert per gap; the writer lock and guarded flush stay the durability boundary.

## Dependencies and review

No hard needs. Shares its lifecycle files with memory-signals-become-events, so land this first. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--memory-daemon-boots-a-root-context.md` (status open, estimate 1d). The PRD state above is authoritative.

> `run_server` builds a root `Context` and mounts the store, the socket RPC, the hub registration, the self-watch and the model service as plugins, so shutdown is the root fiber's LIFO disposal and `memory plugins` prints the tree

### Do

In `src/commands/src/commands_serve.rs` (`run_server`, today at `:330`):

- `let root = extension::Context::root();` before the bootstrap. Add
  `extension` to `commands`' dependencies.
- `memory-core` plugin: `apply` runs `bootstrap(cli, cfg)` and provides
  `store` (`Arc<rpc::server::Server>`), `task_q` and `save_fn` as services;
  its disposer is the save path that follows `shutting down...` today.
- `memory-rpc` plugin, `inject: ["store"]`: `take_memory_listener`, the handover
  fd publication, `MemoryRpcHandler::new`, `tokio::spawn(serve_memory_rpc_loop)`;
  the disposer aborts the task and drops the listener. `hub-register`, `self-watch` (only when `cfg.reload.enabled`) and
  `models` (`commands_models::connect`) each a plugin with the matching
  disposer; `evict_predecessor` stays where it is, before the root.
- The shutdown `Notify` fires `root.fiber().dispose().await`; because the
  RPC plugin was mounted after `memory-core`, it stops admitting before the
  store's disposer saves. `util::lifecycle::begin_shutdown` is
  called first, as now.
- RPC `plugins` on `MemoryRpc` (`src/transport/src/memory_rpc.rs`) returning
  `extension::inspect(&root)` as JSON; `memory plugins` in `commands` prints it
  as a tree: one line per fiber (`uid name state`), indented by parent,
  `Pending` fibers with their missing keys.
- `Server::invoke`'s name list gains `"plugins"` so the MCP surface reaches
  it too.

### Check

`just test` green (the e2e `lifecycle.rs` and `daemon_reads.rs` suites
cover the boot and the ctrl-c save). A unit test in `commands` mounts the
built-in plugin list on a root with a fake `bootstrap` and asserts the
disposal order recorded by the fakes is `models, self-watch, hub-register,
memory-rpc, memory-core`. `memory plugins` against the project daemon prints five
fibers in state `Active`.

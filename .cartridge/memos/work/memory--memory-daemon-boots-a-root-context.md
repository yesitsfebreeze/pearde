---

kind: work
level: 10
status: open
estimate: 1d
needs: "[[@prd/work/memory--extension-services-provide-and-inject.md]] [[@prd/work/memory--extension-events-four-dispatch-modes.md]] [[@prd/work/memory--extension-inspect.md]]"
description: "`run_server` builds a root `Context` and mounts the store, the socket RPC, the hub registration, the self-watch and the model service as plugins, so shutdown is the root fiber's LIFO disposal and `memory plugins` prints the tree"
read_when: "touching run_server, a daemon shutdown path, or adding a built-in plugin"
---

# memory-daemon-boots-a-root-context

## Do

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

## Check

`just test` green (the e2e `lifecycle.rs` and `daemon_reads.rs` suites
cover the boot and the ctrl-c save). A unit test in `commands` mounts the
built-in plugin list on a root with a fake `bootstrap` and asserts the
disposal order recorded by the fakes is `models, self-watch, hub-register,
memory-rpc, memory-core`. `memory plugins` against the project daemon prints five
fibers in state `Active`.

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

# the e2e harness kills only the processes it spawned itself, so the hubs and nodes those processes spawned outlive every run — 27 per suite after the give-up leak was closed

## Do

`MemoryProject::drop` (`tests/e2e/harness.rs:356`) walks `self.children`, kills
each and removes the runtime dir. Those are the processes the harness spawned
by hand. A test daemon auto-starts a `memory hub` through `register_with_hub`,
and that hub spawns per-root nodes; neither is in `self.children`, and the
hub deliberately leaves its nodes running when it exits — `nodes stay up
(they own their sockets)` is the production posture and should not change.

Reap them from the runtime dir instead, which is this project's alone: before
`remove_dir_all`, walk every socket in `self.runtime` — `node_sockets()`
already enumerates the node ones and `memory-hub.sock` is the hub — and shut
down whatever answers, killing what does not. Errors stay dropped, as they
are today: a test that already failed must not fail again on its cleanup.

Landed as `reap_runtime`, called from `drop` between the kill loop and
`remove_dir_all`. The hub socket is asked for its `status`, every node it
names is `unload`ed — the hub's own unload is the graceful shutdown with the
kill behind it, so the killing is the hub's and the harness needs no pid —
then the hub is `stop`ped and whatever node socket is still there is asked to
`shutdown` directly, which reaches a node whose hub is already dead. The call
is a `UnixStream` and one JSON line rather than the generated client: the wire
is one envelope per line with no handshake, `tests/bench` compiles this same
file and does not depend on `transport`, and a blocking socket keeps an async
runtime out of `Drop`. Unix only, like the `.sock` names `node_sockets()`
already matches.

## Acceptance
`ps aux | grep -c 'worktrees/.*/target/debug/memory'` after a full `just all`
in a lane: zero. It was 617 accumulated across nine worktrees on 2026-09-06,
and 27 from a single suite once [[the-hub-leaks-the-node-it-gave-up-on]]
closed the give-up path.

Measured on the e2e suite in the `drive` lane, 2026-09-07: 82 passed, 4
processes standing the moment the binary exited and zero twenty seconds later
— the four were the flushes the reap had just asked for. Every one of the 27
came from `hub::a_cross_root_search_registers_the_project_it_was_called_from`,
whose `query --all` fans the hub out over the machine-wide registry and boots
a node per root on the box; that test alone runs 367s of the suite's 367s.

Unresolved prerequisites at migration: `the-hub-leaks-the-node-it-gave-up-on`.

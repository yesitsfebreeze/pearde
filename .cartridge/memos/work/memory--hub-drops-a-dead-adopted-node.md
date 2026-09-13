---
kind: work
level: 10
status: done
description: the hub's reaper keeps an adopted node whose daemon is gone as long as its root directory exists, so a real tree's hub never reaches empty
read_when: "asking how the hub's map empties"
---

# hub-drops-a-dead-adopted-node

## Do

`spawn_reaper`'s `retain` (`src/hub/src/lib.rs:573`) drops a node on two tests:
`handle.alive()`, which an adopted node answers unconditionally true, and
`root.is_dir()`. A daemon the hub adopted through `resolve` — every daemon that
registers itself on boot — that is then killed leaves an entry the reaper keeps
forever, because its project directory is still there. `idle_pass` cannot clear
it either: `idle_ms` returns `None` on a refused connection and the call site
reads that as "pre-field daemon, never unload on a lie".

Give the retain pass the third test it is missing. `probe(root)`
(`src/hub/src/lib.rs:57`) is the connect check and already exists; it is async,
so collect the adopted roots (`child.is_none()`) first, probe them, and remove
the ones that refuse. Keep the distinction the code already makes: a socket
that answers without an `idle_ms` field is alive, a socket nothing accepts on
is gone.

This is the other half of `an-auto-started-hub-stops-itself`: the idle exit
only fires on an empty node map, and a stale adopted entry is what keeps a
real tree's map from ever being empty.

Done 2026-09-06: `drop_dead_adopted` (`src/hub/src/lib.rs:625-654`) runs in the
reaper right after the retain pass — adopted roots collected under the lock,
probed off it, and removed when nothing accepts on their socket. The map is
emptied before the idle-exit check reads it, so the auto-started hub
`an-auto-started-hub-stops-itself` describes can now reach that exit on a
real tree.

## Check

An e2e test in `tests/e2e/hub.rs`: start a hub, `hub resolve` to spawn a node,
kill the node's process while its root stays on disk, and `hub status` reports
no nodes loaded inside the reaper's cadence.

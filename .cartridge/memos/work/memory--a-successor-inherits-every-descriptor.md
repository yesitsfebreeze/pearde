---
kind: work
level: 10
status: done
description: the handover spawns the successor with `Command::new`, so every non-CLOEXEC descriptor rides along — fourteen daemons on this machine each pin a 331 MB store none of them serves
read_when: "touching the handover, or auditing what a daemon holds open"
---

# a-successor-inherits-every-descriptor

## Do

`spawn_successor` (`src/identity/src/lib.rs:159`) passes the listener on
purpose:

```rust
Command::new(&exe)
    .arg("--daemon")
    .env(TAKEOVER_ENV, "1")
    .stdin(Stdio::from(listener_fd))
```

Everything else open at that moment rides along with it, because a descriptor
is inherited unless it is CLOEXEC and LMDB's is not. Measured 2026-09-06 across
the fourteen daemons running on this machine, one per root: each has fd 0 on
its own socket, fds 12 and 14 on its own root's `data.mdb` — and fd 11 on
`/Users/feb/dev/memory/.memory/data/data.mdb`, a store it does not serve, carried
down from an ancestor that once did.

It is not a second writer. POSIX record locks are not inherited across a fork,
`memory status` reads `daemon not serving this directory` with the writer lock
free, and no daemon writes through fd 11 — the flush fight in
[[@prd/work/memory--one-daemon-per-store.md]] has a different cause. What it costs is that fourteen
processes pin a 331 MB file none of them will ever read, so the store cannot be
replaced or reclaimed while they live, and each new generation of the handover
carries the whole inherited set forward again.

Close what the successor does not need: mark the store's descriptors CLOEXEC
when the environment opens them, and let the handover pass the listener alone,
which is the one descriptor it means to pass.

## Check

After a handover, `lsof` on the successor lists its own socket and its own
store and no descriptor onto any other root's `data.mdb`.

Done 2026-09-06: `spawn_successor` marks every descriptor from 3 up
close-on-exec in a `pre_exec` hook, so only the dup2'd listener and stdio cross
the exec. Checked by two handovers on scratch stores: the shipped binary's
successor held `data.mdb` three times — its own pair and the predecessor's
fd 14 — and the socket twice; the fixed binary's successor held exactly its own
pair, the adopted listener on fd 0, and no other root's file.

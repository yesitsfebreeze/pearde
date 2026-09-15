---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/router.ctg"
capability-owner: router
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/auth.rs"
---

# Router refreshes OAuth tokens under the one daemon, not per process

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies router as a bound
exclusive resource: its OAuth refresh lock only works inside one process
(`auth.rs:282`), so two hosts both spend the same refresh token. Under the
one-daemon shape there is one router node, so the lock holds again — but any
refresh initiated by an attached instance must go through that node.

## Outcome

All OAuth token refreshes happen in the daemon's single router node, where the
in-process lock is the right lock. An attached instance never refreshes on
its own path, so one refresh token is never spent twice.

## What changes

- With the host-attach contract in force there is one router node; verify
  attached instances' routing requests flow through it.
- If any refresh path can still run outside the daemon (e.g. a CLI-side
  refresh), route it through the daemon or hold a file lock instead.

## Acceptance

- [ ] Two concurrent refresh-triggering requests through the daemon spend the
      refresh token once (one token rotation, one successful pair of
      follow-on requests).
- [ ] No refresh code path runs outside the daemon's router node while a
      daemon is attached.
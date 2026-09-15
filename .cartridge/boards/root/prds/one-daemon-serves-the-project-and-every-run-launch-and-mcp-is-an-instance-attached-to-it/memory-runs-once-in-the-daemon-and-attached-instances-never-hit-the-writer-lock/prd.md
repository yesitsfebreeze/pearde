---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/memory.ctg"
capability-owner: memory
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/store/lock.rs"
- "src/"
---

# Memory runs once in the daemon and attached instances never hit the writer lock

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies memory as
must-exist-once-per-project: `writer.lock` means every call on a second host
fails with `another memory writer holds this data dir`, including its ledger
appends (this is the exact failure the ledger item depends on avoiding).

## Outcome

Memory is composed exactly once, in the project daemon. An attached instance's
memory calls (including `ledger append` from the proxy) go through the
daemon's node and succeed; no second node ever exists to hit the writer lock.

## What changes

This child mostly verifies the shape rather than changing memory itself:

- With the host-attach contract in force, an instance never starts a second
  memory node, so the writer lock is never contended by construction.
- The ledger condensing loop (every 60s, holding off 5 min after any import
  call) runs only in the daemon's memory node; verify a short-lived attached
  `run`/`call` does not start or interfere with it.
- If any memory path still assumes process-exclusivity beyond the file lock,
  record it and fix it here (e.g. attach-mode memory must not try to take the
  writer lock read-only; it is the same node).

## Acceptance

- [ ] With the daemon running, `cartridge run memory '{"op":"status"}'` and a
      proxy-ledger append both succeed with exactly one memory node process;
      no `another memory writer holds this data dir` error appears.
- [ ] A memory `ingest` from one attached instance is returned by `query`
      from another (parent Acceptance box 3).
- [ ] The condensing loop's status (`{"op":"ledger","action":"status"}`)
      shows the daemon's one node doing the condensing.
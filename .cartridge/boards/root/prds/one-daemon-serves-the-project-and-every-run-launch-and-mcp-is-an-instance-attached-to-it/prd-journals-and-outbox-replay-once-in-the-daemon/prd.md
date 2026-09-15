---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/prd.ctg"
capability-owner: prd
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/service.ts"
---

# PRD journals and outbox replay once in the daemon

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies prd as must-exist-once:
under two compositions the job journal shows the other host's jobs as
`interrupted`, and the memory outbox is replayed twice (`service.ts:127`,
`:176`). The job journal also claims every job on start (this session's own
`prd add` events observed the peer item's claim).

## Outcome

The one prd node in the daemon owns the job journal and the memory outbox.
Attached instances' `prd` calls (scan/plan/add/claim/collect) all land on
that one node, so jobs are never marked interrupted by a second host and the
outbox replays once.

## What changes

- With the host-attach contract in force there is one prd node; this child
  verifies journal and outbox behaviour under attached instances and removes
  any per-process assumption (the interrupt-marking at start, the outbox
  replay) that would still misbehave if two instance-driven calls race inside
  the one node.

## Acceptance

- [ ] A job started through one attached instance is not shown interrupted
      when another instance starts a job or calls prd.
- [ ] The memory outbox replays exactly once for a given pending
      acknowledgment, no matter how many instances make prd calls.
- [ ] Exactly one prd node exists with the daemon running.
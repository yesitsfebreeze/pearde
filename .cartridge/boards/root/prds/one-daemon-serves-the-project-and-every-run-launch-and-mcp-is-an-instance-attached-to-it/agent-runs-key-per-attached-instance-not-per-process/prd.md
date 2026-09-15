---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/agent.ctg"
capability-owner: agent
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/"
---

# Agent runs key per attached instance, not per process

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies agent runs as
per-instance state: agent's single-flight guard only works inside one
process, so two hosts can drive one session and overwrite its transcript.
Under the one daemon, two attached instances must be able to drive two runs
of their own without the in-node guard serializing them into one session.

## Outcome

Agent runs in the one node are keyed by attached instance: an instance's run
references its own session and transcript, single-flight applies per
instance, and two instances never overwrite one transcript.

## What changes

- The single-flight guard keys by instance id, not globally in the node.
- Run/session references carry the owning instance, so resume and transcript
  writes go to the right instance's run.

## Acceptance

- [ ] Two attached instances can each hold one active agent run
      simultaneously; neither is refused by the other's single-flight guard.
- [ ] One instance resuming its run never reads or writes the other's
      transcript or session.
- [ ] Exactly one agent node exists with the daemon running.
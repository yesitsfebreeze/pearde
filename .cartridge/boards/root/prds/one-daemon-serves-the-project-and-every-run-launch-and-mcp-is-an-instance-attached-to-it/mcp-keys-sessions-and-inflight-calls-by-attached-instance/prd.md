---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/mcp.ctg"
capability-owner: mcp
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/service.rs"
---

# MCP keys sessions and inflight calls by attached instance

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies mcp stdio clients and
in-flight calls as per-instance state keyed inside the shared cartridge: mcp
keeps one `session` and one `inflight` map per node today
(`mcp.ctg/src/service.rs:88-92`), so two attached stdio clients would share
one session and one call set.

## Outcome

The one mcp node keys its `session` and `inflight` maps by attached instance
(the connected stdio client), so two attached MCP clients keep separate
sessions and separate in-flight calls, while the node itself exists once.

## What changes

- `session`/`inflight` maps become keyed by instance id (the connection), not
  one entry per node.
- Session lifecycles: an instance disconnecting drops only its own session
  and cancels only its own in-flight calls.

## Acceptance

- [ ] Two `cartridge mcp` stdio clients attached to one daemon keep separate
      sessions (each sees only its own initialization and history), and one
      closing does not affect the other's session or calls.
- [ ] An in-flight call from one instance is not visible in or cancellable
      from the other.
- [ ] Exactly one mcp node exists with the daemon running.
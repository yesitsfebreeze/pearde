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
needs:
- "@memory/mcp-attachment-recovers-without-replaying-work"
estimate: "1d"
---

# Routine and tool catalogs recover and refresh in an existing MCP session without partial publication

## Do

An MCP session initialized while its daemon is unavailable discovers the canonical
routine and tool catalog when the daemon recovers, without restarting the host.
Additions and removals become visible through the supported catalog-change
contract; browsing definitions never executes their procedures.

A complete validated replacement supersedes the previous catalog. A temporary
fetch failure does not erase usable definitions, and partial registration failure
does not publish half a catalog. Retained definitions are not presented as proof
that their backend is reachable. Stale-generation notifications cannot undo the
current catalog, and project identity never leaks across roots.

The existing harness already implements reconnect, serialized catalog refresh,
and fetch-before-swap behavior. This work closes the adapter-to-daemon gap rather
than rebuilding that host mechanism.
[mcp-attachment-recovers-without-replaying-work](../mcp-attachment-recovers-without-replaying-work/prd.md) owns transport recovery and
its non-replay boundary.

---
kind: work
level: 10
status: open
claim: b424ceba 2026-09-09 15:55
estimate: 1d
description: Routine and tool catalogs recover and refresh in an existing MCP session without partial publication
needs: '[[@prd/work/memory--mcp-attachment-recovers-without-replaying-work.md]]'
read_when: dynamic tools disappear after cold initialization or daemon reload
---

# mcp-catalog-recovers-in-the-existing-session

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
[[@prd/work/memory--mcp-attachment-recovers-without-replaying-work.md]] owns transport recovery and
its non-replay boundary.

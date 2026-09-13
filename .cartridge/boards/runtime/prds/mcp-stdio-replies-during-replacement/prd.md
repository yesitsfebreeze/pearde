---
state: "done"
origin: requested
priority: 50
repo: /Users/feb/dev/cartridge/cartridge.ctg
workflow: develop-one-cartridge
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: mcp-stdio-replies-during-replacement
footprint: ["src/main.rs",".cartridge/tests/unit/stdio.rs","src/loader.rs"]
commit: "bd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df"
---

# MCP stdio replies during replacement

A connected MCP client must receive a correlated JSON-RPC error when profile
replacement temporarily removes the MCP provider. The current stdio bridge
prints the failure to stderr and drops the request, leaving the client waiting.
This dependency was discovered by the real client proof for
[@mcp/improve-mcp-refresh-catalog](../../../mcp/prds/improve-mcp-refresh-catalog/prd.md).
It inherits that plan's used review rounds; splitting does not reset the budget.

## Acceptance

- [x] An unavailable-provider request receives exactly one JSON-RPC internal error with its original ID; successful responses remain unchanged.
- [x] Notifications and client responses remain silent; malformed JSON gets a parse error, and no failed tool call is replayed.
- [x] The focused runtime binary tests pass; the initialized live MCP addition/removal test no longer loses a reply during replacement.

## Proof and recovery

Baseline: the initialized client timed out on tools/list with stderr
`mcp: mcp is not provided`; see baseline.json. Reuse the existing stdio bridge
and response channel. Factor only reply selection for direct tests, preserving
concurrent cancellation and clean protocol stdout. Work in an isolated runtime
lane because the user's checkout contains unrelated work. No persistence changes.

## Verified result

Two focused runtime tests pass and binary/test clippy passes in the isolated
lane. Disabling the bridge error reply makes the unchanged correlation test
fail. The actual initialized MCP client passes all replacement, rejection,
addition and removal scenarios using this lane's built runtime executable.
See verification-summary.json.

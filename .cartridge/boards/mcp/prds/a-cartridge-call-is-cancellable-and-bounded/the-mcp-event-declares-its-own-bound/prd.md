---
state: "done"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/mcp.ctg"
footprint:
- "cartridge.json"
commit: "1595a6fa52e4f8f4635ca426ec1fcddd40e7d277"
---

# The mcp event declares its own bound

## Outcome

The `mcp` event declares the bound it should be held to, so a slow MCP line
fails against a number this cartridge chose rather than silently inheriting the
host's default.

## Evidence

Established 2026-09-17 by analyst-1 of the parent, against `mcp.ctg` HEAD
`345871e`. `mcp.ctg/cartridge.json` declares the `mcp` event with no
`timeout_ms`, so the host applies its default `event_timeout_ms` of 60000 ms —
`cartridge.ctg/src/host/plan.rs:299-301` **at HEAD `63ff234`** — and every MCP
line that overruns it fails as a bare `mcp did not answer in time`, which is the
message this project's coordinators and workers have been seeing all day.

The sibling `@proxy/the-proxy-answers-within-its-bound-or-reports-the-delay`
found the same mechanism in the proxy's manifest and closes the proxy side only.
This PRD is the mcp side. Neither widens its footprint into the other's
cartridge: a cartridge declares its own surface.

## Acceptance

- [x] `mcp.ctg/cartridge.json` declares `timeout_ms` on the `mcp` event, at a
      value chosen from what an MCP line legitimately takes, not from the
      default.
- [x] A check fails if the declaration is removed, so the bound cannot be lost
      silently again.

## Note on line numbers

`plan.rs:322-324`, cited by the proxy sibling's analyst, is the **dirty working
tree**. At HEAD `63ff234` the same code is at `src/host/plan.rs:299-301`. Cite
HEAD: a lane is cut from it.

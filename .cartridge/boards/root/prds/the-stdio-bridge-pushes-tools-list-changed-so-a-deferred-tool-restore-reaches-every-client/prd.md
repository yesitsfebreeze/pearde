---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
capability-owner: cartridge
work-kind: leaf
footprint:
- "cartridge.ctg"
- "cartridge.ctg/src/cli/host.rs"
- "mcp.ctg"
- "mcp.ctg/src/service.rs"
- "mcp.ctg/cartridge.json"
needs:
- "@mcp/deferred-tool-band"
---

# A restored deferred tool reaches the client without a re-list

## Outcome

`@mcp/deferred-tool-band` ships with `band=false` because the host's stdio bridge
(`cartridge.ctg/src/cli/host.rs`) writes one reply per request line and never pushes.
A `tools` restore therefore only reaches a client that re-lists, and Claude Code does
not re-list. The bridge must be able to forward a server-initiated
`notifications/tools/list_changed`, mcp must advertise `capabilities.tools.listChanged`
and emit the notification after a restore, and then the `band` default flips to `true`.

## Acceptance

- [ ] Over the stdio bridge, a `tools/call tools {name}` restore is followed by exactly one `notifications/tools/list_changed` line on the same client's stdout, and a request/reply exchange still pairs one reply per request.
- [ ] mcp's `initialize` result advertises `tools.listChanged: true` only while `band` is on.
- [ ] `band` defaults to `true` in `mcp.ctg/cartridge.json`, and `band=false` still produces byte-identical output to the pre-band listing.
- [ ] `just check cartridge`, `just test cartridge`, `just check mcp` and the mcp band unit tests pass from `/Users/feb/dev/cartridge`.

## Proof and recovery

Filed 2026-09-16 from the round-2 review of `@mcp/deferred-tool-band`. Recovery: set
`band=false`; the push is inert without a restore.

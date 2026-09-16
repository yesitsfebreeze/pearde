---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: runtime
work-kind: leaf
footprint:
- "cartridge.ctg"
- "cartridge.ctg/src/cli/host.rs"
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
---

# cartridge mcp waits for a cold host to settle

## Outcome

On a cold host (no daemon yet), `cartridge mcp` gives up with "service mcp unavailable:
no active listener" in 3 of 3 runs. It stops waiting after three identical status polls
while cartridges are still starting (`cartridge.ctg/src/cli/host.rs:157` at cdd3124/771e046).
The first MCP client of a fresh project therefore fails. The wait should end when the
requested listener is active or a bounded startup deadline passes, not on repeated
identical polls.

## Acceptance

- [ ] In an isolated project with no running daemon, `cartridge mcp` answers `initialize` and `tools/list` on 5 of 5 cold starts.
- [ ] If the listener never becomes active, `cartridge mcp` fails within the documented startup deadline with a message naming the missing listener.
- [ ] `just check cartridge`, `just test cartridge` and `just test lifecycle` exit 0.

## Proof and recovery

Found 2026-09-16 by the smoke analyst of `@root/smoke-passes-mcp-and-proxy` (spec01 round-4
revision). The smoke fixture works around it by starting the daemon itself. The fix lands
after the daemon-attach leaf, which rewrites the same attach path in `src/cli/host.rs`.

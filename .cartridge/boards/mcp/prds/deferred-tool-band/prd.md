---
state: "claimed"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/mcp.ctg"
work-kind: leaf
canonical-scope: deferred-tool-band
claim: "coordinator-c4-7 2026-09-16T08:29:02.894Z"
---

# A deferred tool costs its one-line summary, not its schema

Every exposed tool costs its full schema on every request, so cost grows with the catalog, not with use.

Withhold the schema of a tool that is not hot and list it as one line: its name and what it is for. A deferred tool is not disabled; an explicit restore call makes it directly callable for the rest of the session. A tool without a summary is listed by name alone, never by its description. A tool can opt out of deferral, and naming a tool in an explicit allowlist counts as restoring it.

Scope: the MCP listing (`tools/list` of the mcp cartridge), which "the request" below means. The disposition is a contract carried by descriptor `summary` and `defer` plus a consumer-side `hot` set. mcp's README section `## Deferred tools` is the canonical contract statement other boards cite. Other listings apply it in their own boards.

## Acceptance

- [ ] A deferred tool's schema is absent from the request and its one-line summary is present; the request's declared tools are exactly the hot set, anything restored, and the `tools` meta-tool.
- [ ] Restoring a deferred tool by name makes it directly callable for the remainder of the session without a further restore.
- [ ] A tool declaring no summary is listed by name alone, and its description does not appear in the composed prompt.
- [ ] A tool that opts out of deferral, and a tool named in an explicit allowlist, both arrive with their schema and need no restore.
- [ ] The band is disableable, and disabled the listing is byte-identical to the listing before the band.
- [ ] The withheld and kept byte counts are reported for a fixture catalog, and composition is tested offline by the mcp unit suite (`cargo test --lib band_`).

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/tools/band.ts`; details in `specs/spec01.md`.

The band ships off (`band=false`), which is also the rollback. Turning it on by default belongs to `@root/the-stdio-bridge-pushes-tools-list-changed-so-a-deferred-tool-restore-reaches-every-client`, because a client that does not re-list never sees a restore. `@harness/reflex-tool-audit-loop` needs this PRD for the contract only.

Gates, cwd `/Users/feb/dev/cartridge`: `just check mcp` (green at `6f06acd`). `just test mcp` is red at base (2 live-fixture tests, tracked by `@mcp/the-mcp-live-catalog-tests-settle-at-base`), so the proof is `cargo test --lib band_` with fmt and `clippy -- -D warnings` in mcp.ctg.

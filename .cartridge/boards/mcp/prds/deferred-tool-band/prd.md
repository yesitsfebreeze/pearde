---
state: "analyzing"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/mcp.ctg"
work-kind: leaf
canonical-scope: deferred-tool-band
claim: "coordinator-c4-3 2026-09-16T08:15:02.016Z"
---

# A deferred tool costs its one-line summary, not its schema

Every tool the composition exposes costs its full schema on every request, whether or not the session will ever call it. As cartridges are added — and the port programme adds several — that cost grows with the catalog rather than with what a session does.

Withhold the schema of a tool that is not in the hot set, and list it instead as one line: its name and what it is for. A deferred tool is not disabled — a caller restores it with an explicit call and it is directly callable for the rest of the session. The line is what makes deferral safe, so a tool without one is listed by name alone rather than having its full description smuggled into the prompt in place of a summary.

A tool can opt out of deferral, and naming a tool in an explicit allowlist counts as restoring it.

## Acceptance

- [ ] A deferred tool's schema is absent from the request and its one-line summary is present; the request's declared tool schemas are exactly the hot set plus anything restored.
- [ ] Restoring a deferred tool by name makes it directly callable for the remainder of the session without a further restore.
- [ ] A tool declaring no summary is listed by name alone, and its description does not appear in the composed prompt.
- [ ] A tool that opts out of deferral, and a tool named in an explicit allowlist, both arrive with their schema and need no restore.
- [ ] The band is disableable, and disabled every tool arrives with its schema.
- [ ] The withheld and kept byte counts are reported for a fixture catalog, and composition is tested offline in `just test mcp`.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/tools/band.ts` (verified present in the module at survey), which stamps every registered tool at the one registration choke point and lists deferred tools by their one-line snippet, with a meta-tool to restore them. Upstream reports roughly 17KB of schema withheld against 2.5KB of listing kept on its own surface; measure this composition's own figure rather than inheriting that one.

Reconcile at implementation with `@root/the-proxy-never-teaches-one-tool-twice` and `@root/every-enabled-tool-ships-a-contract-probe`, which touch the same exposure surface, and with `@root/agents-query-the-tool-graph`. Pairs with `@harness/reflex-tool-audit-loop`, the measured half; land this first.

Gates, cwd `/Users/feb/dev/cartridge`: `just test mcp`, `just check mcp`. Not run for this plan.

---
complexity: small
footprint:
  - init.lua
  - cartridge.json
  - .cartridge/tests/policy.rs
  - .cartridge/docs/explain.md
---

# spec01 — Explain through the same immutable policy evaluator

Add a native `policy.explain` service, separately injectable from policy and not
an agent tool. Share one pure evaluator with dispatch decisions. Return the same
decision/reason plus selected rule source, requested operation, a revision bound
to normalized configuration and evaluator version, and authorization metadata.
The revision is a descriptive semantic identity, not an approval or a sandbox
capability. Changed rules change it; invalid replacement retains the old closure.

For allow, the route is ordinary caller dispatch; for deny, none. For ask, report
the trusted caller's optional `authorization_route` (interactive, external or
none), otherwise explicitly unknown. Explanation never asserts that an approval
exists and cannot itself approve anything. It calls no tool or approval service.
Unknown tool catalogs and invalid operations have explicit diagnostics, without
pretending policy knows whether an unlisted provider is installed. Preserve old
policy decisions and configuration semantics. No new default grant or sandbox
behavior is added.

## Acceptance

- [x] Explain and policy agree for allow/ask/deny, deny precedence, operation rules, legacy read/shell/memo/memory behavior and configured/global fallbacks at the same revision.
- [x] Malformed requests, invalid operations and unknown catalogs are diagnosed; caller-supplied authorization metadata is validated. Explanation causes zero target calls and zero approval events.
- [x] Reordered equivalent configuration has the same semantic revision; a changed rule changes it. Invalid replacement preserves the last valid revision and decision; existing native Agent, MCP and proxy tests pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
just test policy
```

The actual pre-change CLI probe is in baseline.json. The separate explain service
was unavailable. Reuse the existing real Lua/native-consumer test crate and its
isolated target. Reverify operation-rules after changing its shared footprint.

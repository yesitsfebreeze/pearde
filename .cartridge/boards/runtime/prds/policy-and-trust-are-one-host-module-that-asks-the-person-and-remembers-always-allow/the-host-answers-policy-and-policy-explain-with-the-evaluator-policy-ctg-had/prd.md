---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/evaluate.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/explain.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/settings.json
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/socket.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/loader/document.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/policy
  - /Users/feb/dev/cartridge/cartridge.ctg/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/settings.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/architecture.txt
---

# the host answers policy and policy.explain with the evaluator policy.ctg had

## Outcome

the host's own plan (`host_plan`, `src/host/plan.rs:57`) declares and listens to `policy` and `policy.explain` the way it already owns `tool.asp`. `Host::bail` answers them in process, the way it answers `asp`, and the socket's `event` branch serves a cartridge's call. The 122-line Lua evaluator is ported to Rust with the same outputs, and its settings are read from the composition's `policy` table on every reconcile, not once. A manifest that declares `events.policy` is refused, the same way `events.asp` is.

Window: until child 2 lands, a live `policy.ctg` fails with "`policy` is already declared by `host`". This is harmless, because the host answers the same way.

## Acceptance

- [ ] Named unit tests reproduce the smoke table with `policy={default="ask",tools={read="allow",docs="allow",write="ask"}}`: read→allow, docs→allow, write→ask, unknown-tool→ask. A `null` request is rejected.
- [ ] Named unit tests cover operation-over-tool precedence, whole-tool deny wins, a malformed request→deny `malformed_request`, and the `policy.explain` `authorization` block for allow, deny and ask with each `authorization_route`. The `revision` string is byte-identical to the Lua `policy-evaluator:3|…` form.
- [ ] A changed `policy` table in `config.lua` changes the next answer after a `reload`, with no daemon restart. An invalid table is refused and the previous rules stay in force.
- [ ] `src/policy/README.md` exists in the fresh-eyes shape.

## Provenance

Child 1 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.

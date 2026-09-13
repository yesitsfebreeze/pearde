---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: launch-authority
---

# launch-authority — Discovery, direct, resolver and nested launches use trusted host-resolved policies while preserving scoped wire behavior and descendant teardown.

Limit this item to mediation of discovery/direct/resolver/nested process starts by the trusted host. First verify whether Host::on_reload is already restored; retain that check as a compatibility prerequisite, and create a separately bounded spec only for a demonstrated remaining reload gap. Do not merge unrelated SDK restoration into launch-policy implementation.

## Acceptance

- [ ] Forged policies/arbitrary command requests are refused, while installed identities resolve against authenticated logical scope.
- [ ] The three previously observed bypass routes and distinct-grant nested launches run through the real command constructor; private child services and descendant teardown retain their behavior.
- [ ] Current Rust/Lua wire, reply correlation, event and reload fixtures pass at the same integrated SDK revision; old patch paths are evidence references, not blindly applied changes.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [command-adapter](../../../.pearde/prds/the-sandbox/command-adapter/prd.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `launch-authority`; maximum five rounds.

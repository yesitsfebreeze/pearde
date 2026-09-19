---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs:
  - '@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/a-consumer-raises-an-approve-or-input-request-and-a-person-answers-it-from-the-command-line'
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/always.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/evaluate.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/request.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/request.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/args.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/policy
  - /Users/feb/dev/cartridge/cartridge.ctg/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/settings.txt
---

# the person can always-allow an operation and revoke it later

## Outcome

`answer <id> always` resolves the request as allowed and stores a rule `{requester, tool, op}`. The rule lives in a 0600 file under `$CARTRIDGE_HOME/policy/<project-hash>.json`, next to the trust store. The evaluator consults stored rules before it returns `ask`. `cartridge request rules` lists them and `cartridge request revoke <rule>` removes one.

## Acceptance

- [ ] Named test: after `always`, the next matching `policy.request` from the same requester and operation is allowed without a pending entry. A different requester or op still asks.
- [ ] Named test: `always` on a `trust` or `secret` request is refused, and the request stays pending.
- [ ] Named test: after `revoke`, the same request asks again. The rule list survives a host restart.

## Provenance

Child 5 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.

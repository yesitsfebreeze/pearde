---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs:
  - '@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/a-consumer-raises-an-approve-or-input-request-and-a-person-answers-it-from-the-command-line'
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/trust.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/trust/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/trust
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/trust.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/project.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/host.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/setup.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/loader/document.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lua/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/settings/files.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/cli/trust.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/policy
  - /Users/feb/dev/cartridge/cartridge.ctg/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md
---

# a changed cartridge raises a trust request from the running daemon instead of staying failed

## Outcome

when `reconcile` marks a slot failed with a trust refusal (`host/mod.rs:348-354`), the host raises a `trust` request carrying the paths and digests. An allow runs `trust::record` on the cartridge root and `replace(id)`. `cartridge trust --ask` and its terminal prompt (`cli/trust.rs:67-165`), and the `ask` call on project open (`cli/project.rs:20`), are deleted. An untrusted project's `init.lua`/`config.lua` also becomes a request from a daemon that starts with the host alone.

## Acceptance

- [ ] Named test: editing a trusted fixture cartridge's manifest yields one pending `trust` request naming the file and its new digest. Allowing it leaves the cartridge active without a daemon restart, and denying it leaves it failed with the refusal.
- [ ] `grep -rn 'read_line\|IsTerminal' src/cli/trust.rs src/cli/project.rs` finds nothing, and `cartridge trust --ask` is an unknown flag.
- [ ] Under `CARTRIDGE_YOLO=1` no trust request is raised (today's yolo behaviour holds), which a named test checks.

## Provenance

Child 4 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.

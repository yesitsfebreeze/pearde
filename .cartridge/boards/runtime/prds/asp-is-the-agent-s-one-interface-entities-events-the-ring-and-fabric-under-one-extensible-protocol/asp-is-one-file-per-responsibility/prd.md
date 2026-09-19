---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp
commit: "324f36e35f1c15aad5e2e4e7e3fa8e9d869d7e33"
---

# asp is one file per responsibility

## Outcome

`cartridge.ctg/src/asp` has one file per responsibility, as the user asked on 2026-09-19 ("also dont create monoliths, one file per responsability", now `system/one-file-per-responsibility.md`). `mod.rs` had grown to 650 lines holding the registry, admission, the merge, the base's own contributions, the provider fan-out, expand, search, the tool envelope and the service. It is now `mod.rs` (the service and its constants), `registry.rs`, `admit.rs`, `world.rs`, `own.rs`, `ask.rs`, `expand.rs`, `search.rs`, `tool.rs`, `rank.rs` and `protocol.rs`, and the tests are one file per behaviour under `.cartridge/tests/unit/src/asp/`. The move changes no behaviour.

## Acceptance

- [x] Every ASP test still passes after the move, and the whole library suite passes.
- [x] No file under `src/asp` holds more than one responsibility, and each opens with a sentence naming it.

---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: extension-loader-plugin-tree
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
---

# extension-loader-plugin-tree

A reload whose new declaration is refused keeps the old node serving. In [host/mod.rs](../../../../../../cartridge.ctg/src/host/mod.rs), `replace_locked` computes `plan` and then calls `stop_slot` before looking at whether the plan is `Err`. Catalogue refusals (`plan::unmatched`, clashes) are only applied later, in `rewire`, to slots that have already stopped. `reconcile` likewise puts entries with a refused plan into `stale` and stops them. In each case a broken `cartridge.json` edit takes a working cartridge down. Unchanged entries already stay running across `reconcile`.

Scope is refusal at planning, before anything is disposed: the candidate plan is checked on its own and against the current catalogue before `stop_slot` runs. A plan that is valid but whose node then fails to start still fails: the socket path is exclusive, and overlapping handoff is out of scope. Status and lifecycle report it with the last stderr lines, as today.

## Acceptance

- [ ] A source edit to a running cartridge that makes its document unreadable, or names an undeclared event, leaves that node `active` on its current generation. `status` and `lifecycle` carry the refusal.
- [ ] The same refusal arriving through an `init.lua`/`config.lua` change in `reconcile` leaves the running entry serving. Removing the entry still stops it.
- [ ] Fixing the document afterwards replaces the node exactly once. Dependents keep working, as `a_restart_keeps_its_dependents_working` shows.
- [ ] A valid plan whose node fails to start ends `failed` with its error. No second node or stale socket is left behind.

## Proof and recovery

First add a failing test next to `a_restart_keeps_its_dependents_working` in [host.rs tests](../../../../../../cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs). Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. Not run. Rollback: restore stop-then-plan ordering.

## Dependencies and review

No hard prerequisites. The acceptance overlaps `documents-own-live-processes/document-sidecar-lifecycle` ("replacement preserves the old usable service"); this leaf owns refusal at planning. [Review](review.md): inherits 2 rounds.

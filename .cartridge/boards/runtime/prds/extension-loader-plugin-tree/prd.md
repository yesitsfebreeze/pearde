---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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
needs:
- "@memory/extension-plugin-config-and-update"
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

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--extension-loader-plugin-tree.md` (status open, claim b424ceba 2026-09-09 15:55, estimate 1d). The PRD state above is authoritative.

> the loader plugin — entries `{ id, name, config, disabled, isolate, intercept }` from a catalog, mounted as a group and reconciled per field on every apply, so the same rows twice restart nothing

### Do

- `Catalog`: `HashMap<String, Arc<dyn Plugin>>` built by the host; `name` in
  an entry is the catalog key (Cordis's `url`).
- `Entry { id: String, name: String, config: serde_json::Value, disabled: bool, isolate: BTreeMap<String, IsolateSpec>, intercept: BTreeMap<String, serde_json::Value> }`
  with `IsolateSpec::{Local, Global(String)}` (Definition 81). A `group`
  entry's `config` is `Vec<Entry>`.
- `Loader` is a plugin providing `loader`. `loader.apply(entries).await`
  reconciles the live group against the rows by `id`: a new id mounts (`ctx.plugin` on the loader's
  context derived with the entry's `isolate` and `intercept`); a missing id
  disposes; `disabled` flipped on disposes and off mounts; `config` changed
  is `fiber.update(config, true)`; `name` or `isolate` changed rebuilds the
  entry (dispose, then mount) — the realm move of Algorithm 7 is the
  upgrade path when a rebuild is measured to hurt, and the code says so;
  `intercept` changed rewrites the derived context's map in place. A
  mount failure unwinds the rows added in that apply in reverse and keeps
  the previous rows, reporting every error.
- Events `loader/config-update` (emit, after an apply) and
  `loader/entry-init { id }` (emit, per mount); `ctx.loader.locate(fiber)`
  answers the entry id owning a fiber. `fiber.entry()` exposes it.
- A plugin that disposes its own fiber marks its entry `disabled = true`
  in the loader's copy of the rows, so the next apply does not remount it.

### Check

`cargo nextest run -p extension` passes with tests proving: three rows mount
three fibers under the loader; applying the identical rows again restarts no
fiber (`internal/status` sees no transition); a `config` change runs one
`update` and the plugin sees the new value; `disabled: true` disposes and
`false` remounts; removing a row disposes it; a row with `isolate: { counter: Local }`
does not see the loader context's `counter` provider; a group row's child
rows reconcile by id; a mount whose `apply` fails leaves the earlier rows of
that apply unmounted and the previously mounted rows `Active`.

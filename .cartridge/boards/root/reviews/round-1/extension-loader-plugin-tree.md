---
kind: work
level: 10
status: open
claim: b424ceba 2026-09-09 15:55
estimate: 1d
needs: [[extension-plugin-config-and-update]]
description: the loader plugin — entries `{ id, name, config, disabled, isolate, intercept }` from a catalog, mounted as a group and reconciled per field on every apply, so the same rows twice restart nothing
read_when: "mounting plugins from configuration, or touching how a config change reaches a running fiber"
---

# extension-loader-plugin-tree

## Do

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

## Check

`cargo nextest run -p extension` passes with tests proving: three rows mount
three fibers under the loader; applying the identical rows again restarts no
fiber (`internal/status` sees no transition); a `config` change runs one
`update` and the plugin sees the new value; `disabled: true` disposes and
`false` remounts; removing a row disposes it; a row with `isolate: { counter: Local }`
does not see the loader context's `counter` provider; a group row's child
rows reconcile by id; a mount whose `apply` fails leaves the earlier rows of
that apply unmounted and the previously mounted rows `Active`.

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
review-status: superseded-recommend-retire
canonical-scope: plugins-from-memory-toml
needs:
- "@memory/memory-daemon-boots-a-root-context"
- "@runtime/extension-loader-plugin-tree"
---

# plugins-from-memory-toml

Reconcile the old plugin configuration proposal with current cartridge profile/manifest ownership. Only database/endpoint settings stay in memory configuration; optional external adapters are composed by runtime. Preserve the old proposal as history rather than adding memory plugins reload back.

## Acceptance

- [ ] Every old plugin row requirement maps to current owner/profile semantics or an explicit obsolete field.
- [ ] Duplicate IDs, unknown providers and invalid candidate configuration fail before replacing a usable composition.
- [ ] Disabled external adapters stop only their effects, while standalone memory ingest/recall and store configuration remain compatible.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `plugins-from-memory-toml`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--plugins-from-memory-toml.md` (status open, estimate 1d). The PRD state above is authoritative.

> `[[plugin]]` rows in memory.toml are loader entries mounted at boot from the binary's catalog, listed by `memory plugins`, and reconciled live by `memory plugins reload`

### Do

- `config::PluginsConfig { plugins: Vec<PluginRow> }` on `Config` with
  `PluginRow { id, name, config: toml::Table, disabled, isolate: BTreeMap<String, IsolateSpec> }`;
  `Config::validate` refuses a duplicate `id` and a `name` the catalog does
  not carry (the catalog's names are a `const` list the config crate can
  see, or validation moves to the loader plugin and reports through
  `loader/entry-init`'s failure).
- `commands::catalog() -> extension::Catalog` names every plugin the binary
  carries; the first entries are the built-ins of
  [memory-daemon-boots-a-root-context](../../../memory/prds/memory-daemon-boots-a-root-context/prd.md) under their names, so a row can
  disable `memory-app` on a headless box, and `echo` — a test plugin providing
  nothing and registering one `plugins/echo` listener — so the loader can be
  exercised without a real subsystem.
- `run_server` mounts the loader after the built-ins and applies the rows.
- RPC and command `memory plugins reload`: re-read `memory.toml`, `loader.apply`
  the new rows, print what changed.

### Check

`just test` green. Unit: a `memory.toml` with two rows parses and a duplicate
id fails validation naming it. E2E (`tests/e2e`): a daemon started with an
`echo` row lists it `Active` under `loader` in `memory plugins`; rewriting
the row to `disabled = true` and running `memory plugins reload` lists it
gone and the listener no longer answers.

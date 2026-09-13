---

kind: work
level: 10
status: open
estimate: 1d
needs: "[[@prd/work/memory--memory-daemon-boots-a-root-context.md]] [[@prd/work/memory--extension-loader-plugin-tree.md]]"
description: "`[[plugin]]` rows in memory.toml are loader entries mounted at boot from the binary's catalog, listed by `memory plugins`, and reconciled live by `memory plugins reload`"
read_when: "switching a plugin on or off in memory.toml, or adding a plugin the binary carries"
---

# plugins-from-memory-toml

## Do

- `config::PluginsConfig { plugins: Vec<PluginRow> }` on `Config` with
  `PluginRow { id, name, config: toml::Table, disabled, isolate: BTreeMap<String, IsolateSpec> }`;
  `Config::validate` refuses a duplicate `id` and a `name` the catalog does
  not carry (the catalog's names are a `const` list the config crate can
  see, or validation moves to the loader plugin and reports through
  `loader/entry-init`'s failure).
- `commands::catalog() -> extension::Catalog` names every plugin the binary
  carries; the first entries are the built-ins of
  [[@prd/work/memory--memory-daemon-boots-a-root-context.md]] under their names, so a row can
  disable `memory-app` on a headless box, and `echo` — a test plugin providing
  nothing and registering one `plugins/echo` listener — so the loader can be
  exercised without a real subsystem.
- `run_server` mounts the loader after the built-ins and applies the rows.
- RPC and command `memory plugins reload`: re-read `memory.toml`, `loader.apply`
  the new rows, print what changed.

## Check

`just test` green. Unit: a `memory.toml` with two rows parses and a duplicate
id fails validation naming it. E2E (`tests/e2e`): a daemon started with an
`echo` row lists it `Active` under `loader` in `memory plugins`; rewriting
the row to `disabled = true` and running `memory plugins reload` lists it
gone and the listener no longer answers.

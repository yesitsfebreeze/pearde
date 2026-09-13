---
kind: work
level: 10
status: done
description: an empty `data_dir` or `intake.dir` in memory.toml makes every watched path a denied path, so the file watcher silently ingests nothing and no validation refuses it
read_when: "debugging a watcher that sees nothing, or adding a config check"
---

# an-empty-denied-path-denies-the-whole-tree

## Do

`watcher_denied_paths` (`src/commands/src/commands_serve.rs:528-534`) hands the
watcher three off-limits prefixes: `cwd.join(".memory")`, `cwd.join(&cfg.intake.dir)` and
`PathBuf::from(&cfg.data_dir)`. `IgnoreRules::with_denied` canonicalizes each,
keeping the original when that fails, and `ignored` refuses any path where
`path.starts_with(d)` (`src/util/src/watcher.rs:165`).

Both configurable values are unchecked, and an empty string in either one
denies everything. Measured with `rustc`: `cwd.join("")` equals `cwd`, so
`intake.dir = ""` makes the project root itself a denied prefix;
`PathBuf::from("").canonicalize()` is an error, so `data_dir = ""` survives
`unwrap_or` as the empty path, and `Path::new("/any/file").starts_with("")` is
`true`. Either way every event and every boot-scan entry is refused, the
watcher ingests nothing, and there is no log line and no counter — the daemon
reports `ingest: queue 0` and `degraded: 0 failures` and looks healthy.

`Config::validate` checks `embed.url`, `embed.model`, `reason.url` and
`reason.key` for emptiness (`src/config/src/config.rs:196-227`) and neither
`data_dir` nor `intake.dir`. [[config-rejects-unknown-keys]] means a *misspelled*
key fails the boot at exit 78; an empty valid one takes the whole record ingest
down quietly, which is the worse half. Refuse both empties in `validate`, beside
the four already there.

**Done 2026-09-06.** `Config::validate` refuses an empty `data_dir` and
`IntakeConfig::validate` refuses an empty `dir`, each naming its key and what an
empty one does. The two checks sit in different impls because that is where the
two values live, so the intake one runs through the existing
`intake: {e}` wrapper.

## Check

A `memory.toml` with `data_dir = ""` fails the boot naming the key, and so does
one with `intake.dir = ""`; a unit test in `src/config/src/tests/config_test.rs`
asserts both, and the existing empty-URL refusals still pass.

**Done 2026-09-06.** `Config::validate` refuses an empty `data_dir` with
"data_dir is required (empty denies every watched path)" (`config.rs:209-210`)
and `IntakeConfig::validate` refuses an empty `dir` with the same clause
(`:843-844`), both naming the key as the Check asks.
`validate_refuses_an_empty_denied_path` (`config_test.rs:185-197`) asserts both
messages, and `validate_requires_embed_and_surfaces_sub_config_invariants`
beside it still holds the empty-URL refusals. Held by
`validate_refuses_an_empty_denied_path`, with
`validate_requires_embed_and_surfaces_sub_config_invariants` unchanged beside
it.

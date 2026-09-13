---
kind: work
level: 10
status: done
description: the file watcher walks its root on start and ingests what the store does not hold, so a cold store carries the record before it serves anything
read_when: "asking how a cold store gets the record"
---

# watcher-scans-at-boot

## Do

`spawn_file_watcher` (`src/commands/src/commands_serve.rs:536`) builds the
roots, the `IgnoreRules` and the `FileWatcher` synchronously before `run_server` binds
the socket, then hands the watcher and a `MemoryFileWatcherSink` to
`ingest::file_watcher::run`, which only drains events. The boot scan belongs
in that same synchronous stretch, after the sink is built and before the
spawn: walk each root, skip what `IgnoreRules::is_ignored` rejects, and feed
every file through `IngestPipeline::handle` as a `WatchEvent` with
`WatchKind::Created` — the same call a live change makes, so a scanned file
and a changed file remain one code path. The content-hash dedup makes the walk
idempotent, so a warm store writes nothing.

The walk reads and embeds every part it finds, so it does not hold the bind:
spawn the scan as its own task once the sink exists, ahead of the drain, and
let the socket bind while it runs.

Retire the part that said the watcher replays nothing in the same change; it is
`the-watcher-walks-its-roots-at-start` that now carries what a boot does, and
git holds the sentence it corrects.

Done 2026-09-05: `ingest::file_watcher::scan` walks the roots depth-first,
skipping a directory by `IgnoreRules::is_ignored_dir` — a new call, because
`is_ignored` asks the file question and a `target/` pattern needs the
directory one, and gitignore never looks at a path's ancestors. Each file
becomes a `WatchKind::Created` event through `IngestPipeline::handle`, the
same call a live change makes. `spawn_file_watcher`
(`src/commands/src/commands_serve.rs:554-587`) builds a second `IgnoreRules` for
the scan (the type is not cloneable and `FileWatcher::new` takes the watch's) and
spawns it beside the drain, so the socket binds while the walk reads.
`the-watcher-walks-its-roots-at-start` carries the retirement line, and the
hole the walk repeats.

## Check

`just test` green, plus an e2e test in `tests/e2e/file_watcher.rs`: a store
with an empty graph and a populated watch root holds every part after the
daemon starts, and a second start writes no new entity.

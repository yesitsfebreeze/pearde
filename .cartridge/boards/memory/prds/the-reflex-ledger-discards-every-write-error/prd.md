---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `Reflex::save` writes the ledger with `let _ = std::fs::write(...)` and drops the result, so the file that decides which tools an agent host is shown can stop persisting and nothing counts it, warns or prints a line

## Do

`Server::invoke` records every operation except `health` into the reflex ledger
(`src/rpc/src/server.rs:123-126`), and [[reflex-measures-the-surface]] is why
that matters: the ledger's counts pick the cold tool `memory mcp` draws at
handshake, and `reflex rate` writes verdicts that keep an operation off the
surface for thirty days.

`Reflex::save` (`src/rpc/src/reflex.rs:74-81`) is:

```rust
if let Some(dir) = self.path.parent() {
    let _ = std::fs::create_dir_all(dir);
}
if let Ok(s) = serde_json::to_string_pretty(state) {
    let _ = std::fs::write(&self.path, s);
}
```

Three failures are swallowed: the directory create, the serialization, and the
write. A read-only data dir, a full disk, or a path whose parent is a file all
leave the in-memory counts advancing and the file frozen at whatever it last
held — and `record` returns `()` either way, so `invoke` cannot know and the
next process starts from a stale ledger. The rate verdicts go the same way,
which is the half that changes behaviour rather than statistics.

This is the shape [[the-tick-persist-drops-its-error]] closed on the other
side of the tree — a persist whose `Result` went nowhere while the write it
declined was logged — and that fix is the precedent: it is now counted, warned
and on the `degraded:` line. The same three lines apply here.

Count a failed ledger write on the per-store counters, warn once with the path
and the error, and print it beside the rest ([count-the-shed-tick-tasks](../count-the-shed-tick-tasks/prd.md) is
the pattern for the counter, `degradation_lines` for the surface). The
serialization arm cannot fail for this state and should say so by
`expect`-ing rather than silently skipping the write.

## Acceptance
A ledger whose file is made unwritable increments a counter and produces one
warning naming the path; `memory health` shows the count; `just all` green.

Planning recheck 2026-09-07: `Reflex::save` still discards directory/write
errors and silently skips serialization failures. The existing per-store
`graph::Counters`, owned by `GraphGnn.counters`, is the counter owner, not a
new process-global statistic. Production construction in
`src/commands/src/commands_serve.rs` already has the graph when it opens the
ledger. Thread that counter handle through construction and test helpers;
carry the added field through health stats, the tolerant wire response and
CLI degradation rendering. Keep the work one end-to-end failure signal,
not a new ledger format or retry policy. A file in place of the destination's
parent is a deterministic fixture for failed persistence without chmod/root
assumptions. Repeated failures should count each failed save while the warning
policy remains the memo's once-only requirement. Run its health observation
and full gate before moving status.

Done 2026-09-08, lane `herd-drive-p4-3`. `Reflex::save` (`src/rpc/src/reflex.rs`)
now `expect`s the serialization, chains the directory create and the write into
one `Result`, counts every failure on a `write_failed: AtomicU64` owned by the
`Reflex` itself — the planning recheck's `graph::Counters` route would have
threaded a handle through `commands_serve.rs`, which this lane does not own,
and the ledger is not the graph's — and warns once, on the first failure, with
the path and the error. The count rides `ReflexHealth::write_failed`
(`src/transport/src/memory_rpc.rs`, `#[serde(default)]`), `Server::reflex_health`
fills it, and `reflex_health_lines` in `commands_admin.rs` goes loud on it and
appends `; N failed ledger writes`. The Check's first clause runs as
`an_unwritable_ledger_counts_every_failed_save_and_warns_once_with_the_path`
in `server_reflex_test.rs`: a file where the data dir should be, four failed
saves, count 4, one warning naming `reflex.json`, read back off a scoped
`tracing_subscriber` (rpc dev-dep). `just check` green in the lane; `just all`
is the caller's serial per-lane run.

---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/sessions.ctg"
work-kind: leaf
needs:
  - '@sessions/file-drift-awareness'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/sessions-contributes-agents-and-their-activity-to-asp'
footprint:
  - /Users/feb/dev/cartridge/sessions.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/persist.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/ops.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/shared.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/config.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/host.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/channels.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/retention.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/mapping.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/roster.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/context.rs
  - /Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/unit/main/tests.rs
---

# sessions src is one file per responsibility

## Outcome

`sessions.ctg/src/lib.rs` is 1304 lines (`wc -l sessions.ctg/src/lib.rs`,
verified 2026-09-19) and answers for at least five distinct jobs that already
have sibling modules for everything else the crate does (`channels.rs`,
`retention.rs`, `mapping.rs`, `roster.rs`, `context.rs`, `mailbox.rs`, ...).
Each job moves to its own file, and `lib.rs` shrinks to module wiring, the
shared `Result` alias and the Lua entry points that must live at the crate
root. Separately, 32 of the 44 `.unwrap()` calls counted across
`sessions.ctg/src` today are lock/RwLock-poison unwraps on shared state
(`self.state`, `self.mutation`, `self.gates`, `store.retention_fault`,
`self.connection`) — a poisoned lock (a panic while any caller held it) turns
into a second panic on the next unrelated caller instead of a reported error.
Serves ranking row 1 of `.cartridge/memos/ranking/cartridges.md` (sessions:
"51 unwraps in shared state; `src/lib.rs` 1304 lines", needed by agent, fs,
harness, live, mcp, proxy).

## Responsibilities found in `lib.rs`, with target files

1. **Persistence primitives** — `Buffer`, `Session`, `File` structs, `Store`
   struct, `Fault`, `PersistError`, `ensure_dir`, `temporary`, `now`, `field`,
   `strip`, `validate_record`, `validate_agent`, `load`, `read_snapshot`,
   `decode_snapshot`, `install`, `check_fault`, `save`, `sync_dir`, `publish`,
   `publish_checked`, `repair_empty` (`lib.rs:51-507`). Target: `src/persist.rs`.
2. **Session/buffer operations** — `sessions`, `sessions_with_lineage`,
   `buffers`, `read`, `session`, `buffer`, `is_transcript`, `touched`,
   `sessions_inner`, `mailbox_buffer`, `buffers_inner` (`lib.rs:509-939`).
   Target: `src/ops.rs`.
3. **Concurrency wrapper and dispatch** — `SharedStore`, `gate`, `execute`
   (`lib.rs:944-1131`). Target: `src/shared.rs`.
4. **Host config parsing** — `Config`, `store_dir`, `parse_config`
   (`lib.rs:1140-1183`). Target: `src/config.rs`.
5. **Lua host glue** — `STORE`, `answer`, `notify`, `start`, `store()`,
   `sessions_op`, `buffers_op`, the `sessions` Lua table (`lib.rs:1185-1281`).
   Target: `src/host.rs`.

After the move, `lib.rs` keeps only: the `mod` declarations, `DOCUMENT`, the
`pub type Result` alias, and whatever thin glue the split leaves that must sit
at the crate root by Rust's own rules (nothing else).

## Acceptance

- [ ] `wc -l sessions.ctg/src/lib.rs` reports 150 lines or fewer.
- [ ] `wc -l sessions.ctg/src/{persist,ops,shared,config,host}.rs` reports no
      file over 500 lines, and each file's content matches only the
      responsibility named for it above (no stray query logic in
      `persist.rs`, no Lua glue outside `host.rs`).
- [ ] `rg -c '\.(lock|read|write)\(\)\.unwrap\(\)' sessions.ctg/src/*.rs` sums
      to 0 (today: `context.rs` 1, `roster.rs` 1, `channels.rs` 10,
      `retention.rs` 6, `mapping.rs` 5, `lib.rs`/`shared.rs` 9 — 32 total,
      verified 2026-09-19). Each is replaced with a handled `Result::Err`
      (recover the poisoned guard with `into_inner()` or return a named
      fault), never a fresh `panic!` or a silent `.unwrap_or_default()` that
      hides the poison.
- [ ] A new test poisons a `SharedStore` lock deliberately (panic on a
      spawned thread while holding `self.state`/`self.mutation`/a `gate`) and
      asserts the next call through `execute` returns `Result::Err` rather
      than panicking the caller.
- [ ] Every existing test module reachable from the crate today still passes
      unmodified in behavior: `tests`, `repair_tests`, `mapping_tests`,
      `retention_tests`, `mailbox_tests`, `change_records_tests`
      (`sessions.ctg/.cartridge/tests/unit/main/*.rs`).

## Proof and recovery

Starting files: `sessions.ctg/src/lib.rs` (split source), plus
`channels.rs`, `retention.rs`, `mapping.rs`, `roster.rs`, `context.rs` (the
lock/poison unwrap fix — `mailbox.rs`'s one unwrap is a JSON-shape unwrap, not
a lock, and is out of scope here). No fixture needs creating; the poison test
is new but runs against the existing `Store`/`SharedStore` fixtures already
built by the current test modules.

Before touching code, capture the baseline so the acceptance boxes measure a
real move rather than restating the current numbers:
`wc -l sessions.ctg/src/*.rs` and
`rg -c '\.(lock|read|write)\(\)\.unwrap\(\)' sessions.ctg/src/*.rs`, both from
`/Users/feb/dev/cartridge`.

Gates, cwd `/Users/feb/dev/cartridge`: `just check sessions`, `just test
sessions`, `just audit sessions`, `just isolation`. All four must report
nothing new for sessions after the split; the compatible fallback is that
`Store`/`SharedStore`'s public op surface (`sessions`, `buffers`, `execute`)
keeps its exact signature, so no caller cartridge (agent, fs, harness, live,
mcp, proxy) observes a change.

## Dependencies and review

Two live rows already claim parts of the exact files this split touches, and
both are strictly upstream of the split, not sideways from it:

- `@sessions/file-drift-awareness` (open, no claim, priority 50) reserves
  `src/drift.rs`, `src/lib.rs`, `src/changes.rs`, `src/limits.rs`,
  `src/change_record.rs`, `cartridge.json`, `README.md`,
  `.cartridge/help.md`, `.cartridge/tests/unit/main/drift_tests.rs` — it adds
  a new `drift.rs` module and wires it into `lib.rs`.
- `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/sessions-contributes-agents-and-their-activity-to-asp`
  (open, priority 100) reserves `src/asp`, `src/lib.rs`, `src/changes.rs`,
  `src/change_record.rs`, `cartridge.json`, `init.lua`, `README.md`,
  `.cartridge/help.md`, `.cartridge/tests/unit/asp.rs` — it adds a new `asp`
  provider module and wires it into `lib.rs`.

Both land new code into `lib.rs` before this PRD would move `lib.rs`'s
existing code out. Splitting first would force both of those rows to rebase
their `lib.rs` wiring onto files that no longer exist at the paths they
expect; landing them first means this split runs once, against the settled
shape of `lib.rs`, and only re-touches `lib.rs` itself (not `changes.rs`,
`change_record.rs`, `cartridge.json`, `README.md` or `.cartridge/help.md`,
none of which this PRD's footprint lists). `needs` is set to both for that
reason; this PRD does not modify either of their records. Everything else in
this footprint (`persist.rs`, `ops.rs`, `shared.rs`, `config.rs`, `host.rs`,
and the lock-unwrap fix in `channels.rs`/`retention.rs`/`mapping.rs`/
`roster.rs`/`context.rs`) is new or untouched by either row, so no further
footprint overlap exists on the sessions board today.

---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/memory.ctg"
capability-owner: memory
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- ".cartridge/tests/unit/src/cartridge/engine_test.rs"
commit: "1351865eb0e787cf819456aaa201c18eacf74406"
---

# Memory runs once in the daemon and attached instances never hit the writer lock

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies memory as
must-exist-once-per-project: `writer.lock` means every call on a second host
fails with `another memory writer holds this data dir`, including its ledger
appends (this is the exact failure the ledger item depends on avoiding).

## Outcome

Memory is composed exactly once, in the project daemon. An attached instance's
memory calls (including `ledger append` from the proxy) go through the
daemon's node and succeed; no second node ever exists to hit the writer lock.

## What changes

This child mostly verifies the shape rather than changing memory itself:

- With the host-attach contract in force, an instance never starts a second
  memory node, so the writer lock is never contended by construction.
- The ledger condensing loop (every 60s, holding off 5 min after any import
  call) runs only in the daemon's memory node; verify a short-lived attached
  `run`/`call` does not start or interfere with it.
- If any memory path still assumes process-exclusivity beyond the file lock,
  record it and fix it here (e.g. attach-mode memory must not try to take the
  writer lock read-only; it is the same node).

## Acceptance

- [x] memory.ctg's share of "exactly one memory node, no `another memory
      writer holds this data dir`": the cartridge takes the writer lock once in
      `Engine::open` and holds it for the node's lifetime, a second local
      service over the same data dir is refused with that exact message and
      opens no engine, and the attached shape never asks for the lock at all.
      (The daemon-wide count is delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.)
- [x] Two callers of the one node see one store: the writer serves ingest,
      query and ledger from a single `Engine`, and a second service that would
      have been the "other instance" gets no engine of its own to diverge in.
      (The cross-instance `ingest`-then-`query` round trip belongs to the
      composed test.)
- [x] The condensing loop belongs to the writer: `spawn_ledger` is called from
      exactly one place, the end of `Engine::open`, after the lock is taken and
      into an `Engine` that holds it — so a service refused the lock, and an
      attached service, run no condensing pass.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. The audit premise held in
part: a second **composed** memory node over one data dir really is refused
(`src/store/core/src/lock.rs:53-56`, raised at `:112-120`). The PRD's own escape
hatch — "if any memory path still assumes process-exclusivity beyond the file
lock" — was already false: `ServiceConfig::Attached` (`src/cartridge/src/lib.rs:23-29`)
never touches the lock, returning over the owner transport before `status.engine`.
So this child is a regression test, not a production change, exactly as its body
predicted.

Three coordinator edits to the record:

- The footprint listed `src/store/lock.rs`, which **does not exist** — the file
  is `src/store/core/src/lock.rs`, already covered by the `src/` entry, so the
  bogus path was dropped rather than corrected. It gained
  `.cartridge/tests/unit/src/cartridge/engine_test.rs`: this repo
  `#[path]`-includes its unit tests from `src/cartridge/src/lib.rs:581`, so the
  only file the spec changes sat outside the declared footprint and collect
  would have refused it. Same trap as the agent sibling.
- All three acceptance boxes were reworded to what memory.ctg can actually
  prove, using the analyst's proposed wordings verbatim. Boxes 1 and 2 need a
  live daemon, `cartridge run` and a process count — all cartridge.ctg — and are
  delegated to the done attach sibling and the composed test.
- Box 3 was **unsatisfiable as written anywhere**: `{"op":"ledger","action":"status"}`
  returns only per-tier row and byte counts (`src/rpc/src/ledger.rs:289-297`) —
  no pid, no node, nothing about who is condensing. Keeping the literal wording
  would mean adding an owning-pid field, a production change this child's body
  explicitly scopes out. If an operator-visible "who is condensing" is wanted
  later, it is its own PRD.

## Planning note, second entry

2026-09-16, coordinator cartridge-1b, after verifier-1. `src/` was **dropped
from the footprint**, leaving exactly the one file this PRD changes.

The reason is a landing hazard the verifier measured, not tidiness. A peer is
mid-way through vendoring `evidence.rs` into memory.ctg: `Cargo.lock`,
`src/cartridge/Cargo.toml`, `src/cartridge/src/lib.rs`, `src/cartridge/src/source.rs`,
an untracked `src/cartridge/src/evidence.rs` and `.cartridge/tests/unit/src/cartridge/source.rs`
are all uncommitted. With `src/` in the footprint, `collect` would have swept the
three `src/cartridge` files and `evidence.rs` into this receipt while leaving
`Cargo.lock` and the peer's test file outside it — committing a manifest without
its lockfile and `pub mod evidence;` without its test. That is worse than either
landing the peer's work whole or not touching it at all.

The plan never needed `src/`: this PRD's finding was that memory's single-writer
shape is already correct, so the spec's own footprint has always been the single
test file, and `feet()` unions the PRD's and the spec's footprints. Nothing this
PRD asserts about `src/` requires permission to write there.

Box 3 carries one residual from the verifier: the *"after the lock is taken"*
clause is not independently falsifiable — moving `store::lock::acquire` below
`spawn_ledger` compiles and keeps both the guard and the test green. The
call-site-count, end-of-`Engine::open` and holds-the-lock clauses are each
falsifiable and were falsified.

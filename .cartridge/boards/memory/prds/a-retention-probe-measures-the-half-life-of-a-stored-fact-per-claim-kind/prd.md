---
state: "claimed"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/memory.ctg"
claim: "coordinator-8e-impl-2 2026-09-16T22:58:43.675Z"
---

# A retention probe measures the half-life of a stored fact per claim kind

## Outcome

Nobody has measured whether the bank still returns a fact after time and unrelated
ingests have passed over it. The heat model in `src/graph/src/heat.rs` gives every
claim kind its own Weibull curve and every unlabelled entity one seven-day exponential,
but the benches in `.cartridge/tests/integration/bench` only rank a fixed store; none
of them ages one. The probe borrowed here is the one that falsified the
`jrz97619761/test-model-thing` memory claim: compare the answer with and without the
earlier fact, at growing distances, and read the distance at which the two stop
differing.

One runnable eval on the mature fixture: ingest a labelled fact, advance the entity
clocks by a chosen span, push a chosen count of unrelated documents through the tick,
query for the fact at k=10, and record its rank. Repeat with one intermediate touch of
the fact. Report a table with one row per claim kind and one column per span: the
rank, and whether the row was spilled to cold. The half-life per kind is the span at
which recall@10 drops below one half. Run it for both retrieval variants so the default
is chosen on retention as well as rank.

## Acceptance

- [x] `just eval-retention` runs against the mature fixture with fixed entity clocks and prints one table with a row per built-in claim kind plus the unlabelled default.
- [x] Each cell records rank at k=10, cold or hot, with and without one intermediate touch.
- [x] The run is repeatable: a second process against the same vector cache produces identical ranks.
- [x] `RESULTS.md` gains a dated section with the table and the decision it supports, without changing any question or label after seeing scores.

## Landing blocker

2026-09-17, coordinator cartridge-8e. The verified lane commit 717ddae is
collectable (`collect --dry` passes; every Acceptance box in the PRD and
spec01 is ticked on the independent verifier's observed exits: unit tests
8 passed, two `--fake-llm` runs against one shared vector cache byte-identical
after dropping timestamps, report shape 8 rows x 2 variants x 5 span cells
with valid ranks and tiers, RESULTS.md dated section present). Landing is
parked, not failed, because the live `memory.ctg` checkout carries nine
uncommitted paths that are not this PRD's work — `M .cartridge/tests/integration/cartridge.rs`,
`M .cartridge/tests/integration/spill_transparency.rs`,
`M .cartridge/tests/unit/src/cartridge/source.rs`, `M Cargo.lock` (foreign
dependency-dedup hunks, disjoint lines from this lane's own two-line
memory-bench addition), `M src/cartridge/Cargo.toml`, `M src/cartridge/src/lib.rs`,
`M src/cartridge/src/source.rs`, `M src/graph/src/diskann.rs`,
`?? src/cartridge/src/evidence.rs` — and this PRD's footprint is the whole
repository, so a collect would sweep them into this PRD's receipt and the
fast-forward would refuse on the Cargo.lock overlap. The dirt is owned by
another session's/user's in-progress work; do not touch it. Collection
proceeds once that work is committed or moved. The lane at
`boards/memory/.lanes/a-retention-probe-...` holds the verified commit and
must not be removed.

## Landing blocker

2026-09-17, coordinator cartridge-8e. The work is complete and verified:
implementer DONE at lane commit 717ddae (retention subcommand, `just
eval-retention`, span grid [1, 8, 30, 120, 365] days, 24 unrelated docs, real
qwen3-embedding run recorded in RESULTS.md); independent verifier reran all
three Verify blocks in the lane — exit 0 each (8/8 unit tests, two fake-LLM
runs byte-identical apart from volatile fields, RESULTS.md greps). All
Acceptance boxes are ticked on that evidence and `collect --dry` passes.

Collection is blocked by foreign dirt in the live `memory.ctg` checkout, whose
whole repository is this PRD's footprint: nine dirty paths (`Cargo.lock`,
`src/cartridge/Cargo.toml`, `src/cartridge/src/lib.rs`, `src/cartridge/src/source.rs`,
untracked `src/cartridge/src/evidence.rs`, `src/graph/src/diskann.rs`, three
test files). A collect would commit all of it into this PRD's receipt, and the
foreign `Cargo.lock` hunk collides with the lane's own `Cargo.lock` change, so
the fast-forward would refuse even with a narrowed footprint. Not touching,
stashing or committing another session's work. Land when the checkout is clean.

### Landing blocker, re-observed 2026-09-17 by coordinator cartridge-2e

The claim `coordinator-8e-impl-2` is held by a session that `ListAgents` no
longer lists, and it was eight hours old at this check. The lane and the claim
are kept, because the lane at `717ddae` holds the verified work and releasing
the claim would invite another session to collect without knowing it.

Two facts now stand between this PRD and `collect`:

1. `memory.ctg` `main` has moved from the lane's base `1351865` to `47864de`,
   so the lane no longer fast-forwards. It needs a rebase onto `47864de`
   before collection, exactly as the engine-tests PRD did.
2. The lane commit touches `Cargo.lock`, and `memory.ctg`'s live `Cargo.lock`
   carries another session's unrelated dependency-dedup edit (8 insertions,
   85 deletions). The fast-forward would have to overwrite it. Narrowing this
   PRD's footprint to its reviewed spec's file list cannot help, because
   `collect` requires every path the lane commit touches to be inside the
   footprint, and `Cargo.lock` is one of them.

`collect --dry` reports "Would verify, integrate and commit collection
records", so the refusal is not in the engine's preconditions; it is the
working tree. Collect when `git -C memory.ctg status --porcelain` is clean,
after rebasing the lane onto the then-current `main`.

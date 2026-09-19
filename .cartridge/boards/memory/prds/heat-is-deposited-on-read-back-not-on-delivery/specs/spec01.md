---
complexity: mid
footprint:
  - /Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece/src/retrieval_score.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/graph/src/heat.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/config/src/config.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece/src/lib.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/retrieval/src/lib.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/tick/src/tick_queue.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/tick/loop/src/tick.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/tick/loop/src/tick_tasks.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/rpc/src/server.rs
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/unit/src/retrieval/piece/src/tests/retrieval_score_test.rs
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/unit/src/rpc/src/tests/server_query_test.rs
  - /Users/feb/dev/cartridge/memory.ctg/README.md
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench/RESULTS.md
---

# spec01 — Move the access-heat deposit from delivery to read-back

## Base and dependencies

- Base repository: `/Users/feb/dev/cartridge/memory.ctg` at source HEAD
  `3432b13376017be921d745719e0626d6f0b5463c`.
- `@memory/a-retention-probe-measures-the-half-life-of-a-stored-fact-per-claim-kind`
  is `done`; `just eval-retention` and
  `.cartridge/tests/integration/bench/RESULTS.md` exist and are the "before"
  side of Acceptance box 3.
- Other sessions hold `src/store/core/src/lib.rs`, `src/store/core/src/cold.rs`,
  `.cartridge/tests/unit/src/store/core/src/lib/tests.rs`,
  `.cartridge/tests/integration/cartridge.rs` and `src/cartridge/src/lib.rs`.
  None of them is in this footprint and none of them needs to change:
  `get` is already rewritten to `query` at `src/cartridge/src/lib.rs:190`, and
  `context.memory` `read` already reaches that rewrite through
  `src/cartridge/src/source.rs:107-108`.

## Mechanism

`stamp_access` does three things to a delivered row: it stamps `accessed_at`
(the access-order key), increments `access_count` (the QBST boost), and deposits
heat. Only the third is retention. Split it.

1. `src/config/src/config.rs` — `HeatConfig` gains
   `deposit_delivery_fraction: f32`, defaulting to `0.0`: the fraction of
   `deposit_access` a mere delivery earns. This is the PRD's "or a configured
   fraction", and it is also what keeps `commit_access`'s `heat_cfg` parameter
   honest (see Footprint notes).
2. `src/retrieval/piece/src/retrieval_score.rs`
   - `stamp_access(e, now, heat_cfg)` keeps the order stamp and the counter, and
     deposits `deposit_access * deposit_delivery_fraction` — nothing by default.
   - `stamp_read(e, now, heat_cfg)` is the read-back: `stamp_access` plus the
     full `deposit_access`. Its cooldown reads `heat_updated_at` **alone**, not
     the delivery stamp's `accessed_at` — a read follows the query that offered
     it by seconds, so one shared window would suppress every deposit this
     change exists to make, while the separate window still stops a replayed
     read from pumping one row.
   - `deposit_heat(e, now, heat_cfg, amount)` is the shared tail. A zero amount
     returns without touching `heat_updated_at`: stamping it would restart the
     decay clock, which is a silent heat gain, not a no-op.
   - `commit_access_ids` and the new `commit_read_ids` share one `stamp_ids`
     walk, so the monotonic-`now` fix and the "never bump the mutation epoch"
     rule keep exactly one owner.
3. `src/retrieval/piece/src/lib.rs` — `#[no_mangle] retrieval_commit_read_ids`
   beside `retrieval_commit_access_ids`, so the hot-reload dylib exports it.
4. `src/retrieval/src/lib.rs` — re-export it as `score::commit_read_ids` in both
   the `hot` and the `not(hot)` block.
5. `src/tick/src/tick_queue.rs`, `src/tick/loop/src/tick.rs`,
   `src/tick/loop/src/tick_tasks.rs` — `TaskKind::CommitRead` at the same rank
   as `CommitAccess`, its `task_commit_read` constructor, and `do_commit_read`.
   One kind must not carry two deposit rules.
6. `src/rpc/src/server.rs` — `query_by_id` and `query_by_ids` are the only
   places a fetch by reference is served. Both drop the read lock, then call one
   private `commit_read(&[id])` that enqueues `task_commit_read` when a queue is
   present. Advisory, like the delivery stamp: a daemon with no queue deposits
   nothing. The text-query path at `server.rs:721` and `server.rs:764` keeps
   enqueuing `task_commit_access` unchanged — the `tool.memory` `query` surface
   still stamps order and count, and now deposits no heat.
7. Docs: `src/graph/src/heat.rs`'s module header states the read-back as the
   deposit point and drops the claim that every retrieval deposits. `README.md`
   says the same on the `context.memory` line under `## Use` (see Footprint
   notes — the "Compacts itself" paragraph the PRD names no longer exists).
8. `just eval-retention` is rerun and
   `.cartridge/tests/integration/bench/RESULTS.md` gains a dated section holding
   the before and after tables and the decision they support. The probe deposits
   heat itself through `graph::heat::deposit_for` and queries through
   `retrieval::query::query`, which stamps result copies only — so an unchanged
   table is a real result and must be recorded as one, not tuned away.

## Acceptance

- [ ] A query that is never read back leaves every delivered entity's heat, and
      its `heat_updated_at`, exactly as they were, while order and count still
      record what was shown.
- [ ] A read-back of one reference deposits `deposit_access` on that entity and
      on no other, and is not suppressed by the delivery that offered it.
- [ ] A fetch by id through the `memory` service queues the read-back deposit
      naming only the reference that resolved, and a row that was not read
      queues nothing.
- [ ] A replayed read-back cannot pump one reference's heat.
- [ ] `heat.rs`'s module docs and the README's `context.memory` description
      state the read-back as the deposit point, and neither still describes
      delivery as depositing.
- [ ] `just eval-retention` is rerun and `RESULTS.md` records the before and
      after tables in one dated section.

## Denied worlds

Three mutants, each applied to a `git clone --local` copy under `$TMPDIR` and
run with `CARGO_TARGET_DIR` set inside that copy. Observed, not predicted.

- **Delivery deposits again.** `deposit_delivery_fraction` default `0.0` → `1.0`.
  `cargo test -p retrieval-piece --lib` exits **101**, `102 passed; 3 failed`.
  Red: `assertion left == right failed: delivery deposits nothing on the first
  row`, `assertion left == right failed: the row that was shown but never read
  stays cold`, `assertion left == right failed: delivery is the engine's own
  output and deposits no heat`.
- **The read-back stops depositing.** `stamp_read`'s tail becomes
  `deposit_heat(e, now, heat_cfg, 0.0)`. `cargo test -p retrieval-piece --lib`
  exits **101**. Red: `assertion left == right failed: the read reference earns
  the full access deposit`, and the delivery-cooldown guard at
  `retrieval_score_test.rs:385`.
- **The by-id path enqueues the delivery stamp instead.**
  `task_commit_read(ids)` → `task_commit_access(ids)` in `server.rs`.
  `cargo test -p rpc --lib id_filter_tests` exits **101**, `9 passed; 1 failed`.
  Red: `assertion left == right failed: the deposit rides the read-back task,
  not the delivery stamp / left: CommitAccess / right: CommitRead`.

A fourth world is denied by the first `sh` block rather than by a test: the doc
gate fails while `heat.rs` still carries its old deposit claim (observed exit
**1** before the module header was rewritten, **0** after), and it names the
sentence that must go, never the sentence that would satisfy it.

## Footprint notes

The declared footprint is `retrieval_score.rs` and `heat.rs`. Eleven more paths
are needed; each is named here with the evidence.

- `src/config/src/config.rs` — without `deposit_delivery_fraction`,
  `commit_access(results, heat_cfg)` takes a parameter it ignores. Removing the
  parameter instead cascades through `retrieval_query.rs:22,36,531`
  (`query`, `query_profiled`, `query_locked` hold `heat_cfg` for this one call
  and nothing else) into `src/rpc/src/server.rs:743`,
  `src/commands/src/commands_query.rs:346`, and both facade files. One config
  field is the smaller diff and is the PRD's own wording.
- `src/retrieval/piece/src/lib.rs:99-105` and `src/retrieval/src/lib.rs:66-76` —
  the piece is a hot-reloadable dylib. `hot_functions_from_file!(
  "src/retrieval/piece/src/lib.rs")` at `src/retrieval/src/lib.rs:31` generates
  the binding from that file alone, and the two `pub use` blocks are the only
  names a caller can reach. A new `score::*` entry point cannot exist without
  both.
- `src/tick/src/tick_queue.rs:32,45,302`, `src/tick/loop/src/tick.rs:20,234`,
  `src/tick/loop/src/tick_tasks.rs:487` — the deposit runs off the hot path as a
  tick task. `commit_access_ids` scans every access time in the graph
  (`retrieval_score.rs:22-45`) to keep `now` monotonic, so doing this
  synchronously under a write lock on each `get` would be an O(graph) cost on a
  point lookup.
- `src/rpc/src/server.rs:547-587` — `query_by_ids` and `query_by_id` are the
  only servers of a fetch by reference, and today neither enqueues anything.
  This is the read-back call site; it exists nowhere else.
- `.cartridge/tests/unit/src/retrieval/piece/src/tests/retrieval_score_test.rs`
  and `.cartridge/tests/unit/src/rpc/src/tests/server_query_test.rs` — the unit
  tests are mounted into their crates by `#[path]` at
  `retrieval_score.rs:352-354` and `server.rs:2364-2366`. They reach
  crate-private items (`stamp_access`, `Server::tool_query`) and can live
  nowhere else. `retrieval_score_test.rs:302` also asserts the old behaviour
  (`assert!(live.heat > 0.0, "query heat deposited on the live entity")`) and
  must be amended in the same change.
- `README.md` — **the paragraph Acceptance box 4 names does not exist.**
  "Compacts itself" was removed when the README was rewritten in `bf34040`; its
  last text is at `git show 8507e3e:README.md` lines 42-48. The live README's
  equivalent sentence is the `context.memory` bullet under `## Use`
  ("Query previews are discarded; the compact exact-ID readback is the
  evidence"), and that is what this spec updates.
- `.cartridge/tests/integration/bench/RESULTS.md` — Acceptance box 3. Note it is
  **not** at the repository root; that path is the only `RESULTS.md` in the
  repo.

## Measured cost

All measured on the probe clone with `CARGO_TARGET_DIR` inside it.

- `cargo test -p retrieval-piece --lib`, cold target directory: **18.3 s**
  wall, test phase 0.39 s, `105 passed; 0 failed; 6 ignored`.
- `cargo test -p rpc --lib id_filter_tests`, reusing that target directory:
  **7.9 s** wall, `10 passed; 0 failed`.
- Whole-workspace build from a cold target directory: 37.2 s. `kache` is the
  configured `rustc-wrapper` (`~/.cargo/config.toml`), so a cold cache raises
  these; the worst case measured for the pair is still under half the 120 s
  limit.
- The gate is scoped on purpose. `cargo test -p rpc --lib` whole passes
  `110 passed; 0 failed` five runs out of five when run alone, but
  `server_admin_tests::readiness_tests::readiness_answers_while_a_write_holds_
  the_graph` failed once under the load of two test binaries running in
  parallel, and `cargo test --workspace --lib` includes one suite that takes
  165 s by itself. Both blocks are therefore narrow. The full workspace was run
  green once against this change: every suite `ok`, `0 failed`.
- `just eval-retention` is a real embedder run against the mature fixture and
  cannot fit a 120 s block. It is a manual step; its evidence is `RESULTS.md`,
  gated below only as "this file moved off its base text".

## Verify and Proof

```sh
# The heat model's own doc is where the deposit point is stated. The old claim
# has to be gone, not merely joined by a new sentence beside it.
if grep -qin 'every retrieval deposits' src/graph/src/heat.rs; then
	echo 'the heat model still documents delivery as the deposit point' >&2
	exit 1
fi
# The README and the retention record must both have moved off their base text.
base=3432b13376017be921d745719e0626d6f0b5463c
for f in README.md .cartridge/tests/integration/bench/RESULTS.md; do
	git cat-file -e "$base:$f"
	if git show "$base:$f" | diff -q - "$f" >/dev/null; then
		echo "$f carries the same text it had before this change" >&2
		exit 1
	fi
done
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/heat-read-back-verify}"; cargo test -p retrieval-piece --lib
pass: a_query_that_is_never_read_back_leaves_every_delivered_heat_alone
pass: a_read_back_deposits_on_that_reference_alone
pass: a_read_is_not_suppressed_by_the_delivery_that_offered_it
pass: a_replayed_read_cannot_pump_one_references_heat
pass: commit_access_ids_stamps_the_live_entity_without_bumping_the_epoch
pass: replaying_a_query_cannot_pump_one_thoughts_access_count
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/heat-read-back-verify}"; cargo test -p rpc --lib id_filter_tests
pass: a_read_by_id_enqueues_the_read_back_deposit
pass: id_read_keeps_a_row_the_filters_admit
```

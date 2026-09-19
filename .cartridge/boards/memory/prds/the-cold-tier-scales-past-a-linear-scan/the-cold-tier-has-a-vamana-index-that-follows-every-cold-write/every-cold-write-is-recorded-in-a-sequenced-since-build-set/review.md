# @memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/every-cold-write-is-recorded-in-a-sequenced-since-build-set review history

Plan: @memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/every-cold-write-is-recorded-in-a-sequenced-since-build-set (prd.md, specs/spec01.md).
Scope: leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 2, from @memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write (../review.md).

Use the shared [review method](../../../../../../workflows/review-plan.md).

## Round 3 — 2026-09-19

Presented revision: memory.ctg `3432b13` (lane base per the brief). `git diff --stat 5097a83 3432b13 -- src/store/core .cartridge/tests/unit/src/store` is empty, so the spec's stated base `5097a83` and HEAD are identical for every footprint file. The plan files are uncommitted board records. This child inherits rounds 1 and 2 from `the-cold-tier-has-a-vamana-index-that-follows-every-cold-write`.

| Input | Content digest |
| --- | --- |
| Plan | `every-cold-write-is-recorded-in-a-sequenced-since-build-set/prd.md` sha256 `023a8cbb417dd8e78321e47760335c3644eed32229c3f8adab5678c566fc4c39` (matches the brief's Revision) |
| Specs | `specs/spec01.md` sha256 `3082b1d89af6b53f78f19fc8a728d087d8d908bba11fb9eff865ce88cded64ce` |
| Material contracts/dependencies | memory.ctg `3432b13`: `src/store/core/src/{lib.rs,cold.rs,health.rs}`, `.cartridge/tests/unit/src/store/core/src/lib/tests.rs`; external callers of the cold writers (`tick_stigmergy.rs:137-138`, `commands_reembed.rs:186`, `commands_admin_compact.rs:78`, `commands_export.rs:157`, `commands_hub.rs:131,180`); `prd.ctg/.cartridge/templates/spec.md` engine facts; `prd.ctg/src/lifecycle.ts:60-109` (`test` blocks); parent `review.md` rounds 1–2 |

Earlier findings that apply to this child, checked against the plan and the code:

- R1 #2 (the proof cannot fail at base): **regressed.** The new names are good, but the same filter also ORs in `test(/::cold_rekey_/)` and `test(/::cold_relocate_/)`, which match 8 existing tests (see finding 1).
- R1 #7 / R2 D (MAX_DBS citation): **resolved.** `health.rs:22` opens with `max_dbs(32)`, and `compact_dir` (`lib.rs:873`) uses `MAX_DBS`. 5 → 6 is compatible in both directions.
- R1 #10 (reopen after drop): **resolved.** Acceptance 1 and the test say "first handle dropped".
- R1 #12 (cold_move chains): **carried, and now material**, because the set records an op per id (finding 3).
- R2 A, part 1 (persisted floor in the clear transaction): **resolved** in this child. Parts 2 and 3 belong to the sibling `the-cold-tier-has-a-vamana-index-that-the-tick-keeps-current`.
- R2 H (shared target dir): **still open**, and the path is now absolute (finding 4).
- The split cost ("nothing reads or clears the set until the builder lands") is stated as round 2 asked.

Writer coverage: I checked this independently. `rg` finds cold/cold_vec `put`/`delete` only in `cold.rs`, at `import_snapshot:156-170`, `cold_spill:175-182`, `cold_put_all:310-319` and `cold_move:430-445`. `lib.rs` only creates the tables, and `health.rs`/`read_graph` open read-only. Every external writer (tick spill, reembed, admin compact, import, hub rekey/relocate) goes through those four methods. `compact_dir`'s `copy_to_file` carries the new table along. The footprint covers every cold writer.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One observable outcome, one crate, 312 body words, three acceptance boxes, and the cost is stated. −1: `cold_since_len()`/`cold_len()` are added with no consumer and no acceptance in this child. They serve the sibling's trigger, so they belong to it or need one assertion here. −1: the spec says "Base: memory.ctg 5097a83" but the lane is cut from `3432b13`. The code is identical, but the record should name the real base. |
| Ownership and reuse | 17 | It correctly keeps sequence, set and floor in store_core, reuses `meta` and LMDB's writer serialisation, and places each call before the existing `commit`. −1: `cold_snapshot_vectors` re-implements the 7-line `cold_visit_vectors` scan (`cold.rs:224`) instead of sharing a private `visit_vectors_in(&txn, ..)` helper. −1: the `record_cold(puts, deletes)` signature with one seq cannot express order inside a transaction (finding 3). −1: the encoding of the `cold_seq`/`cold_since_floor` meta values is unspecified. Should they be raw LE like `cold_vec`, or versioned `encode` like `EPOCH_KEY`? The choice decides whether `rewrite_meta` and `note_version` must know about them. |
| Dependencies and implementable slices | 18 | No unmet `needs`, medium complexity, three files, and all four write sites are cited with correct lines at HEAD. The sibling B `needs` this child. −1: the stale base sha. −1: the `import_snapshot` scenario needs a memories map, replica, quant mode and stamp. The spec does not point at an existing fixture for it. |
| Observable acceptance and baseline evidence | 10 | The tests are named and well shaped for the floor and the reopen. −6 BLOCKING (finding 1): the Verify block **exits 0 at base**. I measured 8 existing `cold_rekey_*`/`cold_relocate_*` tests passing. This contradicts spec acceptance box 5 and the PRD's "fails at 5097a83". −2 BLOCKING, same finding: `--no-tests=fail` pins no individual name. An implementation that adds none, or only some, of the three tests passes the block. The template requires a `test` block with `pass:` lines. −2: the "survives the clear" test runs sequentially, so it cannot tell a same-transaction seq read from a seq read in a separate transaction before or after the scan. The central race claim is ungated (finding 2). |
| Failure, recovery and compatibility | 16 | MAX_DBS compatibility is verified. The floor never moves down. An older binary ignores the table, and dropping the table degrades to a full build. LMDB serialises `cold_seq` bumps across processes. −3: in a `cold_move` chain (A→B, B→C, or the reverse order), B is both deleted and put in one transaction under one seq. Either fixed order inside `record_cold` records the wrong op for one of the two orders, and a spurious `Delete` becomes a tombstone that hides a live row in the sibling's reader (finding 3). −1: the Verify block hard-codes an absolute `CARGO_TARGET_DIR` into the live checkout (finding 4). |
| Reviewer total | 79 / 100 | |

Findings and concrete revisions:

1. **BLOCKING — the Verify block passes at base and pins no new test.** Evidence: the exact spec filter at `3432b13`, run with an isolated target, gave "Starting 8 tests across 1 binary (68 tests skipped) … 8 passed", exit 0. `--no-tests=fail` fails only when zero tests match, so the `cold_rekey_`/`cold_relocate_` alternatives keep the block green whether or not any `cold_since_build_*` test exists. Fix: replace the `sh` block with the engine's `test` block, so collect requires each name to be reported PASS:
   ````
   ```test
   run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/since-build-set-verify}" cargo nextest run --no-tests=fail -p store_core -E 'test(/::cold_since_build_/) or test(/::cold_rekey_/) or test(/::cold_relocate_/)'
   pass: cold_since_build_names_every_writer
   pass: cold_since_build_write_during_a_build_survives_the_clear
   pass: cold_since_build_floor_persists_across_open
   ```
   The regression tests still run in the same command. Then correct acceptance box 5 and the PRD's "Proof and recovery" to say what actually fails at base: the three `pass:` names are not reported.
2. Non-blocking (but it gates the PRD's central claim) — the same-read-transaction property is untested. As written, the test spills b and c after `cold_snapshot_vectors` returns, so an implementation that reads `cold_seq` in its own transaction also passes. Fix: do the write *inside* the `visit` callback, from a spawned thread that is joined before the callback returns (a write txn on another thread is legal while this thread holds a read txn). Then assert that the returned S is below the write's seq and that the entry survives `clear_cold_since_build(S)`. A seq read after the scan in a separate transaction would then clear it, and the test goes red. Optionally add one mutant step (a copy of the repo in `$TMPDIR` without `target`, the `record_cold` call removed from `cold_move`, a check that the anchor matched, and a requirement that the test turns red). Per the method, one round at most on gate design.
3. Non-blocking — `record_cold(puts, deletes)` is ambiguous for an id that is both deleted and put in one transaction. `cold_move` applies moves in plan order (`cold.rs:432-443`). A→B then B→C leaves B absent, while B→C then A→B leaves B present. Both orders record B in both lists under one seq, so one fixed order inside `record_cold` is wrong for one of them. Fix: after the writes and before commit, have `record_cold(&self, txn, touched: &[&str])` derive each op from the final state (`self.cold.get(txn, id)?.is_some()` → `Put`, else `Delete`). Or record in apply order with a map where the last op wins. Add one chained `cold_rekey`/`cold_relocate` case to `cold_since_build_names_every_writer`, or state that chains cannot occur and why.
4. Non-blocking — use `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/since-build-set-verify}"` (the template form) instead of the absolute `/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify`. The absolute path ties the lane pass to the live checkout's target, only works on this machine, and is shared with sibling B's blocks (R2 H: cargo build-dir lock contention when both collect). It does not hot-restart anything (`-p store_core` builds no cdylib, and the subdirectory is not watched).
5. Non-blocking — specify the meta value encoding. Recommendation: raw `u64` LE with no version byte, as `cold_since` values are, and say that `rewrite_meta` skips them. Also say whether a writer call with an empty batch (for example `cold_put_all(&[])` from compact) still bumps `cold_seq`. Either answer is harmless, but it should be stated.
6. Non-blocking — share the scan. Have `cold_visit_vectors` and `cold_snapshot_vectors` call one private helper that takes the open `RoTxn`, or make `cold_visit_vectors` return the seq it read (its one production caller, `retrieval_query.rs:777`, discards the `Ok` value). Move `cold_since_len`/`cold_len` to the sibling, or assert them in one test here.
7. Non-blocking — set the spec's `Base:` to `3432b13`. The footprint is unchanged since `5097a83`, as verified above.
8. Non-blocking, a note only: `cold_visit_accesses`'s `ponytail:` comment (`cold.rs:238-244`) asks for "a persisted write counter" if a long-lived foreign reader appears. `cold_seq` is that counter. It is out of scope here and worth a follow-up line.

Disposition: revise. Keep the scope and the footprint. Fix the proof (1), and preferably 2–4, in one bounded revision.
Validation:
- `cargo nextest run --no-tests=fail -p store_core -E '<exact spec filter>'` under `sh -eu -c`. cwd `/Users/feb/dev/cartridge/memory.ctg` at `3432b13`, `CARGO_TARGET_DIR=<scratchpad>/since-build-reviewer/target` (fresh, with kache). It compiled in 10.6 s and ran 8 tests (all `cold_rekey_*`/`cold_relocate_*`), 8 passed, 68 skipped, **exit 0**.
- `git diff --stat 5097a83 HEAD` over the footprint: empty.
- `rg` census of cold-table writes and their external callers, as listed above.
- Read `lifecycle.ts:60-109`: `test` blocks are supported and require each `pass:` name in the nextest `PASS` lines.
- I ran no builds against the live target dir and made no edits to the plan files.
Reviewer identity: fresh reviewer agent, coordinator-5c-4.
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (79/100).
Unresolved blocking findings: 1 (Verify passes at base and pins no new test name).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision of spec01.md's Verify (a `test` block with three `pass:` lines and a relative target dir), its acceptance box 5 and the PRD's proof sentence, ideally with findings 2 and 3, then round 4.

VERDICT: FAIL

## Round 4 — 2026-09-19

Presented revision: memory.ctg `3432b13` (lane base). The footprint files are clean at HEAD (`git status --short` empty). The plan files are uncommitted board records, revised per `.state/loop/since-build-set/revision-3.md`. This child inherits rounds 1 and 2 from `the-cold-tier-has-a-vamana-index-that-follows-every-cold-write`. Round 3 is in `review.md`.

| Input | Content digest |
| --- | --- |
| Plan | `every-cold-write-is-recorded-in-a-sequenced-since-build-set/prd.md` sha256 `23bc59d1399c799648b9df094595f75ae2e9e2ac998eabcc212530d8dc0f1611` |
| Specs | `specs/spec01.md` sha256 `76051dd8a0bf331c41346660a2917bdc62cb22091464d7f110844330fd97906c` |
| Material contracts/dependencies | memory.ctg `3432b13`: `src/store/core/src/{lib.rs,cold.rs,health.rs}`, `.cartridge/tests/unit/src/store/core/src/lib/tests.rs`, `src/commands/src/commands_admin_compact.rs:71-85` (migrate calls `cold_put_all` over every row), `src/util/src/util.rs:195` (`LogThrottle`, which is atomic, so `Store` is `Sync`); sibling `the-cold-tier-has-a-vamana-index-that-the-tick-keeps-current/specs/spec01.md:27-64`; `prd.ctg/src/lifecycle.ts:60-109`; `prd.ctg/.cartridge/templates/spec.md` |

Round-3 findings, each checked against the spec and the code rather than taken from the change log:

- **1 BLOCKING (the Verify passes at base and pins no name): resolved.** The block is now `test` with one `run:` line and three `pass:` lines. I ran the exact `run:` line at `3432b13` under `env -u CARTRIDGE_YOLO sh -eu -c` with a fresh isolated target. It exited 0 with "Starting 8 tests across 1 binary (68 tests skipped)" and 8 PASS lines, all `cold_rekey_*`/`cold_relocate_*`. I then fed the log to the engine's own `verificationBlocks`, `testBlock` and `passedTests` (imported from `lifecycle.ts`). The block parsed as one `test` block with three names, and all three were missing, so `runTestBlock` throws at base. When I appended PASS lines for only two of the three names, the third was still reported missing. The block therefore fails if any named test is absent, ignored or failing. Spec acceptance box 5 and the PRD's proof sentence now describe this correctly.
- **2 (same-transaction read untested): resolved.** The write now runs from a scoped thread spawned and joined inside the first `visit` callback, while the scan's read transaction is open. A `cold_seq` read in a separate transaction after the scan would return an S that covers b2 and c, and the test would go red. `Store` is `Sync` (heed handles, `Mutex`, atomics, `LogThrottle` of atomics), so `thread::scope` over `&Store` compiles. A write transaction on another thread while this thread holds a read transaction is legal in LMDB. Reading S before the scan in its own transaction is conservative and harmless, so the test pins the only unsafe direction. Per the method, no mutant gate is required. The diff reading is the backstop.
- **3 (op order in `cold_move` chains): resolved.** Deriving the op from the final state (`cold.get(txn, id)`) is correct in both orders. I traced `cold_move` (`cold.rs:430-445`): B→C then A→B leaves B present, and A→B then B→C leaves B absent. That matches the spec's expected sets. The claim that chains can occur holds: `staying` excludes moving rows (`cold.rs:371-376,382`, `:415`), and `planned` follows the key-sorted scan order.
- **4 (absolute shared target): resolved.** The block uses the template form `${CARGO_TARGET_DIR:-$PWD/target/since-build-set-verify}` with its own slug, on its one cargo command. `-p store_core` builds no cdylib.
- **5 (meta encoding, empty batch): resolved for `meta`.** The meta values are raw u64 LE, read through `self.meta` directly. `rewrite_meta` (`lib.rs:757-766`) reads only named keys, and `health.rs:64-78` reads only `EMBED_KEY`. Nothing iterates `meta`. An empty batch does not bump the sequence, and a test asserts it. See the new finding A for the `cold_since` table.
- **6 (shared scan, the two lens): resolved.** `visit_vectors_in(&RoTxn, ..)` is shared, and the signature of `cold_visit_vectors` is unchanged. `cold_len`/`cold_since_len` are asserted here and consumed by the sibling (`spec01.md:44-46`).
- **7 (base sha): resolved.** `Base: memory.ctg 3432b13`.

API alignment with the sibling: `cold_snapshot_vectors -> Result<u64>` (S), `cold_seq`, `cold_since_floor`, `cold_len`, `cold_since_len` and `clear_cold_since_build(S)` match what the sibling's spec01 calls at `:32`, `:41-46` and `:64`. The floor is raised in the clear's own transaction and never moves down, which covers R2 A part 1.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One observable outcome in one crate, three acceptance boxes, and the cost is stated. The writer census is complete: every cold/cold_vec put or delete is in the four `cold.rs` methods. −1: the PRD body is about 320 words, over the 150–300 aim (under the 400 split line). |
| Ownership and reuse | 18 | Sequence, set and floor sit in store_core. The spec reuses `meta`, LMDB writer serialisation and the existing scan loop through `visit_vectors_in`. −2: the spec does not say how `cold_since_build()` reads the table. The obvious house helper, `scan_with`/`get_with`, calls `note_version` on every value, and the `cold_since` value starts with the op byte (finding A). |
| Dependencies and implementable slices | 19 | No unmet needs. Three files, medium complexity, every call site cited with correct lines at HEAD, and the `import_snapshot` fixture named (`EmbedStamp { model, dim }` matches `lib.rs:312`). −1: "The coordinator warms the target with `--no-run`" does not say that the lane pass and the repo pass resolve `$PWD` to different target dirs (finding C). |
| Observable acceptance and baseline evidence | 18 | The blocker is fixed, and I reproduced both the base failure and the missing-name failure with the engine's own matcher. The race test now gates the same-transaction property. −1: "a rising seq" in `cold_since_build_names_every_writer` is unspecified when every scenario uses a fresh store, where each single-writer scenario records seq 1 (finding D). −1: no gate can show a test died of the behaviour. That ceiling is accepted per the method, and the diff reading is the backstop. |
| Failure, recovery and compatibility | 17 | MAX_DBS 5→6 is compatible both ways (`health.rs:22` uses 32, and `compact_dir` uses `MAX_DBS` with `copy_to_file`). An older binary ignores the table, dropping it only forces a full build, and the floor is monotone. −2: finding A. If `note_version` sees the op byte as an old format, `memory check` reports the store as stale forever, and `migrate` (`commands_admin_compact.rs:71-85`, which calls `cold_put_all` over every row) repopulates the set, so a clean migrate cannot fix it. −1: the spec's own chain scenario A→B then B→C runs through a `cold_move` that already loses data (finding B), and the plan names no follow-up. |
| Reviewer total | 91 / 100 | |

Findings and concrete revisions:

A. Non-blocking: say how `cold_since` is read. `note_version` (`lib.rs:477-492`) flags any value whose first byte is not `FORMAT_VERSION`, and its comment names `cold_vec` as "the one table without a version byte". A `cold_since` value begins with `0`/`1`. If `cold_since_build()` is written with `scan_with` or `get_with`, `migrated_from` sticks, and `memory check` and `migrate` report the store as old indefinitely. Fix: add one sentence to spec step 3. `cold_since_build()` iterates `self.cold_since` directly in its own read transaction, never through `scan_with`/`get_with`. Extend the `note_version` comment to name `cold_since` beside `cold_vec`. Optionally assert `migrated_from() == None` after `cold_since_build()` in `cold_since_build_names_every_writer`.

B. Non-blocking, follow-up: `cold_move` loses data on the A→B, B→C order, and this bug predates the plan. Iteration 1 overwrites B's row and vector with A's. Iteration 2 then moves B's original planned row to C with A's vector, read from `cold_vec[B]` at move time. A's row and B's vector are gone. In `cold_rekey` this order occurs whenever A sorts before B (`scan_with` is key-ordered). The since-set records the final state correctly either way, so this child is not wrong. However, its test drives exactly this order and would enshrine the result. Fix: add one line to the PRD's cost paragraph naming a follow-up PRD. A cheap two-phase `cold_move` fits the same file: read every planned vector first, delete every `old`, then put every `new`.

C. Non-blocking: be exact about the warm-up. The lane pass uses `<lane>/target/since-build-set-verify`, and the repo pass uses `memory.ctg/target/since-build-set-verify`. Fix: either say the coordinator warms both, or drop the sentence and cite the measurement. A cold build in a fresh isolated target took 5.8 s to compile and 7 s in total (with the user's `kache` rustc-wrapper from `~/.cargo/config.toml`), well inside 120 s. Without kache it is unmeasured.

D. Non-blocking: state what "rising seq" means. For example: within the chain and `cold_put_all(&[])` scenarios, which share a store, each writer's entries carry a seq exactly one above the previous writer's, and `cold_seq()` equals the highest recorded seq.

Disposition: keep. The findings are clarifications and one follow-up, and none changes scope or footprint.
Validation:
- `env -u CARTRIDGE_YOLO sh -eu -c 'CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/since-build-set-verify}" cargo nextest run --no-tests=fail -p store_core -E '\''test(/::cold_since_build_/) or test(/::cold_rekey_/) or test(/::cold_relocate_/)'\'''`, cwd `/Users/feb/dev/cartridge/memory.ctg` at `3432b13`, `CARGO_TARGET_DIR=<scratchpad>/since-build-r4/target` (freshly created). Exit 0, 7 s wall time, 8 passed and 68 skipped, and `cold_since_build` absent.
- `bun <scratchpad>/r4check.ts` imports `verificationBlocks`, `testBlock` and `passedTests` from `prd.ctg/src/lifecycle.ts`. The spec yields one `test` block with three names. On the base log all three are missing. With two synthetic PASS lines, the third is still missing.
- Code reads at `3432b13`: `cold.rs:20-47,140-186,220-320,340-450,505-540`; `lib.rs:25-45,360-381,455-530,757-766,860-890`; `health.rs:55-80`; `commands_admin_compact.rs:60-90`; `rg` for `max_dbs`/`open_database` and the `cold_put_all` callers.
- I ran no build in `memory.ctg/target` and made no edits to prd.md, spec01.md or review.md.
Reviewer identity: fresh reviewer agent, coordinator-5c-4.
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: PASS (91/100).
Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: optionally fold A–D into the spec body as a clarification-only edit; findings A and B are the ones worth doing before implementation. Then proceed to implementation.

VERDICT: PASS

# @memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write review history

Plan: `@memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write`, `prds/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/prd.md`.
Scope: one leaf. A cold-tier Vamana snapshot plus a persisted since-build set that every cold writer maintains, and a rebuild that runs off the query path. The query read belongs to the sibling `a-query-reads-the-cold-tier-through-its-index`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 with 0 used rounds.

Use the shared [review method](../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: memory.ctg `5097a83` (clean for the reviewed paths). The plan files are uncommitted board records.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `06d7aa83679646bde862412bc8f48c982469d610e3ae1e64b0d6e7f829d91a18` |
| Specs | `specs/spec01.md` sha256 `123e2416438c47f87213191cc7109fd5561180549b4444ed5499f915ac26bc8a` |
| Material contracts/dependencies | memory.ctg `5097a83`: `src/store/core/src/cold.rs`, `src/store/core/src/lib.rs`, `src/store/core/src/lock.rs`, `src/graph/src/graph.rs`, `src/graph/src/diskann.rs`; the prerequisite `diskann-builds-keep-every-node-reachable-from-the-entry-point` (collection.md, commit 5097a83); the sibling `a-query-reads-the-cold-tier-through-its-index/prd.md`; `prd.ctg/src/lifecycle.ts` `verificationBlocks`/`verify`; analyst-1.md and analyst-2.md |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The outcome is clear. The split is sound: this leaf has no reader, and the sibling `needs` it. At about 330 words it stays under the 400-word limit. The model-stamp decision is argued with evidence. −2: nothing in this leaf states who owns and holds the built index. The sibling "reads through its index", but there is no handle or API for it to read through. −2: the build trigger has no named caller, so the promise that the index "follows every cold write" is incomplete. |
| Ownership and reuse | 12 | It correctly reuses `build_and_save_with_epoch`, `DiskIndex` and `cold_visit_vectors`. −3: the "stamp" it plans to reuse does not fit. The only epoch at hand is `Store::read_epoch` (`EPOCH_KEY`), and it moves only in `write_snapshot` (`lib.rs:704`), never in `cold_spill`, `cold_put_all` or `cold_move`. If the build passes that epoch, `build_and_save_with_epoch` (`diskann.rs:190`) short-circuits and skips needed rebuilds. −2: `reconcile_disk`'s `outgrown` rule runs its rebuild on `&mut self`, which means under the write lock. `consolidate_disk_index` says "COST: the Vamana build runs under the graph WRITE lock", and `tick_tasks.rs:484` calls it inside `g.write()`. So the pattern being copied is the one the plan forbids. −3: the footprint is wrong. The PRD lists `diskann.rs` and `diskann_test.rs`, which no step edits. Neither list includes `.cartridge/tests/unit/src/graph/src/tests/graph_test.rs` (where graph.rs tests live, `graph.rs:1066`), `.cartridge/tests/unit/src/store/core/src/lib/tests.rs` (where every existing cold writer test lives), or any runner or tick file. `MAX_DBS = 5` (`lib.rs:36`) is already full with five tables, so a sixth table needs that bump, or the set has to live under a `meta` key prefix. The plan says neither. |
| Dependencies and implementable slices | 13 | `needs` names the prerequisite, which is done (5097a83, collection exit 0). The dependency order with the sibling is right. −3: the spec is a single "large" step, and step 2 leaves open where the build runs: which thread, which process, and what it takes as input. The type `GraphGnn` cannot be borrowed across a lock release, and store_core sits below graph. −2: the plan defines no handoff contract for the sibling: a cold index handle, a freshness rule, and whether since-build deletes act as tombstones over snapshot ids. −2: the spec and the PRD disagree about Verify. The engine runs only the spec's blocks (`lifecycle.ts` `verify` uses `specs(prd)`), so the PRD's Verify is dead text that contradicts the spec. |
| Observable acceptance and baseline evidence | 9 | Box 1 is observable per writer. −5 (BLOCKING): the spec's Verify runs `cargo nextest run` without `--release` or `--cargo-profile release`, with `CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target`. That builds `memory.ctg/target/debug`, which the live daemon watches, so the second pass hot-restarts the live memory cartridge. The block's comment says it warms "this release target", but the command does not build one. −4 (BLOCKING): the blocks cannot fail at 5097a83 for the right reason. `nextest list -p store_core cold` already matches 25 existing tests, so the store_core block passes today. `-p graph cold` matches 0 tests, so that block fails today only because no tests were found. Neither names the new tests. −2 (BLOCKING): "no build runs inside a query or under the graph write lock" has no test or structural check behind it. −0: the 100k measurement has no stated destination (Result section). |
| Failure, recovery and compatibility | 11 | The plan intends to keep the old snapshot on a failed build, and the staging swap in `build_and_save_into` supports that for failures before the swap. −4 (BLOCKING): the since-build row is `(id, put\|delete)` and has no sequence. A build takes a snapshot of `cold_visit_vectors` at T0 and then runs for 56–72 s at 10k and far longer at 100k. Any write to an id already in the set during that time overwrites the same key, so `clear_since_build(stamp)` cannot tell it apart and deletes it. The plan does not say that the stamp is read in the same read transaction as the vector scan. −3 (BLOCKING): builders are unserialised. The daemon plus a CLI `compact`, `reembed` or `import` (all cold writers, `commands_admin_compact.rs:78`, `commands_reembed.rs:186`, `commands_export.rs:157`) can both build `diskann/cold` and share `cold.staging` (`diskann.rs:280`). The second builder's `remove_dir_all(&staging)` destroys the first builder's staging files. No lock is named, and `lock.rs` WriterLock is the obvious candidate. −1: the stamp write is best-effort (`let _ = std::fs::write(epoch)`, `diskann.rs:300`), so "clear only with the new stamp" needs a read-back before clearing. −1: after `memory reembed`, `cold_put_all` rewrites n rows into a snapshot of n rows, but `outgrown` is `inserted > snap_count` (`graph.rs:122`) and does not fire at equality. The index stays on old-model vectors, and possibly an old width, until more writes arrive. Neither an `EmbedStamp` change nor a width change forces a rebuild. −0: an older binary still writing cold rows would leave the set silently incomplete; the plan names no guard such as a cold row count in the stamp. |
| Reviewer total | 61 / 100 | |

Findings and concrete revisions:

1. **BLOCKING — Verify would hot-restart the live daemon.** spec01 runs `CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target cargo nextest run ...` in the debug profile, which writes to the watched `target/debug`. Fix: add `--cargo-profile release` (or `cargo test --release`, as the prerequisite's collected spec did), or export a scratch `CARGO_TARGET_DIR` that is warmed first. Make the PRD `## Verify` match the spec, or remove it.
2. **BLOCKING — the proof cannot fail at 5097a83.** Filter `cold` already selects 25 passing store_core tests and 0 graph tests. Fix: name the new tests, for example `-E 'test(=tests::since_build_names_every_cold_write) or ...'` or a unique prefix such as `cold_since_build_`, and state that each one fails or does not compile at 5097a83.
3. **BLOCKING — undefined stamp and a clear that races writes.** Define the stamp as a persisted cold sequence in `meta`, bumped in each cold writer's own transaction. Store each since-build entry as `id -> (op, seq)`. Read the snapshot's sequence in the same read transaction as the vector scan. `clear_since_build(s)` deletes only entries with `seq <= s`. Do not pass `Store::read_epoch`, which cold writes do not move, to `build_and_save_with_epoch`. Add a test in which a write lands between the snapshot read and the clear and survives.
4. **BLOCKING — no single builder and no runner.** Name the caller (for example a tick task that clones `Arc<Store>` and `data_dir`, releases the graph lock, builds, then swaps a handle in), the file it lives in (add it to the footprint), and the cross-process exclusion: hold `WriterLock` or a `diskann/cold.lock` flock around staging, swap and clear. State where the `DiskIndex` handle lives for the sibling.
5. **BLOCKING — "no build under the graph write lock" is untestable as written.** Make it structural, for example a build function whose signature takes `&Store` and `&Path` but no `GraphGnn`, plus one test that takes the write lock from another thread while a build is in progress and requires it to succeed within a bound. Or reword the box to name the check.
6. **BLOCKING (cheap) — footprint.** Remove `src/graph/src/diskann.rs` and `diskann_test.rs` from the PRD unless a step edits them. The stamp read-back could justify one diskann.rs edit, but only if a step says so. Add `graph_test.rs` or a new graph test file, `lib/tests.rs` if the writer tests extend it, and the runner file. Keep the PRD and spec footprints identical.
7. Non-blocking: `MAX_DBS = 5` is full. Either bump it (and check `compact` and `read_graph` at `cold.rs:629`, which open with `MAX_DBS`) or keep the set under a `meta` prefix.
8. Non-blocking: rebuild when `EmbedStamp` or width changes, and use `>=` rather than `>` for the since-build size against the snapshot, so that `reembed` and `import_snapshot` do not leave a same-size, old-model index.
9. Non-blocking: read back `snapshot_epoch(dir) == Some(seq)` before clearing, because the stamp write in `diskann.rs:300` is best-effort. A crash between swap and clear must leave a superset set, which is harmless; say so.
10. Non-blocking: Acceptance 1's "second `Store::open`" works in-process only after the first handle is dropped (one env per process). Say "reopen after drop". LMDB already guarantees cross-process visibility.
11. Non-blocking: say where the 100k build-time measurement is recorded (the Result section), and whether it runs in release. It cannot run inside a 120 s block.
12. Non-blocking, outside this scope, worth a note: `cold_move` applies moves in key order, so a chain A→B, B→C can read B's vector after A's row was put there. If such chains are possible, the since-build set records the final state faithfully but inherits that mix-up.

Disposition: revise (keep the split and the scope; fix the proof commands, the stamp and sequence contract, the builder owner and lock, and the footprint).
Validation: `cargo nextest list -p store_core -p graph cold` with cwd `/Users/feb/dev/cartridge/memory.ctg` and `CARGO_TARGET_DIR=<scratchpad>/target-rv` (isolated, debug): exit 0 in 23 s. It listed 25 store_core tests and 0 graph tests. I checked `nextest` 0.9.143 and the engine's verify code (`prd.ctg/src/lifecycle.ts:35-50`: spec blocks only, heading regex `Verify\b` matches `## Verify and Proof`, 120 s timeout). I ran no release build. Block timing is unmeasured: the prerequisite's graph release run finished in 4.8 s warm; store_core's release test binary is not yet known to be warm.
Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (61/100).
Unresolved blocking findings: 1, 2, 3, 4, 5, 6.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of prd.md and spec01.md that addresses findings 1–6 (and ideally 7–11), then round 2.

## Round 2 — 2026-09-16

Presented revision: memory.ctg `5097a83` (clean). The plan files are uncommitted board records.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `5448896468d48b980ec1795e0c097f9da2d1c4494ac8a2ac62c57784b32eb695` (matches the hand-off `54488964…`) |
| Specs | `specs/spec01.md` sha256 `003514f7659a5043d84f95527727e4beeb30a34a046c27ab68f18c3eed41f015` (matches the hand-off `003514f7…`) |
| Material contracts/dependencies | memory.ctg `5097a83`: `src/store/core/src/{lib.rs,cold.rs,lock.rs,health.rs}`, `src/graph/src/{diskann.rs,graph.rs,persist.rs}`, `src/tick/src/{tick_queue.rs,tick_pulse.rs}`, `src/tick/loop/src/{tick.rs,tick_tasks.rs}`, `src/commands/src/commands_serve.rs:700-725`; cartridge.ctg `src/loader/mod.rs:67-88` (`native_candidates`); the parent PRD and the siblings `a-query-reads-the-cold-tier-through-its-index`, `a-point-in-time-query-names-what-it-costs` and `the-memory-cartridge-integration-tests-trust-the-project-they-boot` |

Round 1 blockers, checked against the code:

- **1 (Verify hot-restarts the daemon): resolved.** The host watches `<root>`, `<root>/target/release` and `<root>/target/debug` for `lib<name>.dylib|.so` (cartridge.ctg `src/loader/mod.rs:67-88`). `target/cold-index-verify/debug` is not on that list, and `-p store_core|graph|tick_loop` never builds the memory cdylib anyway.
- **2 (proof cannot fail at base): resolved.** At 5097a83 all three blocks exit 4 with "no tests to run" (76, 179 and 73 tests skipped). The `/::name$/` filters will match the module paths the plan implies (`cold_index::tests::…`, `tick_tasks_tests::…`, `tests::…`).
- **3 (stamp and racing clear): mostly resolved.** `cold_seq` is bumped inside each writer's own LMDB write transaction. LMDB serialises write transactions across processes, so read-increment-write is atomic under concurrent writers. S is read in the scan's read transaction (MVCC), and a later write to the same id replaces the entry with seq > S. That part is correct. The new ordering defect is finding A.
- **4 (no builder, runner or lock): resolved in shape.** `try_lock_patiently` (`lock.rs:78`) uses flock semantics, which are per open file description. A second `File::open` in the same process conflicts, so the in-process `second_builder_skips` test is valid. The OS releases the lock when a process is killed. Hot snapshots live in `diskann/{entity,gnn,reason}` (`graph.rs:556,586,640`), so `diskann/cold`, `cold.staging` and `cold.lock` collide with none of them. New gaps are findings B and C.
- **5 (write-lock claim untestable): resolved.** The builder's signature takes no `GraphGnn`, and there is a tick test. Test-shape notes are in finding F.
- **6 (footprint): mostly resolved.** `diskann.rs` is gone, and the runner, queue, pulse and test files are listed. Test modules are declared by `#[path]` in each source file (`tick_tasks.rs:626`, `graph.rs:1066`), so `cold_index.rs` carries its own test module and no mod file is missing. The one gap is in finding E.
- **7 (MAX_DBS): resolved, with a wrong citation.** `max_dbs` sizes one env handle's DBI table, not the file, so 5 → 6 is compatible both ways: a 5-slot binary on a 6-table store never opens `cold_since`. `compact_dir` uses `MAX_DBS` and `copy_to_file`, which copies every table. `read_graph` does NOT open through `MAX_DBS`: it uses `health::open_readonly`, `max_dbs(32)` (`health.rs:22`), and `cold.rs:629` is an `open_database` call. The conclusion stands; the citation should be corrected.
- **8–12: addressed.** Finding A contradicts point 9's "crash between swap and clear".

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The outcome is clear, and the sibling now has a concrete handle and freshness contract. −2: the PRD body is 402 words, over the 400-word leaf limit, and the spec is "large" and bundles two outcomes (see the split recommendation). −2: a 100k build runs on the single tick drain (`tick.rs` `start`: one task at a time inside a tokio task), so Persist, CommitAccess and every other task stall for the whole build. The plan records the time but gives no decision rule for what cost is acceptable. |
| Ownership and reuse | 17 | It reuses `build_and_save_with_epoch`, `try_lock_patiently`, the graph-global `""` key and the rank table. −1: it does not reuse `claim_slot` cadence gating (`tick_pulse.rs:52`), which every other global task uses (finding C). −1: the `read_graph`/`MAX_DBS` citation is wrong (see 7). −1: "Load opens it if present" is not placed in a file. Graph load is `persist.rs::load_dir` (`:51-64`), which is not in the footprint (finding E). |
| Dependencies and implementable slices | 16 | `needs` is met (5097a83). Sibling order is right. −2: one large slice covers three crates. −1: `do_cold_index_build(g)` has no hook parameter, yet the tick test injects a blocking hook. −1: the steps contradict each other on ordering. `build` clears inside itself (step 2.5), and the runner swaps afterwards (step 3.3), but the Contract speaks of a "crash between swap and clear". |
| Observable acceptance and baseline evidence | 17 | Tests are named, `--no-tests=fail` is proven to exit 4 at base, and the timings fit (below). −1: the rebuild trigger rules (`>=`, embed, width, no snapshot) have no test. −1: no test covers a query-visible handle against a cleared set (finding A). −1: the write-lock test should bound `g.write()` with `try_write_for(5 s)`. As written, a regression hangs the main thread until the hook's timeout panics the builder thread, and it only fails if the test joins and checks that thread. |
| Failure, recovery and compatibility | 12 | The sequence, lock and MAX_DBS compatibility are sound, and failure injection works: `create_dir_all` on a regular file at `cold.staging` errs before the Vamana build, at `diskann.rs:281-282`. −5 BLOCKING (A): clearing before the handle swap loses rows. −3 BLOCKING (B+C): a persistent failure becomes a full-tier rebuild every tick with no backoff, and nothing filters bad widths. |
| Reviewer total | 78 / 100 | |

Findings and concrete revisions:

- **A. BLOCKING — clearing before the swap loses since-build rows for a reader holding the older handle.** `build` runs `clear_cold_since_build(S_new)` with no graph lock, and only then does the runner take `g.write()` to swap (spec step 2.5, step 3.3). A query already under `g.read()` holds `(handle, S_old)` and then reads a set with every entry ≤ S_new gone. Rows put or re-keyed in (S_old, S_new] are in neither the old snapshot nor the set, so they are invisible: the rekey case vanishes, because `cold_get(old)` is `None` and `new` is unlisted. In-process this is a transient recall miss. The plan also names "a daemon and a CLI" as concurrent builders. If another process builds and clears, the daemon keeps S_old indefinitely: `reconcile_if_stale` reloads only on `read_epoch`, which cold writes never move (`lib.rs:704`). The Contract's freshness rule (`cold_seq() >= S`) accepts that handle, so the miss is silent and lasts until restart.
  - Fix, part 1: persist `cold_since_floor = S` in `meta` in the same transaction as the clear.
  - Fix, part 2: a handle is usable only when `handle S >= floor`; otherwise reopen from disk or take the exact scan. Put this in the sibling contract.
  - Fix, part 3: in-process, swap before clearing (clear after the runner's write-locked assignment), which makes the "crash between swap and clear" sentence true.
  - Test: build twice while holding the first handle, and assert the old handle reads as unusable.
- **B. BLOCKING — nothing filters widths, so a bad tier rebuilds forever.** `build_and_save_into` takes `dim` from the first item and writes every vector as it is (`diskann.rs:285`, `write_files:355`). A tier holding mixed or empty widths, which the store expects (`cold_search` skips `buf.len() != query_vec.len()`, `cold.rs:465`), yields a snapshot that `DiskIndex::open` rejects with "file size does not match meta" (`diskann.rs:420`). The "no snapshot" trigger then holds on every pulse. Fix: the builder keeps only vectors of the store width (the `EmbedStamp` dim) and skips empty ones, then opens the new snapshot before the handle swap and the clear. Test with one wrong-width row.
- **C. BLOCKING (merged with B) — no cadence, backoff or recheck.**
  - The pulse runs every `tick.interval_secs` under `g.read()` (`commands_serve.rs:716-719`).
  - `Queue::dequeued` clears the pending key when a task starts (`tick.rs` `start`, `tick_queue.rs:225`), so a pulse during a long build enqueues a second `ColdIndexBuild`.
  - Any write during the first build changes S, so the second one is another full build.
  - Any persistent `Err` (disk full, B) repeats a full vector scan plus build attempt every interval on the single drain lane.
  - Fix: gate the enqueue through `claim_slot` with a `cold_index_at_secs` cadence, as `maybe_enqueue_disk_consolidate` does. Have the runner recheck the trigger before building. On `Err`, record it with `q.record_task_failure` (or equivalent) and back off until the next cadence slot.
- D. Non-blocking: correct the `MAX_DBS` citation. `read_graph` uses `open_readonly` with `max_dbs(32)`. Compatibility holds either way.
- E. Non-blocking: say where the handle is opened at load. Either `set_store`/`graph.rs`, or add `src/graph/src/persist.rs` (`load_dir`) to both footprints. Also say whether `reconcile_if_stale` → `load_dir` reopens it; it will if the open lives there.
- F. Non-blocking: give `do_cold_index_build` a hook parameter (or a `_with_hook` variant) in the spec, and use `try_write_for(Duration::from_secs(5))` in the lock test so a regression fails instead of hanging.
- G. Non-blocking: say that the build stalls the tick drain for its whole duration, and set the threshold the 100k measurement is judged against. Crash loss stays bounded, because `snapshot_if_dirty` runs outside the drain (`commands_serve.rs:722`). Alternatively, move the build to `spawn_blocking` or a dedicated thread. Either choice is acceptable if it is stated.
- H. Non-blocking: both passes share `target/cold-index-verify`. The lane pass and the main pass compile different source roots, so workspace crates rebuild on the second pass (dependencies are reused). Two lanes collecting at once would wait on cargo's build-dir lock. The timings below leave ample room.

Split recommendation: **split**, keeping the round count (2 used).
- **Child A (store_core only):** `cold_seq`, `cold_since`, the entries written by all five writers, `cold_snapshot_vectors`, `clear_cold_since_build`, and the `cold_since_floor` from finding A (it is a store_core concern). Footprint: `lib.rs`, `cold.rs`, `lib/tests.rs`. Verify: block 1 plus a floor test. It has one observable outcome, no dependency on B, a 14 s cold proof, and it is well under 400 words.
- **Child B (`needs` A):** builder, runner, handle, trigger, width filter and backoff. Footprint: graph and tick files. Verify: blocks 2 and 3.
- Reasons: the leaf is over the word limit; the two halves touch disjoint crates; A's contract is now settled while every remaining blocker except A's floor sits in B; A can land and be collected while B is revised.
- Cost: A alone writes set entries that nothing reads until B lands. That is acceptable at equal priority, and the set is bounded by the rebuild rule only once B exists. Say so in A.

Disposition: revise (split as above, then fix A in child A and B/C in child B).
Validation:
- `cargo nextest run --no-tests=fail -p <pkg> -E '<spec filter>'` for each of the three blocks, cwd `/Users/feb/dev/cartridge/memory.ctg`, `CARGO_TARGET_DIR=<scratchpad>/target-r2` (fresh). Every run exited 4 with "no tests to run".
  - store_core: cold 14 s, warm 1 s, 76 skipped.
  - graph: cold 21 s, warm 0 s, 179 skipped.
  - tick_loop: cold 11 s, warm 0 s, 73 skipped.
  - "Cold" means a fresh target dir, but `~/.cargo/config.toml` sets `rustc-wrapper = "kache"`, so dependency artefacts came from its cache. A machine without kache would be slower. The coordinator's `--no-run` warm-up covers that.
- I ran no release build and no 100k measurement.
- Reviewer identity: independent reviewer agent r2 (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (78/100).
Unresolved blocking findings: A (clearing before the swap / no floor loses rows for an older handle), B+C (no width filter, cadence, backoff or recheck, so a bad tier rebuilds on every pulse).
Rounds used / remaining: 2 / 3.
Next action: split into child A (store_core sequence, set and floor) and child B (builder, runner and handle, `needs` A). Resolve A, B/C and D–H, then round 3 for both children, which inherit 2 used rounds.

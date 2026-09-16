# @memory/diskann-builds-keep-every-node-reachable-from-the-entry-point review history

Plan: @memory/diskann-builds-keep-every-node-reachable-from-the-entry-point, `boards/memory/prds/diskann-builds-keep-every-node-reachable-from-the-entry-point/prd.md`.
Scope: one observable outcome: a Vamana build on a clustered corpus reaches every node from `entry` and keeps top-10 recall. Leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (new defect leaf lifted from analyst-1 of `@memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write`).

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: prd.ctg a0454963 (both files clean at review time); code memory.ctg a9ab81a.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `54bb71d4ba29ed53d29facc0d60733f40c4f90a8a4ecb6871f92b8706c4a158a` |
| Specs | `specs/spec01.md` sha256 `6ab9cbaf9381f5b5e2bb1ed098cbf59b39a8690718afe13c8e891e6f6f123996` |
| Material contracts/dependencies | memory.ctg a9ab81a `src/graph/src/diskann.rs`, `src/graph/src/graph.rs`, `src/config/src/config.rs`; analyst evidence `.state/loop/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/{analyst-1.md,probe-vamana.diff}`; dependent `prds/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/{prd.md,specs/spec01.md}`; engine `prd.ctg/src/lifecycle.ts:36-47,125-168` |

### Root cause, checked on its own

- Reproduced at a9ab81a in a scratch detached worktree with its own target, release. Corpus: 64 centres × 40 rows, 1024-d, noise 0.6, seed 3, default `Params`, `search(q,10,96)`, 20 queries. **reach 40/2560 (one cluster), recall@10 0.000**, build 8.5 s. Seed 5 gave the same result. With 64 × 34 rows (clusters of r+2): reach 102/2176, recall 0.100. So the spec's 64 × 40 starting size fails at HEAD for both new tests.
- Other explanations ruled out:
  - Entry choice: the graph itself splits into closed clusters, so no entry can reach everything.
  - Random initial graph: it exists (`diskann.rs:206-217`).
  - Pass order: the order is reshuffled for each pass (`:220-224`), and the two passes are α=1.0 then α.
  - Paper line 1 of RobustPrune (`V ∪ N_out(p)`): adding `adj[p]` to the candidates **still gave 40/2560, 0.000**. The missing union is a small divergence from the paper, but it does not cause this bug.
- Is the fix principled? Yes. In the paper, pass 2 with an independent α>1 selection turns into a plain kNN list when distances within a cluster are concentrated. The back-edge re-prune (`:239-241`) then evicts the last cross edges. The reference implementation (microsoft/DiskANN `occlude_list`) prevents this: it raises `cur_alpha` from 1.0 up to α and fills free slots under one running occlusion factor per candidate. The spec's version is close to this but not the same: it appends from an *independent* α selection. Both were probed on 64 × 40:
  - spec variant: 2560/2560, recall 1.000, build 10.9 s
  - `occlude_list` variant: 2560/2560, recall 1.000, build **8.1 s** (HEAD: 8.5 s)
  - With each variant on, all 12 existing diskann tests pass, including `the_same_corpus_builds_a_byte_identical_index`.
- Hot-tier exposure is wider than the PRD says. `Graph::rebuild_index` spills when `entity_count > disk_threshold` (`graph.rs:427`). It builds through `build_disk_snapshot` → `build_and_save_with_epoch(.., Params::default(), epoch)` (`graph.rs:559-563`) and searches through `VectorBackend::Disk` (`vector_backend.rs:18`). The default `disk_threshold` is **0** (`config.rs:717`), so every store-backed graph uses this build, not only large ones.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Real, reproduced silent recall loss on the default path. One outcome, two-file footprint. −1: exposure understated ("above `disk_threshold`", but the default is 0). −1: PRD is 384 words (target 150–300). −1: the recovery claim overstates what users get (see N2). |
| Ownership and reuse | 18 | Correct owner and file. Reuses `build_adjacency`, `brute_topk`, `medoid`, and the probe corpus shape. −2: the spec invents an "append from an independent α selection" rule instead of the reference `occlude_list` escalation, which is cheaper (8.1 s against 10.9 s) and has upstream precedent (N1). |
| Dependencies and implementable slices | 18 | No `needs`. The dependent cold-tier plan `needs` this one, and integration order is stated because both share `diskann.rs` and its test file. One small spec. −2: the Verify timing depends on the coordinator warming the shared release target, which is written as a comment, not a step. |
| Observable acceptance and baseline evidence | 12 | Good baseline: the probe table was reproduced here (40/2560, 0.000), and both new tests will fail at a9ab81a at 64 × 40. Warm timing fits: two builds of about 8–11 s plus existing tests of about 0.3 s, well under 120 s. **−6 BLOCKING (B1): the Verify block cannot pass.** −1: the recall test's search `L` is unspecified. −1: "recorded output" has no named destination. |
| Failure, recovery and compatibility | 15 | On-disk format unchanged, determinism kept (byte-identical test passes with the fix and still exercises the new code, because default α=1.2 goes through it). −3 (N2): old disconnected snapshots are **not** rebuilt at load while the store epoch matches (`diskann.rs:178-181`, `graph.rs:587-610`). They stay broken until the next write bumps the epoch. −2: the build-time cost (+30% at 10k probed) has no bound or acceptance. |
| Reviewer total | 80 / 100 | |

Findings and concrete revisions:

- **B1 (BLOCKING): the Verify block fails under `sh -eu`.**
  - *Evidence:* `spec01.md` Verify starts with `cd memory.ctg`. `collect` runs the blocks with `cwd` = the lane worktree (which *is* the memory.ctg checkout), then with `cwd` = `/Users/feb/dev/cartridge/memory.ctg` (`lifecycle.ts:125,137,167`). Neither directory has a `memory.ctg` child: `sh -eu -c 'cd memory.ctg'` → `cd: memory.ctg: No such file or directory`, exit 1.
  - *Revision:* delete the `cd memory.ctg` line. Keep `CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target cargo test --release -p graph --lib diskann`, which already matches the new test names through the `diskann::tests` path.
  - The dependent cold-tier spec01 has the same `cd memory.ctg` defect in both of its blocks. Record that in its own review.
- **N1 (non-blocking):** in spec step 1, specify the reference `occlude_list` semantics. Sort the candidates once and keep one occlusion factor `max d(p,v)/d(p*,v)` per candidate over every chosen `p*`. Select at `cur_alpha = 1.0`, then at `cur_alpha = alpha`, stopping at `r`. This probed faster than the spec's two-selection form and matches upstream DiskANN. Update the PRD's "keep the α=1.0 selection first and fill…" sentence to match.
- **N2 (non-blocking):** replace "they reconnect at the next rebuild" with the actual behaviour: a snapshot whose epoch still matches is reused until the next store write. Either accept that explicitly, or add a build-version marker so pre-fix snapshots rebuild once. Any marker must stay inside the footprint and keep `snapshot_epoch` backward-safe.
- **N3 (non-blocking):** in the Outcome, state that `disk_threshold` defaults to 0 (`config.rs:717`), so every store-backed graph uses this build today.
- **N4 (non-blocking):**
  - Fix the recall test's search beam (e.g. `search(q, 10, 96)`, which gives recall 1.000 after the fix).
  - Name where the failing-at-a9ab81a output goes (the lane report or `collection.md`).
  - Add a loose build-time note for the 10k ignored test, e.g. no more than 1.5× HEAD.
  - Trim the PRD toward 300 words by moving the probe numbers to analyst-1.

Disposition: revise (B1 is a one-line change; N1–N4 are wording). Keep the scope and the leaf.

Validation (scratch detached worktree of memory.ctg a9ab81a with sibling symlinks, `CARGO_TARGET_DIR=<scratchpad>/rv/target`, release):
- `cargo test --release -p graph --lib diskann --no-run`: exit 0, 17.9 s from an empty target.
- Env-gated probe `rv_probe --ignored --nocapture`, all exit 0:
  - HEAD 64 × 40 seeds 3 and 5: 40/2560 reachable, recall 0.000.
  - HEAD 64 × 34: 102/2176 reachable, recall 0.100.
  - `RVFIX=spec`: 2560/2560, recall 1.000, build 10.9 s.
  - `RVFIX=ref` (occlude_list): 2560/2560, recall 1.000, build 8.1 s.
  - `RVNOUT` (paper union only): 40/2560, recall 0.000.
- `diskann` filter with `RVFIX=spec` and with `RVFIX=ref`: 12 passed, 1 ignored, 0.3 s each.
- `sh -eu -c 'cd memory.ctg'` in `/Users/feb/dev/cartridge/memory.ctg`: exit 1.
- Cleanup: both files restored with `git show HEAD:` (status empty), `git worktree remove` exit 0, symlinks removed. The 10k corpus was not re-run; analyst-1's 10k numbers were accepted.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (80/100).
Unresolved blocking findings: B1.
Rounds used / remaining: 1 / 4.
Next action: make one bounded revision (B1, plus N1–N4 as chosen), recompute the digests, and request review round 2.

## Round 2 — 2026-09-16

Presented revision: prd.ctg 5086a167 (both files clean at review time); code memory.ctg a9ab81a.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `4c04a6503b27df627f9cde82497bc2e16936080d43d07adb405e72cba66afb79` (matches hand-off) |
| Specs | `specs/spec01.md` sha256 `24e33841cd124352bd4bcd0bd0dbc8e0b0a19b31ed6399d73a2a6c8fbc953e94` (matches hand-off) |
| Material contracts/dependencies | memory.ctg a9ab81a `src/graph/src/diskann.rs` (`robust_prune` :111, `build_adjacency` :197, `cos_dist` :58), `src/graph/src/graph.rs:580-665`, `src/config/src/config.rs:717`, `src/tick/src/tick_pulse.rs:80-96`, `src/commands/src/{commands_graph_ops,commands_check,commands_hub,commands_export}.rs`; engine `prd.ctg/src/lifecycle.ts:36-47,125-168`; microsoft/DiskANN `occlude_list` (in-mem index) |

### Round-1 findings

- **B1: resolved.** No `cd`. The block is `CARGO_TARGET_DIR=<abs> cargo test --release -p graph --lib diskann`, has no relative paths, and `sh -n` exits 0. Both `collect` cwds (the lane worktree, then `memory.ctg` after the ff-merge, `lifecycle.ts:161-163`) are the workspace root. The heading `## Verify and Proof` matches `/^##\s+(?:Verify|Verification|Proof)\b/i`.
- **N1: resolved, with a precision gap (N5).** The spec now describes one sorted pool, one occlusion factor per candidate, pick at `occlude <= cur_alpha`, update later unchosen `k` with `max(occlude, d(p,k)/d(j,k))`, `+inf` at `d(j,k)==0`, and stop at `r`. This matches upstream. `cos_dist` = 1−cos is proportional to squared L2 on the unit sphere, so the ratio lines up with upstream's squared-L2 ratio. Differences from upstream:
  - Upstream's schedule is `cur_alpha = 1; while cur_alpha <= alpha && |result| < R { …; cur_alpha *= 1.2 }`. The spec's `{1.0, alpha}` is identical at the default 1.2, and every production caller uses `Params::default()`. It differs for alpha in (1, 1.2), where upstream runs only 1.0, and for alpha > 1.44, where upstream runs more steps.
  - Upstream skips the update when `occlude[t] > alpha`. That is a performance shortcut only.
- **N2: resolved.** The epoch-fresh reuse (`diskann.rs:178-181`, `graph.rs` `open_snapshot`), the stale reconcile, and the full build on a missing directory are stated correctly. The trigger list understates recovery a little: `import` (`commands_export.rs:266`) and the tick `DiskConsolidate` task also consolidate. The "delta outgrows it" item is `tick_pulse.rs:80-96`. Harmless.
- **N3: resolved** (`disk_threshold` 0, `config.rs:717`, stated in Outcome).
- **N4: mostly resolved.** The beam is pinned to `search(q, 10, 96)` and the 10k bound is 84 s (1.5 × 56 s). Two gaps remain:
  - The destination is only "the implementer's report", with no path.
  - The PRD was not trimmed: 383 words, against the 150–300 target.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Reproduced silent recall loss on the default path (every store-backed graph). One outcome, two-file footprint. −2: PRD body is still 383 words (N4 trim not taken). |
| Ownership and reuse | 19 | Correct owner and file. Reuses `build_adjacency`, `medoid`, `brute_topk`, `DiskIndex::search`, and the probe corpus. Callers are unchanged. −1: the `{1.0, alpha}` schedule is presented as upstream `occlude_list` without saying it simplifies the ×1.2 escalation (N5). |
| Dependencies and implementable slices | 19 | No `needs`. The integration order ahead of the cold-tier child is stated. One small spec. −1: warming the target is still only a comment. Risk is low, because after a worktree path switch the shared target recompiled only `graph`, in 3.1 s. |
| Observable acceptance and baseline evidence | 17 | Both new tests fail at a9ab81a as pinned and pass with the spec's prune (see Validation). −1: nothing prints the build time and Verify runs without `--nocapture`, so the 1.5× bound rests on an unspecified manual measurement (N6). −1: the failing-output destination has no path. −1: query noise and RNG continuation for the 20 recall queries are not pinned. The result is robust either way, because reach at HEAD is one cluster. |
| Failure, recovery and compatibility | 18 | The on-disk format is unchanged. The byte-identical test and the 12 existing tests pass under the new prune. Recovery is described accurately and the lack of a marker is accepted explicitly. −1: recovery triggers are incomplete (import, tick consolidate). −1: `cos_dist` can come out slightly negative from float error for near-duplicates. The spec guards only `== 0`, so a tiny negative `d(j,k)` yields a negative ratio that never occludes (N7). |
| Reviewer total | 91 / 100 | |

Findings (none blocking):
- **N5:** in step 2, say "for `cur_alpha` = 1.0, then ×1.2 while `<= alpha` (upstream). At the default 1.2 this is {1.0, 1.2}", or label `{1.0, alpha}` as a deliberate simplification. Optionally skip the update when `occlude[k] > alpha`.
- **N6:** have `diskann_build_reaches_every_node_on_clustered_corpus` `eprintln!` the `build_adjacency` elapsed time, and measure with `-- --nocapture` at a9ab81a and after the fix. Name the report path (e.g. the lane report or `collection.md`).
- **N7:** treat `d(j,k) <= 0.0` as `+inf`.
- Carry-over: trim the PRD toward 300 words and add import and tick consolidation to the recovery triggers.

Disposition: keep. Proceed to implementation. N5–N7 can be folded in by the implementer without another round.

Validation (scratch detached worktree of memory.ctg a9ab81a at `<scratchpad>/rv2/memory.ctg`, sibling symlinks `memo.ctg`/`cartridge.ctg`, `CARGO_TARGET_DIR=<scratchpad>/rv/target`, release):
- Added two tests exactly as spec step 1 pins them: 64 × 40, 1024-d, StdRng seed 3, centres U−0.5, noise 0.6·(U−0.5), `i % 64`, default `Params`, BFS from `medoid` over `build_adjacency`, 20 queries from the continued RNG, `search(q,10,96)`. Also added step 2's prune, written literally from the spec text and env-gated.
- `cargo test --release -p graph --lib diskann --no-run`: exit 0, 3.1 s (only `graph` recompiled).
- HEAD: `reachable 40/2560` FAILED, `recall 0.000` FAILED, 12 passed, 2 failed, build 8.98 s, 9.1 s wall.
- Spec prune: 14 passed, 0 failed (including `the_same_corpus_builds_a_byte_identical_index`), build 9.78 s (1.09×, under the 1.5× bound; the two tests run in parallel), 9.9 s wall. Verify fits easily in 120 s when the target is warm.
- `sh -n` on the extracted Verify block: exit 0.
- 10k was not re-run.
- Cleanup: both files restored with `git show HEAD:` (status empty), `git worktree remove` exit 0 (no --force), symlinks removed.

Reviewer identity: independent reviewer agent r2 (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: PASS (91/100).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation (N5–N7 optional in-lane).

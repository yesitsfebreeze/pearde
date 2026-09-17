# @memory/a-spilled-graph-answers-the-same-queries-as-one-that-never-spilled review history

Plan: `@memory/a-spilled-graph-answers-the-same-queries-as-one-that-never-spilled`,
`prd.ctg/.cartridge/boards/memory/prds/a-spilled-graph-answers-the-same-queries-as-one-that-never-spilled/prd.md`.
Scope: one observable outcome, executable leaf — the spilled DiskANN backend returns the
same top-k ids as the resident one, with the three lowered test floors restored.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. No predecessor slug on this board; the two
`.state/loop/a-spilled-graph*` directories are analyst scratch, not prior reviewed plans.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-17

Presented revision: memory.ctg `1351865eb0e787cf819456aaa201c18eacf74406`. The checkout is
dirty from a concurrent session, none of it inside this PRD's footprint: `M
.cartridge/tests/integration/cartridge.rs`, `M .cartridge/tests/unit/src/cartridge/source.rs`,
`M Cargo.lock`, `M src/cartridge/Cargo.toml`, `M src/cartridge/src/lib.rs`, `M
src/cartridge/src/source.rs`, `?? src/cartridge/src/evidence.rs`. Reviewed against HEAD
content, not the working tree, via `git archive HEAD` into a scratch tree.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `990998520eba138143e0e43b77540c2fb13adf65da496c7ab52e6b757100cfd7` |
| Specs | `specs/spec01.md` — `32c1dbb97285a94957aec11da3e3485d4683e8600153213b7000531e654f61a9` |
| Material contracts/dependencies | memory.ctg 1351865: `src/graph/src/diskann.rs` `6fe4a815…77454`; `.cartridge/tests/integration/spill_transparency.rs` `974117e3…dcb55b`; `src/graph/src/vector_backend.rs` `a0ccb4b2…af1771`; `src/util/src/util.rs` `2e310f69…1cda5bca`; `src/math/src/math.rs` `6eec3ebd…3b10be3f`; reference diff `.state/loop/a-spilled-graph/attempt-diskann-search-rerank.diff` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Restores a real, currently red gate and three floors that were lowered rather than explained; refuses to lower a threshold; scope is two files. Reproduced the red state myself (below). −2: acceptance item 1 ("recorded in the implementer's report") is not machine-checkable and duplicates what the spec's own Cause paragraph already records; the spec also swaps the PRD's stated command (`cargo nextest run -p memory --test spill_transparency`) for `cargo test --release …` without saying it is deviating or why release is required. |
| Ownership and reuse | 15 | Stays inside `memory.ctg` / `graph`, adds no dependency, and correctly refuses to touch `cos_dist`/`greedy`/`robust_prune` — I verified `cos_dist` is a build-path kernel (`src/graph/src/diskann.rs:127`, `:158`, `:241`, `:322`), so changing it would move the persisted graph bytes and break `the_same_corpus_builds_a_byte_identical_index`. That restraint is the right call. −5: finding F2 — the fix hand-rolls a fourth bespoke ranking comparator in the very change that exists because ranking sites diverged, instead of `util::cmp_rank`, which `graph` already depends on (`src/graph/Cargo.toml:14`) and which the spec's own Cause paragraph quotes as "use at every ranking site or top-k regresses to nondeterministic order". |
| Dependencies and implementable slices | 17 | No `needs`; base pinned at 1351865, which is HEAD; two ordered steps; a reference diff that applies cleanly (`patch -p1`, verified). −3: findings F4 and F8 — three of the spec's own line citations in Step 2 are wrong, and the first `TEMPORARY` comment is two lines, so "delete the three TEMPORARY comments" as written leaves an orphan half-sentence that the Verify grep accepts. |
| Observable acceptance and baseline evidence | 15 | Five acceptance items, four of them machine-checked by the two blocks; baseline recorded at both revisions; I independently reproduced both ends (HEAD red at 0.8370, fixed green at 1.0000 ×3). −5: finding F1 — the Cause paragraph's central claim is wrong as stated, and acceptance item 1 asks the implementer to write that wrong cause into the record. −F3 is folded in here: acceptance item 4 and its guard gate on a variable name rather than on behavior. |
| Failure, recovery and compatibility | 14 | Block 2 is a genuine regression guard over reachability, clustered recall, brute-force recall and the byte-identical build, and I confirmed it passes under the fix; the build path is deliberately untouched, so nothing persisted changes and rollback is a two-file revert. −6: the spec states no recovery boundary at all and leaves the PRD's ("revert the prune change in a lane and compare") standing although its own analysis makes it obsolete (F5); it deletes the platform comments and asserts platform independence while `math::cosine` takes an AVX2 path on x86_64 that the test's hand-rolled f32 brute force does not, untested there (F6); it records no latency reading for up to 64 extra distance evaluations per spilled query although the harness that reports `search_us` already exists (F7); and Block 2 discards cargo's log on failure (F8). |
| Reviewer total | 79 / 100 | Below the 90 threshold. No blocking finding. |

### Findings and concrete revisions

- **F1 — the named cause is wrong, and an acceptance item propagates it. (major, not blocking)**
  `specs/spec01.md` "Cause": *"The spilled path is the one ranking site that does not [break
  ties by id]."* It is not. The disk path's hits are ranked by `util::cmp_rank` twice
  downstream — `union_rank` at `memory.ctg/src/graph/src/vector_backend.rs:146` and
  `merge_hits` at `memory.ctg/src/graph/src/search.rs:89`. The id tiebreak is present and
  simply never engages, because `DiskIndex` scores come from its own private f32 kernel
  `cos_dist` (`memory.ctg/src/graph/src/diskann.rs:58`, dot accumulated in f32) rather than
  the shared `math::cosine` (`memory.ctg/src/math/src/math.rs:8`) every other site uses, so
  vectors that tie exactly under the shared kernel get unequal f32 scores and order by noise.
  The other half of the defect is `search_hits_filtered`'s `.take(k)` at
  `memory.ctg/src/graph/src/diskann.rs:512`, which truncates in beam order before any
  id-aware rank runs. This is why the Steps are right and the Cause is wrong: a reader who
  fixed only what the Cause names — adding `.then_with(id)` to the `total_cmp` sort at
  `memory.ctg/src/graph/src/diskann.rs:101` — would change nothing, because under the f32
  kernel those entries are not equal. Rewrite the Cause to name the kernel divergence plus
  the pre-rank truncation, and keep `:490`/`:512` as the file:line the acceptance item wants.
- **F2 — reuse `util::cmp_rank`. (not blocking)** The reference diff sorts with
  `a.0.total_cmp(&b.0).then_with(|| self.ids[a.1].cmp(&self.ids[b.1]))`. `graph` already
  depends on `util` (`memory.ctg/src/graph/Cargo.toml:14`); `util::cmp_rank(1.0 - a.0, id_a,
  1.0 - b.0, id_b)` (`memory.ctg/src/util/src/util.rs:100`) is the identical ordering through
  the shared helper, and the whole PRD exists because one site went its own way. Name it in
  Step 1.
- **F3 — a guard on a variable name, not on behavior. (not blocking)** Acceptance item 4 and
  the block-1 guard `if grep -qn "beam.truncate(k)" src/graph/src/diskann.rs; then … exit 1`
  pass only because the reference diff happens to rename the vector to `ranked`. The spec's
  own Step 1 says to sort "and only then truncate to k" — an implementation that does exactly
  that while keeping the name `beam` is correct and fails the gate. Drop the guard (the recall
  assertion is the behavioural check) or restate it as "truncation does not precede the
  rerank".
- **F4 — wrong line citations in Step 2, and an orphaned comment. (minor)** The asserts are at
  `memory.ctg/.cartridge/tests/integration/spill_transparency.rs:149`, `:154` and `:159`; the
  spec gives `:147`, `:151`, `:155`. The `TEMPORARY` comments are at `:147-148`, `:152` and
  `:157` — the first is two lines, so deleting only the line containing the word leaves
  `// tends to be ~0.85; the original threshold was set on an x86_64 host.` behind, which the
  Verify grep accepts. Say "delete the comment blocks at :147-148, :152 and :157".
- **F5 — no recovery boundary. (minor)** The spec has none, and the PRD's ("revert the prune
  change in a lane and compare before fixing forward") is made obsolete by the spec's own
  finding that a9ab81a shows the same cause. State that explicitly and give the real boundary:
  the change is two files, touches no build path, and moves no persisted byte, so recovery is
  reverting the diff.
- **F6 — the platform claim is asserted, not measured. (minor)** The spec deletes the
  "Apple Silicon" / "x86_64 host" comments and declares the floors platform-independent.
  `math::cosine` takes an AVX2/FMA path on x86_64 (`memory.ctg/src/math/src/math.rs:20-26`)
  that the test's own brute force — a hand-rolled f32 dot at
  `memory.ctg/.cartridge/tests/integration/spill_transparency.rs:52-62` — does not, so the tie
  sets there need not match. Everything was measured on arm64. One sentence recording that
  limit is enough; it does not change the disposition, since 0.99 is where those floors came
  from on x86_64 in the first place.
- **F7 — no latency reading for the rerank. (minor)** `DiskIndex::search` gains up to one
  extra `vec_at` + `math::cosine_distance` per beam member on every spilled query, and this
  path runs with L = max(2k, 64) = 64. Nothing gates it —
  `memory.ctg/.cartridge/tests/integration/spill_memory.rs:202` reports `search_us` and, by
  its own note at `:20`, asserts none of it — so this is not a regression risk, but the spec
  should record the number from the harness it already has.
- **F8 — Block 2 throws its diagnostics away. (minor)** `cargo test … > "$log" 2>&1` under
  `sh -eu` exits before anything prints the log, so a regression in the four guarded diskann
  tests yields an exit code and no output. `|| { cat "$log"; exit 1; }`.
- **F9 — the 120 s budget is NOT a blocking finding. (informational)** Measured below:
  the whole of block 1, from a deleted `CARGO_TARGET_DIR`, is 23 s wall against the 120 s
  per-block limit — 18.32 s to build 237 crates in release plus three runs of ~1.2 s. That is
  roughly 5× headroom and better than the analyst's 1 m 04 s. Both figures fit, on both the
  lane pass and the integrated pass. The margin exists because `~/.cargo/config.toml` sets
  `rustc-wrapper = "kache"`, a user-global compile cache the collector inherits; on a cold
  kache cache a 237-crate release build would not fit 120 s, but that condition applies to
  every cargo Verify block in this repository and to nothing this spec controls. Optional
  cheapening if the margin is ever wanted back: the test is deterministic (the byte-identical
  build check inside it pins that, and the analyst observed identical numbers on every run),
  so the 3× loop buys little — but it comes from the PRD's acceptance, so leaving it is fine.

### Validation

All commands run by the reviewer, `sh -eu -c`, verbatim from the spec.

1. Block 1 at HEAD, cwd `/Users/feb/dev/cartridge/memory.ctg`: **exit 1**, immediately, with
   no output — it fails on its first guard, `grep -q "cold_recall >= 0.99"`, because the
   lowered floors are still in the file. Fails for the spec's reason, not a mechanical defect.
2. Block 2 at HEAD, cwd `/Users/feb/dev/cartridge/memory.ctg`: **exit 0** in 10 s. Block 2 is
   a pure regression guard and does not discriminate the fix; it is green before and after.
   That run was warm — the analyst left a 593 MB `memory.ctg/target/spill-transparency-verify`
   in the live checkout (timestamped 01:05–01:08), so it is not a cold-build datapoint.
3. Cold reference measurement, cwd `<scratchpad>/wt` (a `git archive HEAD` copy with
   `memo.ctg`/`cartridge.ctg` symlinked as siblings — `src/cartridge` has a path dep on
   `../../../memo.ctg/evidence` at HEAD, and cargo loads every workspace manifest even for
   `-p memory`; the board's `.lanes/` directory already carries those symlinks, so the lane
   pass is unaffected), reference diff applied with `patch -p1` and the three floors restored,
   `target/` deleted first: block 1 verbatim → **exit 0**, 23 s wall, `Finished release
   profile … in 18.32s`, three runs printing
   `recall@10 vs brute force: resident=1.0000 spilled=1.0000; spilled-vs-resident
   overlap=1.0000, top1 agreement=1.0000`, each test 1.2 s. Block 2 verbatim in the same fixed
   tree → **exit 0**, `test result: ok. 14 passed; 0 failed; 1 ignored`.
4. HEAD reproduction, cwd `<scratchpad>/wt2` (unmodified `git archive HEAD`):
   `cargo test --release -p memory --test spill_transparency` → **exit 101**,
   `recall@10 vs brute force: resident=1.0000 spilled=0.8370; spilled-vs-resident
   overlap=0.8370, top1 agreement=1.0000`, `panicked at
   .cartridge/tests/integration/spill_transparency.rs:146:5: spilled DiskANN recall@10 vs
   brute force regressed: 0.8370`. Exactly the reported failure.
5. Source claims checked directly, all confirmed: `beam.truncate(k)` at
   `src/graph/src/diskann.rs:490` inside `pub fn search` at `:482`; the beam sort with
   `total_cmp` alone at `:101`; the private f32 `cos_dist` at `:58`; `util::cmp_rank` at
   `src/util/src/util.rs:100`; the three `TEMPORARY` floors at
   `.cartridge/tests/integration/spill_transparency.rs:147/152/157` with their asserts at
   `:149/:154/:159`; all four test names named in block 2 exist in
   `.cartridge/tests/unit/src/graph/src/tests/diskann_test.rs`.

No write was made to `memory.ctg` source, index or history. The only bytes the reviewer added
under it are gitignored build artifacts in the pre-existing `target/spill-transparency-verify`,
from running block 2 verbatim as instructed.

Disposition: revise. The fix is the right fix and it works — keep the Steps and the reference
diff; correct the Cause, route the comparator through `util::cmp_rank`, drop or reword the
name-based guard, fix the Step 2 citations, and add the three missing sentences (recovery,
platform limit, latency). All of that is one bounded editing pass on the spec; it changes no
measured behaviour, so round 2 should clear 90 without re-measuring anything but the Verify
blocks.
Reviewer identity: reviewer subagent (Claude Opus 5, 1M context), session
`64c5884a-23a2-41ab-acec-67431416100e`, dispatched by the memory-board coordinator; independent
of the analyst that wrote spec01.
User rating: not supplied; not required under delegation.
User feedback/provenance: none for this revision.
Result: FAIL — 79/100, below the 90 threshold, with no blocking finding.
Unresolved blocking findings: none. The 120 s Verify budget (F9) is explicitly not blocking.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of `specs/spec01.md` addressing F1–F8, then round 2.

## Round 2 — 2026-09-17

Presented revision: memory.ctg `1351865eb0e787cf819456aaa201c18eacf74406`, unchanged from
round 1. `spec01.md` rewritten in place; `prd.md` unchanged; the reference diff rewritten too
(mtime 01:24). Live checkout dirty only in the concurrent session's `src/cartridge/*` — seven
paths, none in this footprint.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `990998520eba138143e0e43b77540c2fb13adf65da496c7ab52e6b757100cfd7` (unchanged) |
| Specs | `specs/spec01.md` — `a5169ecf9587117986363832e5dcb48505abebb0266fcf17ea73f798f24e2185` (was `32c1dbb9…54f61a9`) |
| Material contracts/dependencies | memory.ctg 1351865, unchanged since round 1: `src/graph/src/diskann.rs` `6fe4a815…77454`, `.cartridge/tests/integration/spill_transparency.rs` `974117e3…dcb55b`; reference diff `.state/loop/a-spilled-graph/attempt-diskann-search-rerank.diff` — `5219e4f2…5754b81` (rewritten) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Still one outcome, two files, no threshold lowered, and the new Recovery / Platform limit / `--release` sections make the plan self-contained. −4: the spec now prescribes a per-query rescoring pass over the whole beam that its own evidence does not support and that measurement contradicts (B1). The minimal fix that makes this test green is strictly smaller — rank the beam the greedy walk already produced through `cmp_rank`, add no distance evaluations — and I measured it at 1.0000. |
| Ownership and reuse | 19 | F2 resolved and real, not nominal: the reference diff was rewritten and now maps through `math::cosine` and sorts with `util::cmp_rank(a.0, a.1, b.0, b.1)`; it compiles and the test passes (verified). The refusal to touch `cos_dist`/`greedy`/`robust_prune` is kept and its justification re-verified — `cos_dist` is the build-path kernel at `src/graph/src/diskann.rs:127`, `:158`, `:241`, `:322`. −1: the reuse is argued as causally required rather than as the consistency improvement it actually is. |
| Dependencies and implementable slices | 19 | F4 resolved and verified by replay: executing Step 2 exactly as written (delete `:147-148`, `:152`, `:157`; raise the asserts at `:149`, `:154`, `:159`) produces a file with zero occurrences of `TEMPORARY`, `Apple Silicon` or `x86_64 host`. Base still pinned to HEAD; the rewritten reference diff applies with `patch -p1`. −1: the Cause still writes `.then_with(|id)`, which is not Rust, and the "15-20 s in debug" figure in the `--release` section is unverified here. |
| Observable acceptance and baseline evidence | 11 | The blocks now gate behaviour rather than a variable name, and I confirmed both edges of that: a real behavioural regression fails at the test, not at a grep (mutant C below, exit 101 at `spill_transparency.rs:146`), and a correct sort-then-truncate implementation passes. Block 2 prints diagnostics. −9: the Cause — the PRD's primary deliverable, and what acceptance item 1 instructs the implementer to record — states a mechanism I falsified by direct measurement (B1), and the statistic it leans on does not support it. |
| Failure, recovery and compatibility | 15 | Recovery and Platform limit are new, accurate and independently checked: `math::cosine`'s AVX2/FMA path is x86_64-only (`src/math/src/math.rs:20`, `:42`, `:96`), the test's brute force is a hand-rolled f32 dot (`spill_transparency.rs:52-62`), `spill_memory.rs` really is `#![cfg(target_os = "linux")]` at `:24` and really asserts nothing at `:202`, and `the_same_corpus_builds_a_byte_identical_index` really is what proves no persisted byte moves. F8 resolved and verified. −5: the Latency section's explanation is false on the platform it measured, and its reported effect is smaller than the noise (F10). |
| Reviewer total | 80 / 100 | Below the 90 threshold, and one blocking finding. |

### Findings and concrete revisions

- **B1 — BLOCKING. The rewritten Cause is measurably wrong, and acceptance item 1 would write
  it into the record.** `specs/spec01.md` "Cause" now presents two halves and says both must
  go: the private f32 kernel `cos_dist` (`memory.ctg/src/graph/src/diskann.rs:58`) turning
  exact ties into "two unequal f32 scores", plus truncation before the id-aware rank. It then
  states the consequence explicitly: *"adding `.then_with(|id)` to the beam sort at
  src/graph/src/diskann.rs:101 would change nothing: under `cos_dist` those entries are not
  equal in the first place."* I tested both halves separately, in a scratch tree, on the
  spec's own test:
  - **Mutant C — shared kernel, no id tiebreak** (`math::cosine` kept, `util::cmp_rank`
    replaced by `util::cmp_partial` on score alone): `spilled=0.8370`, identical to HEAD, test
    FAILS at `spill_transparency.rs:146`. The kernel swap on its own fixes nothing.
  - **Mutant D — old kernel, id tiebreak only** (no rescoring at all; the beam's existing f32
    `cos_dist` distance ranked through `util::cmp_rank` before truncating):
    `resident=1.0000 spilled=1.0000 overlap=1.0000 top1=1.0000`, test PASSES.
  So the id tiebreak is necessary *and sufficient*, and the kernel divergence is neither. The
  quoted consequence is the opposite of what happens: under `cos_dist` the tied entries **are**
  bit-equal, because the corpus's vectors give an exactly representable f32 dot and identical
  norms, so a tiebreak alone resolves them the same way brute force does. The statistic the
  Cause leans on — "1964/2000 spilled scores not bit-equal to the brute-force score" — is a
  comparison against brute force's *different* formula (an unnormalised f32 dot,
  `spill_transparency.rs:52-62`), not evidence about ties within the beam, and it has been
  read as if it were.
  Consequence beyond the record: the spec buys, on that false premise, up to `beam_l` = 64
  extra `vec_at` + `math::cosine` evaluations on every spilled query, on the cold-tier
  retrieval path, for no measured behavioural gain.
  Revision: state what is measured — the beam is ordered without the one tiebreak and is
  truncated at `:490`/`:512` before anything id-aware runs; ranking it through `util::cmp_rank`
  before truncating is necessary and sufficient, measured at 1.0000. Keep the `math::cosine`
  swap only if it is argued on its own merits (one kernel per repo law; robustness on a corpus
  whose ties are *not* exactly representable), priced honestly as added work — not as a cause.
  Then correct acceptance item 1, which currently names `:58` as a cause.
- **F10 — the Latency section's explanation is false on the platform it measured. (not
  blocking)** It reads *"no regression, because the shared SIMD-pathed kernel is cheaper per
  call than what the beam already pays."* There is no SIMD path on this host: every vector
  path in `memory.ctg/src/math/src/math.rs` is `#[cfg(target_arch = "x86_64")]` (`:20`, `:42`,
  `:96`), so on arm64 `math::cosine` is `cosine_scalar` (`:29-40`), the same three
  multiply-accumulates per element as `cos_dist` (`src/graph/src/diskann.rs:61-73`). The
  rerank therefore strictly adds work and cannot be cheaper. The reported effect is also below
  the instrument's resolution: the claimed 1.14 → 1.09 s is 0.05 s, while my three runs of the
  *identical* fixed tree gave 1.21 / 1.23 / 1.20 s and a mutant run of near-identical work gave
  1.35 s — a spread of 0.15 s, three times the claimed effect, in a measurement dominated by
  three 1000-entity index builds. Keep the numbers, drop the causal claim, and say the cost is
  below what this instrument can resolve.
- **F11 — half 2 of the Cause is partly inert. (minor)** The Cause names `beam.truncate(k)` at
  `src/graph/src/diskann.rs:490` and `.take(k)` at `:512` as one defect. On the path this test
  exercises only `:512` bites: `search_hits_filtered` calls `search(query, want, want)` with
  `want = search_l.max(k)`, so inside `search` `k == beam_l` and `:490` truncates nothing.
  Measured — mutant B, the accepted fix with the raw beam truncated to k *before* rescoring,
  still gives `spilled=1.0000` and passes. `:490` is not dead in general (`search` is `pub`
  and the diskann unit tests call it with `k < search_l`), but it is not part of this failure.
- **F12 — carried from round 1, unfixed: `.then_with(|id)` (Cause) is not valid Rust.**
  Cosmetic.
- Round-1 findings F2, F3, F4, F5, F6, F8 are **resolved and independently verified** (see
  Validation). F7 is resolved in substance — the `spill_memory.rs` cfg claim is true and the
  substitute instrument is the right shape — but its interpretation is F10.

### Validation

All commands run by the reviewer, `sh -eu -c`, blocks verbatim from the revised spec.

1. **Negative control — block 1 at HEAD, cwd `/Users/feb/dev/cartridge/memory.ctg`: exit 1**,
   instantly, on the first guard, with no cargo invocation and no `target/` directory created.
   The probe really was cleaned up: `src/graph/src/diskann.rs` still digests to
   `6fe4a815…77454` and `spill_transparency.rs` to `974117e3…dcb55b`, both identical to round
   1, and `git status --short` shows exactly the other session's seven `src/cartridge/*` paths.
   The 593 MB `target/spill-transparency-verify` is gone and I did not recreate it — every
   cargo run below was kept out of the live checkout deliberately.
2. **Block 1, fixed tree, cold: exit 0**, 21 s wall against the 120 s limit
   (`Finished release profile … in 16.67s`, then three runs at 1.21 / 1.23 / 1.20 s), each
   printing `recall@10 vs brute force: resident=1.0000 spilled=1.0000; spilled-vs-resident
   overlap=1.0000, top1 agreement=1.0000`. Tree: `git archive HEAD` + the rewritten reference
   diff via `patch -p1` + Step 2 applied exactly as written, `target/` deleted first, siblings
   symlinked.
3. **Block 2, same tree: exit 0**, 11 s, `test result: ok. 14 passed; 0 failed; 1 ignored`.
4. **F4 orphan case — block 1: exit 1** with
   `a lowered-floor comment survives in .cartridge/tests/integration/spill_transparency.rs:
   x86_64 host`. Built by deleting only the lines containing `TEMPORARY` and raising the
   floors, which leaves `// tends to be ~0.85; the original threshold was set on an x86_64
   host.` at `:147`. The new guard catches exactly the case round 1 raised.
5. **Mutant B — accepted fix, raw beam truncated before the rescore:** `spilled=1.0000`,
   passes. (F11.)
6. **Mutant C — accepted fix with `util::cmp_rank` replaced by score-only `util::cmp_partial`:**
   `resident=1.0000 spilled=0.8370 overlap=0.8370 top1=1.0000`, panic at
   `spill_transparency.rs:146`, `test result: FAILED`, cargo exit 101. Confirms block 1 fails
   on a behavioural regression at the assertion rather than at a grep.
7. **Mutant D — no rescore at all, beam's own f32 `cos_dist` distance ranked through
   `util::cmp_rank` before truncating:** `resident=1.0000 spilled=1.0000 overlap=1.0000
   top1=1.0000`, passes. This is the measurement behind B1.
8. Claims spot-checked directly and found true: `cos_dist` accumulates dot and both norms in
   f32 (`diskann.rs:58-74`); `math::cosine` has no non-x86_64 SIMD path (`math.rs:20/42/96`);
   `spill_memory.rs:24` is `#![cfg(target_os = "linux")]`; `cargo-nextest 0.9.143` is installed,
   so acceptance item 2 is executable; block 2's `|| { cat "$log"; exit 1; }` is well-formed on
   the cargo run and on every grep.

No write was made to `memory.ctg` source, index, history or `target/`. All probes ran in
scratch copies made with `git archive HEAD` under the reviewer's scratchpad.

Disposition: revise. Six of round 1's eight findings are genuinely fixed and I could verify
each one; the plan's mechanics are now sound and its blocks discriminate correctly. What is
left is the same thing that decided round 1, moved rather than removed: the Cause asserts a
mechanism instead of the one the test measures, and this time it is falsifiable in twenty
seconds and false. Fixing it is a paragraph plus one acceptance line, and it makes the fix
smaller, not larger.
Reviewer identity: reviewer subagent (Claude Opus 5, 1M context), session
`64c5884a-23a2-41ab-acec-67431416100e`, same reviewer as round 1, independent of the spec's
author.
User rating: not supplied; not required under delegation.
User feedback/provenance: none for this revision.
Result: FAIL — 80/100, below the 90 threshold, with one blocking finding.
Unresolved blocking findings: B1 — `specs/spec01.md` "Cause" and acceptance item 1 name
`memory.ctg/src/graph/src/diskann.rs:58` (kernel divergence) as half the cause and assert that
an id tiebreak alone would change nothing; measured, the tiebreak alone is sufficient
(spilled 1.0000) and the kernel swap alone is useless (spilled 0.8370).
Rounds used / remaining: 2 / 3.
Next action: one bounded revision of the Cause, acceptance item 1 and the Latency paragraph,
then round 3.

## Round 3 — 2026-09-17

Presented revision: memory.ctg `1351865eb0e787cf819456aaa201c18eacf74406`, unchanged from
rounds 1 and 2. `spec01.md` rewritten in place; `prd.md` unchanged; the rescoring reference
diff deleted and replaced by a tiebreak-only one.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `990998520eba138143e0e43b77540c2fb13adf65da496c7ab52e6b757100cfd7` (unchanged since round 1) |
| Specs | `specs/spec01.md` — `1b3218a53db59000c45c1ac2b27e41c5ce53099e1aca32accf76c9afa42a0249` (was `a5169ecf…f24e2185`) |
| Material contracts/dependencies | memory.ctg 1351865, unchanged since round 1: `src/graph/src/diskann.rs` `6fe4a815…77454`, `.cartridge/tests/integration/spill_transparency.rs` `974117e3…dcb55b`; reference diff `.state/loop/a-spilled-graph/attempt-diskann-search-tiebreak.diff` — `b8dde546…5678eb93`; `attempt-diskann-search-rerank.diff` deleted (confirmed) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome, two files, eight lines of code, no threshold lowered, and — the round-2 deduction now reversed — no work added to the cold-tier query path at all. This is the minimal change that makes the claim true. −1: n2, the `--release` section's "15-20 s in debug" is off; I measured the debug run at 27.45 s. |
| Ownership and reuse | 20 | `util::cmp_rank` applied at the one ranking site that lacked it, no local comparator, no new dependency, build path untouched with its justification re-verified (`cos_dist` at `src/graph/src/diskann.rs:127`, `:158`, `:241`, `:322`). The rejected alternative is kept in the record with the measurement that rejects it, which is how a design decision should read. |
| Dependencies and implementable slices | 19 | No `needs`; base is HEAD; Step 2 replayed exactly as written produces a file with zero occurrences of `TEMPORARY`, `Apple Silicon` or `x86_64 host`; the reference diff applies with `patch -p1` and is the artefact I measured. −1: n1 and n3 below. |
| Observable acceptance and baseline evidence | 19 | The Cause is now exactly what the ablation supports, and acceptance item 1 requires both arms and both numbers as its evidence. Both load-bearing claims verified character-by-character against source (below). The blocks discriminate at both edges: negative control exits 1 instantly, and a tiebreak regression fails at the assertion (round 2, mutant C, exit 101). −1: n4 — block 2 gates 14 of the graph package's 179 tests. |
| Failure, recovery and compatibility | 19 | Recovery, Platform limit and Latency are each accurate and each independently checked. Blast radius verified clean beyond the gated tests: the full `-p graph` suite passes 178/179 under the fix (1 ignored, 0 failed), and the only other consumer of the spilled backend outside these tests asserts backend variant, not order (`.cartridge/tests/unit/src/commands/src/commands_serve/entry_point_tests.rs:338`, `:365`). −1: the x86_64 limit is stated and scoped but nothing in the plan would detect a divergence there; acceptable, and named rather than hidden. |
| Reviewer total | 96 / 100 | At or above the 90 threshold, with no blocking finding. |

### Findings and concrete revisions

All three round-2 findings are resolved, and the blocking one is resolved on evidence rather
than by assertion.

- **B1 (round 2) — RESOLVED.** The Cause is rewritten to the mechanism the ablation supports:
  the beam is ordered by distance alone at `src/graph/src/diskann.rs:101`, `.take(k)` at
  `:512` is the live truncation, and `util::cmp_rank` at `src/graph/src/vector_backend.rs:146`
  and `src/graph/src/search.rs:89` cannot repair an order whose tied candidates are already
  gone. The kernel story is now stated as the false alternative it is, with both arms and both
  numbers in the spec, and acceptance item 1 requires them as the report's evidence. The two
  arms in the spec's table match the two I measured in round 2 (arm A = my mutant D, 1.0000;
  arm B = my mutant C, 0.8370), and I re-confirmed arm A today by running block 1 against the
  new reference diff. The withdrawn 1964/2000 statistic is gone.
- **The claim that decides whether the fix is principled — verified.** `search_hits_filtered`
  emits `score: 1.0 - dist as f64` at `src/graph/src/diskann.rs:515`; the new sort key is
  `1.0 - a.0 as f64` over that same f32 `dist`. Same expression, same numbers, so the ordering
  inside `search` and the ordering at `union_rank` are now one function. It is also
  order-preserving in the strict sense: f32→f64 is exact and `1.0 - x` is injective over these
  values, so the sort creates and destroys no ties — the only thing it can change is which of
  two *equal* distances comes first. Not coincidental.
- **The secondary argument — sound, and stronger than the spec claims.** `util::cmp_rank` is
  `cmp_partial(&b_score, &a_score).then_with(|| a_id.cmp(b_id))` (`src/util/src/util.rs:106`),
  so the id comparison is reached only on `Equal`. Its one loophole — `cmp_partial` maps
  incomparable to `Equal` — cannot fire here, because `cos_dist` returns early with `1.0` on a
  length mismatch and on a zero norm and otherwise divides by a positive product, so it never
  yields NaN. Combined with the order-preservation above, arm A moving 0.8370 → 1.0000 is
  attributable to tie reordering and nothing else, which settles the bit-equality question
  round 2 raised.
- **F11 (round 2) — RESOLVED and verified.** `search_hits_filtered` computes
  `let want = search_l.max(k)` and calls `self.search(query, want, want)`
  (`src/graph/src/diskann.rs:507-509`), so inside `search` `beam_l = k` and `beam.truncate(k)`
  at `:490` cuts nothing on this path. The spec now says exactly that and cites `:512` as the
  live truncation.
- **F10 (round 2) — RESOLVED.** "Cheaper per call" is withdrawn. The new paragraph claims no
  figure and shows why it cannot: 1.23/1.28/3.05/1.57/1.29 s at HEAD against 1.22/1.21/1.19/
  1.23/1.20 s with the fix, a 1.8 s spread on unchanged code. That is the honest reading. My
  own three runs of the fixed tree (1.14/1.11/1.09 s) sit inside it.
- **F12 (round 2) — RESOLVED.** The invalid `.then_with(|id)` sentence is gone.
- **n1 (nit).** "eight added lines" counts code only; the diff adds twelve, eight of them code
  and four a comment. Say "eight lines of code" or "twelve lines".
- **n2 (nit).** The `--release` section's "15-20 s in debug" understates it: I measured the
  debug test run at 27.45 s (plus a 26.54 s debug build). The conclusion is unaffected and in
  fact strengthened — three debug runs plus a build is ~109 s against the 120 s limit, which
  is exactly the margin the release profile buys. Correct the figure or drop it.
- **n3 (nit).** "The one ranking site that truncates before the tiebreak is `DiskIndex::search`"
  is loose where the paragraph above it is exact: the truncation that bites is `.take(k)` in
  `search_hits_filtered`.
- **n4 (nit).** Block 2 filters to `--lib diskann`, gating 14 of the graph package's 179 tests.
  I ran the other 164 and they pass, so nothing is hiding there; widening the block to
  `-p graph --lib` would cost nothing measurable (8.63 s against 8.42 s). Optional.

None of n1-n4 blocks implementation, changes a measured number, or makes the record false.

### Validation

All commands run by the reviewer, `sh -eu -c`, blocks verbatim from the revised spec.

1. **Negative control — block 1 at HEAD, cwd `/Users/feb/dev/cartridge/memory.ctg`: exit 1**,
   instantly, on its first guard, with no cargo invocation and no `target/` directory created.
2. **Block 1, fixed tree, cold from a deleted `CARGO_TARGET_DIR`: exit 0**, 20 s against the
   120 s limit (`Finished release profile … in 15.91s`, then 1.14 / 1.11 / 1.09 s), each run
   printing `recall@10 vs brute force: resident=1.0000 spilled=1.0000; spilled-vs-resident
   overlap=1.0000, top1 agreement=1.0000`. Tree: `git archive HEAD` + the new reference diff
   via `patch -p1` + Step 2 applied exactly as written.
3. **Block 2, same tree: exit 0**, 12 s, `test result: ok. 14 passed; 0 failed; 1 ignored`.
4. **Acceptance item 2's second command:** `cargo nextest run -p memory --test spill_transparency`
   → `1 test run: 1 passed, 0 skipped` (cargo-nextest 0.9.143 present, so the item is
   executable as written).
5. **Blast radius:** `cargo test --release -p graph` → `178 passed; 0 failed; 1 ignored`.
   The change breaks nothing outside the filter block 2 gates.
6. **Debug comparison** (to check the `--release` justification): `cargo test -p memory --test
   spill_transparency` → build 26.54 s, `test result: ok … finished in 27.45s`.
7. **Ablation, second confirmation.** Arm A is the new reference diff itself, re-measured at
   1.0000 in run 2 above; in round 2 I measured it independently as mutant D at 1.0000, and
   arm B as mutant C at 0.8370 with the test failing at `spill_transparency.rs:146`. HEAD is
   0.8370. Both arms of the spec's table are reproduced by this reviewer.
8. **Source claims spot-checked:** `src/graph/src/diskann.rs:515` is `score: 1.0 - dist as f64`;
   `:507-509` is `let want = search_l.max(k); self.search(query, want, want)`;
   `src/util/src/util.rs:106` is `cmp_partial(&b_score, &a_score).then_with(|| a_id.cmp(b_id))`;
   `cos_dist` (`:58-74`) cannot return NaN; the only other spilled-backend consumer asserts
   backend variant, not order.

**Live checkout: clean, third round running.** `git status --short` shows exactly the
concurrent session's seven `src/cartridge/*` paths and nothing else; `src/graph/src/diskann.rs`
and `.cartridge/tests/integration/spill_transparency.rs` digest identically to rounds 1 and 2,
so no probe was left applied; `memory.ctg/target/` contains no `spill-transparency-verify`
and I created none. Every cargo run was kept in `git archive HEAD` scratch copies under the
reviewer's scratchpad. No write to `memory.ctg` source, index, history or `target/`; no `prd`
operation; no commit.

Disposition: keep, and implement. The plan now names a cause it proved rather than one it
inferred, prescribes the smallest change that makes the claim true, and gates it with blocks
that fail for the right reason at both edges.
Reviewer identity: reviewer subagent (Claude Opus 5, 1M context), session
`64c5884a-23a2-41ab-acec-67431416100e`, same reviewer as rounds 1 and 2, independent of the
spec's author.
User rating: not supplied; not required under delegation.
User feedback/provenance: none for this revision.
Result: **PASS** — 96/100, at or above the 90 threshold, with no unresolved blocking finding.
This rating applies to `specs/spec01.md` at digest `1b3218a5…a42a0249` and to the reference
diff at `b8dde546…5678eb93`; a substantive later change to either makes it stale.
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: proceed to implementation. n1-n4 are optional and can be folded into the
implementer's pass without another review round.

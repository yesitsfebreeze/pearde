---
complexity: small
footprint:
  - src/graph/src/diskann.rs
  - .cartridge/tests/integration/spill_transparency.rs
---

# spec01 — the spilled beam is ranked by the one tiebreak before it is truncated

Base: memory.ctg 1351865 (HEAD; measured there on 2026-09-17). No `needs`.

## Cause

`DiskIndex::search` returns the greedy beam ordered by distance **alone**: the
beam is sorted with `total_cmp` and nothing else at src/graph/src/diskann.rs:101,
and `search` hands it back in that order (src/graph/src/diskann.rs:482-494). The
live truncation is `.take(k)` in `search_hits_filtered` at
src/graph/src/diskann.rs:512 — `beam.truncate(k)` at :490 cuts nothing on this
path, because `search_hits_filtered` calls `search` with `k = search_l = want`,
so the beam is never longer than the k it is truncated to. So when two entities
tie exactly, which one survives into the top 10 is decided by beam order, i.e. by
which one the walk happened to reach first.

The id tiebreak is not missing from the system and it is not missing downstream:
`util::cmp_rank` (src/util/src/util.rs:100 — "score desc, id asc — the single
ranking tiebreak; use at every ranking site or top-k regresses to
nondeterministic order") does rank disk hits, at `union_rank`
(src/graph/src/vector_backend.rs:146) and at `merge_hits`
(src/graph/src/search.rs:89). It cannot repair the order, because by the time it
runs the tied candidates have already been dropped at :512. The one ranking site
that returns its order before the tiebreak is `DiskIndex::search`; the
truncation that drops the tied ids is `search_hits_filtered`'s `.take(k)`.

This was settled by ablation rather than by reading, because a plausible
alternative story — that `DiskIndex`'s private f32 kernel `cos_dist`
(src/graph/src/diskann.rs:58) makes exact ties unequal, so no tiebreak could fire
— is false. Both arms, measured at 1351865 in a `git archive HEAD` tree
(analyst-1.md, round 3):

| Arm | Change to `DiskIndex::search` | spilled recall@10 | Test |
| --- | --- | ---: | --- |
| A | Rank the beam's **existing** `cos_dist` distances through `util::cmp_rank` before truncating. No rescoring. | **1.0000** | passes |
| B | Rescore through the shared `math::cosine`, compare by score only, no id tiebreak. | **0.8370** | fails at spill_transparency.rs:146 |

HEAD itself is 0.8370. The tiebreak is necessary and sufficient; changing the
kernel is neither. Arm A also proves the ties are bit-equal under `cos_dist`:
`cmp_rank` only reaches its id comparison when `partial_cmp` returns `Equal`, so
recall could not have moved from 0.8370 to 1.0000 unless those beam distances
were numerically equal.

So this is **not** a regression from the 5097a83 prune. That change only
reshuffled which tied id the walk reaches first (0.8410 → 0.8370), spending the
0.001 of margin the 0.84 floor had. The defect predates it — a9ab81a shows the
same cause — and the three "Apple Silicon TEMPORARY" floors in the test are the
same defect written down as a platform excuse, which is why they go back up
rather than staying lowered.

## Steps

1. In `DiskIndex::search` (src/graph/src/diskann.rs:482), sort the beam with
   `util::cmp_rank(1.0 - a_dist as f64, a_id, 1.0 - b_dist as f64, b_id)` before
   `beam.truncate(k)`. That is the whole change: twelve added lines, eight of
   them code and four a comment, no rescoring,
   no new distance evaluation, and `1.0 - dist as f64` is exactly the score
   `search_hits_filtered` already hands downstream at
   src/graph/src/diskann.rs:515, so the ordering here and the ordering at
   `union_rank` are now the same function of the same numbers.
   Use `util::cmp_rank`, not a local comparator: `graph` already depends on
   `util` (src/graph/Cargo.toml:14), and this PRD exists because one ranking site
   went its own way.
   Do **not** rescore through `math::cosine`: arm B above shows it buys no
   recall, and it would add up to `beam_l` = 64 extra `vec_at` plus cosine
   evaluations per spilled query on the cold-tier retrieval path.
   Do **not** touch `cos_dist`, `greedy` or `robust_prune`. `cos_dist` is the
   build-path kernel (src/graph/src/diskann.rs:127, :158, :241, :322); changing it
   moves the persisted graph bytes and breaks
   `the_same_corpus_builds_a_byte_identical_index`. `search_hits_filtered` needs
   no change: its `.take(k)` now truncates an already correctly ranked list.
   Reference diff, applied and measured:
   `prd.ctg/.cartridge/boards/memory/.state/loop/a-spilled-graph/attempt-diskann-search-tiebreak.diff`.
2. In .cartridge/tests/integration/spill_transparency.rs, raise the three floors
   back to the values they were lowered from and delete the whole comment block
   above each one — `:147-148` (two lines; deleting only the line with the word
   `TEMPORARY` orphans `// tends to be ~0.85; …`), `:152` and `:157`. The asserts
   themselves are at `:149` → `cold_recall >= 0.99`, `:154` →
   `hot_recall - cold_recall <= 0.01`, `:159` → `agree as f64 / denom >= 0.99`.
   Keep the RECORDED BASELINE comment above `hot_recall`: it is the measurement
   note, not a lowered floor.

Measured with both steps applied at 1351865 on arm64 (2026-09-17): resident
1.0000, spilled 1.0000, overlap 1.0000, top1 1.0000, on three consecutive runs.

## Why `cargo test --release`, not the PRD's `cargo nextest run`

A deliberate deviation from the PRD's wording, same test binary: the release
profile runs this 1000-entity, 3-build, 600-query test in ~1.2 s against 27.45 s
in debug, so three runs plus a cold build fit the 120 s Verify limit with room,
and both Verify blocks then share one target profile instead of two. The
implementer should still run `cargo nextest run -p memory --test spill_transparency`
once (cargo-nextest 0.9.143 is installed) and record it, since that is the
command the PRD names.

## Latency

The change adds one sort of at most `beam_l` = `max(2k, 64)` = 64 elements per
spilled query and **no** extra distance evaluation. No latency figure is claimed,
because this harness cannot support one: five runs of the test at HEAD measured
1.23 / 1.28 / 3.05 / 1.57 / 1.29 s and five with the fix measured
1.22 / 1.21 / 1.19 / 1.23 / 1.20 s, so the run-to-run spread on unchanged code
(1.8 s) is far larger than any difference between the two. The usual instrument
cannot supply one either: `spill_memory.rs` is `#![cfg(target_os = "linux")]`
(.cartridge/tests/integration/spill_memory.rs:24), compiles to nothing on this
host, and asserts nothing about `search_us` (`:202`) by design. No latency gate is
added.

## Platform limit

Everything here was measured on arm64. Every SIMD path in `math.rs` is x86_64
gated (src/math/src/math.rs:20, :42, :96), and on x86_64 `math::cosine` takes an
AVX2/FMA path that the test's hand-rolled f32 brute force
(.cartridge/tests/integration/spill_transparency.rs:52-62) does not, so the two
tie sets need not coincide exactly there. This does not change the disposition —
0.99 is where these floors came from on an x86_64 host in the first place — but
the claim proven is "the floors hold on arm64", not "on every target".

## Recovery

The PRD's stated recovery ("revert the prune change in a lane and compare before
fixing forward") is **superseded**: a9ab81a, the pre-prune tree, has the same
cause at 0.8410, so reverting the prune would not isolate anything. The real
boundary: the change is two files and twelve lines, touches no build path, and
moves no persisted byte — `the_same_corpus_builds_a_byte_identical_index` in
Verify block 2 is what proves that — so recovery is reverting the diff, with no
index rebuild and no migration. Verify block 2's `--lib diskann` filter gates 14
of the graph package's 179 tests; the rest of the package is the implementer's
blast-radius check, not a gate.

## Acceptance

- [x] The implementer's report records the test result at a9ab81a and at 5097a83 (recall and pass/fail) and names the cause at file:line — the beam ordered by distance alone at src/graph/src/diskann.rs:101 and truncated at src/graph/src/diskann.rs:512 before the id-aware rank at src/graph/src/vector_backend.rs:146 — with the two ablation arms and their two recall numbers (A 1.0000, B 0.8370) as the evidence that it is the tiebreak and not the kernel.
- [x] `cargo test --release -p memory --test spill_transparency` exits 0 on 3 consecutive runs, and `cargo nextest run -p memory --test spill_transparency` (the PRD's command) exits 0 once, recorded in the report.
- [x] .cartridge/tests/integration/spill_transparency.rs contains `cold_recall >= 0.99`, `hot_recall - cold_recall <= 0.01` and `agree as f64 / denom >= 0.99`, and none of `TEMPORARY`, `Apple Silicon` or `x86_64 host` survives in it.
- [x] `DiskIndex::search` orders its beam through `util::cmp_rank` before truncating, adding no local comparator and no rescoring pass.
- [x] The DiskANN reachability, clustered-recall, brute-force-recall and byte-identical-build tests still pass: `cargo test --release -p graph --lib diskann` exits 0.

## Verify and Proof

<!--
Engine facts honoured here: each block runs as `sh -eu -c`, 120 s, twice (lane,
then repo); paths are relative to the repo root; no `cd`; every cargo command
pins CARGO_TARGET_DIR so the live host does not hot-restart on target/debug; no
block writes inside the footprint (block 2 writes only to `mktemp`); no `!`
negation, since it is inert under `set -e`.
Budget: block 1 measured 21-38 s cold from a deleted CARGO_TARGET_DIR against
the 120 s limit, block 2 11-15 s. The negative control — block 1 on an
unmodified HEAD tree — exits 1 instantly on its first guard.
-->

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/spill-transparency-verify}"
f=.cartridge/tests/integration/spill_transparency.rs
grep -q "cold_recall >= 0.99" "$f"
grep -q "hot_recall - cold_recall <= 0.01" "$f"
grep -q "agree as f64 / denom >= 0.99" "$f"
for stale in TEMPORARY "Apple Silicon" "x86_64 host"; do
	if grep -qn "$stale" "$f"; then echo "a lowered-floor comment survives in $f: $stale"; exit 1; fi
done
grep -q "util::cmp_rank" src/graph/src/diskann.rs
for n in 1 2 3; do cargo test --release -p memory --test spill_transparency; done
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/spill-transparency-verify}"
log="$(mktemp -t spill-diskann-verify)"
cargo test --release -p graph --lib diskann > "$log" 2>&1 || { cat "$log"; exit 1; }
for t in diskann_build_reaches_every_node_on_clustered_corpus diskann_recall_on_clustered_corpus recall_at_10_is_high_vs_brute_force the_same_corpus_builds_a_byte_identical_index; do
	grep -q "$t ... ok" "$log" || { cat "$log"; exit 1; }
done
grep -qE "^test result: ok\." "$log" || { cat "$log"; exit 1; }
```

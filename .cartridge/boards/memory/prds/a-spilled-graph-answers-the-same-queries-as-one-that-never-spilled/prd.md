---
state: "done"
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
footprint:
- ".cartridge/tests/integration/spill_transparency.rs"
- "src/graph/src"
- "src/retrieval"
commit: "e1d5569e49670a0f940f0f6b71356adb1d06bb19"
---

# A spilled graph answers the same queries as one that never spilled

## Outcome

`memory::spill_transparency a_spilled_graph_answers_the_same_queries_as_one_that_never_spilled`
fails at memory.ctg 5097a83 with recall@10 0.8370 against a 0.84 floor, on 2 of 2 runs
(observed 2026-09-16 by the trust-fixture analyst). Find out whether this is a regression
from the DiskANN prune change (5097a83, collected today as
`@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point`) or pre-existing at
a9ab81a. Fix the cause without lowering the threshold unless the test's floor is shown to
be wrong.

## Acceptance

- [x] The test's result at a9ab81a and at 5097a83 is recorded (pass/fail and recall), and the cause is named at file:line.
- [x] `cargo nextest run -p memory --test spill_transparency` exits 0 on 3 consecutive runs, with the threshold unchanged or its change justified by evidence in the spec.
- [x] The DiskANN reachability and recall tests still pass.

## Proof and recovery

If this is a regression from 5097a83, revert the prune change in a lane and compare before fixing forward.

## Verification qualification (2026-09-17)

A fresh verifier re-ran both Verify blocks, the blast-radius check and both
owner gates, and reproduced the ablation a third time from its own scratch copy
and its own arm patches: pristine HEAD spilled 0.8370 and FAILED at
`spill_transparency.rs:146`, arm A (`util::cmp_rank` over the existing
`cos_dist` distances) 1.0000 and ok, arm B (rescore through `math::cosine`,
score-only compare) 0.8370 and FAILED. Both spec numbers reproduce to the digit.
Cold block 1 measured 27 s against the engine's 120-second limit.

One qualification. The `a9ab81a` arm of acceptance line 1 — the 0.8410 figure
before the prune — was not re-derived; the verifier did not check out or build
that revision, so that number rests on the analyst's record rather than on
observation in this pass. The `5097a83` figure was proved transitively instead:
`5097a83..HEAD` is a single commit touching none of `src/graph/src`, `src/math`
or `spill_transparency.rs`, so the observed 0.8370 at `1351865` is also the
`5097a83` result.

`just test memory` fails at
`memory_cartridge --lib engine_tests::health_overtakes_blocked_ingestion_and_dispose_drains_it`
(`Elapsed(())`, `engine_test.rs:137`). The verifier confirmed it independently
as pre-existing: with both of this PRD's files restored to their HEAD content
the failure reproduces identically, and the test passes in isolation. It is an
order-dependent flake in another session's tree, recorded as further evidence on
[[@memory/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them]].

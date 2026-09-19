# @memory/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence review history

Canonical plan: @memory/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence. Threshold: 90/100 with no blocking findings. Round limit: five. Inherited rounds: none. This record rates plans, not product behavior.

## Round 1 — 2026-09-19

Reviewer: `/root/memory_plan_review_a`. Plan SHA256: `85a05276ceaba0cde2499d911fd8bb4df888c106108bc9b6bea1e09c62fd4f44`. Specs: not yet published. Source evidence: [pinned source digests](../evidence/source-digests.json).

| Dimension | Score / 20 |
| --- | ---: |
| User value and scope | 19 |
| Ownership and reuse | 19 |
| Dependencies and implementable slices | 18 |
| Acceptance and baseline evidence | 19 |
| Failure, recovery and compatibility | 19 |

Total: **94/100 — PASS**. No blocking finding; retain the bounded specification recommendations in the full review.

[Full independent findings](../evidence/review-a-round-1.md), SHA256 `66e68ecee39fb7e453cf96e672e7094c0b96cf8c8aac1f6238cda23e4ea0fdea`. Validation: targeted source, PRD and dependency reads; no behavioral tests run by the reviewer. Coordinator test evidence is separately attributed in the investigation. User rating: not requested under delegated policy. Rounds used: 1; remaining: 4.

## Round 2 — 2026-09-19, executable writer specification

Reviewer: `/root`, independent of analyst `/root/baseline_audit`. **94/100 PASS**, no blocking findings. Scope 19, ownership 19, boundaries 19, executable proof 19, recovery 18. Three rounds remain. This rates the specification, not implementation.

PRD SHA256 `e6aecf2426063e2b3d749e88bea22dd443004b670473b206229067284ebc98b9`. Specification SHA256 `541bf2960f5c04c533659128460da9e91bc54902ba07516be771457d21d55220`. Reproduction report SHA256 `364f87d7765d4133ea20229a92ad90dac4df79514f105caf4fbb462d1cf4fd13`. Source baseline is memory `ff22be8dda3814e79b4d830c9904261b167af160`.

The reviewer read the executable specification, actual bootstrap save, registry closure, RPC drain, store commit and existing experience tests. The analyst's named controlled probe executed twice and identifies the advancing ordinary writer only in that controlled interleaving. The specification correctly does not turn it into proof of historical live causation. One per-store gate protects durable commit through epoch publication without extending graph locks over ordinary serialization/I/O. Lock order and unrelated-store progress are explicit; stale prepared snapshots and genuine external advances still refuse. Existing status owns the automatic/operator-required distinction and no parallel API is introduced.

Required implementation evidence includes the actual-flush barrier, real RPC concurrency, unrelated dirty RAM durability, crash before reply and named-test execution. Do not report a successful baseline characterization as repaired behavior. Added store-core initialization and bootstrap tests are within the reconciled footprint. README/help changes must be reconciled with preserved dirty tails during collection. The existing per-engine pass lock remains necessary; the store gate alone does not deduplicate separately captured batches. Future quality/latency and loaded integration gates remain outstanding.

## Round 3 — 2026-09-19, maintenance preservation and corrupt epoch refusal

Reviewer: `/root`, independent of implementer `/root/baseline_audit`. **94/100 PASS**, with no blocking findings. Scope scored 19, ownership 19, boundaries 19, acceptance 19 and recovery 18. Three rounds have been used and two remain. This records the substantive contract review; independent implementation verification remains required before collection.

PRD SHA256 is `02c1ee4157f1d4a0534996f0dfe3ffd6976bc80baf1762cb8718f3801537034e`. Specification SHA256 is `49ca15f61d79291bec7a02719d99b654646bf856b4aae03c527d6ecf8571840c`.

The reviewer read the full amended specification and bootstrap, store-core and RPC diffs. Independent verification exposed an existing maintenance path that could replace dirty RAM during the ordinary writer publication window or after an external advance. Two new actual-function tests failed before correction, then passed after correction. Maintenance now acquires the store coordinator before graph access and reports divergence without automatically replacing RAM. The exact footprint includes the existing commands regression, its maintenance explanation and store-core corruption tests.

Fallible authoritative epoch reads and transactional decode-error propagation close the corrupt-as-zero write hole while retaining the legacy advisory accessor. Tests require a corrupt epoch to refuse the write without pruning durable rows. The implementation preserves the prior stale-snapshot comparison and does not make historical live causation claims. The root reviewer authorized this amendment as necessary to satisfy the existing RAM-preservation acceptance; no unrelated scope was added.

No collection is authorized by this review alone. The independent verifier must execute the amended named tests and confirm the final source footprint.

### Round 3 editorial amendment

The root reviewer authorized a comment-only correction in `src/commands/src/commands_serve.rs` and its exact footprint addition. The maintenance-loop comment now describes operator-required divergence and preserved RAM instead of automatic adoption. No executable behavior or contract changed, so the substantive Round 3 disposition remains PASS. Updated PRD SHA256 is `5ec97542f3ae3be6e1f1b10a492a30e1801536c8e67443092cd90a2db0a3ef65` and specification SHA256 is `19e9ed3c40ebdbacc10fe1f136449c4661f6b0d4026ad213bc2cd966a26a0434`.

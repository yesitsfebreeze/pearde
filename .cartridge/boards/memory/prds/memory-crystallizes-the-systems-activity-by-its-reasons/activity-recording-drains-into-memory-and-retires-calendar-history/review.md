# activity-recording-drains-into-memory-and-retires-calendar-history review history

Plan: memory::activity-recording-drains-into-memory-and-retires-calendar-history, [prd.md](prd.md). This is an executable leaf dependent on the graph experience contract. Round limit is five, with a passing threshold of 90/100. There are no inherited rounds. The independent reviewer is `/root/architecture_review`; the user delegated ratings and supplied no numeric rating.

## Round 1 — 2026-09-19

The reviewed plan was an uncommitted document with SHA-256 `a6ff715f18f43ad6503553473e1ed64f62c158dfed8c7e4fd1e7fb2bc086c325`, on composition baseline `8850e0c96e4af5fda15c399ee2af595a0e12ee17`. Runtime source inputs are recorded in round 2 below and were unchanged between these reviews. Specs were not yet applicable.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | The leaf removes parallel calendar history and makes memory authoritative. |
| Ownership and reuse | 18 | The physical legacy table is reused as intake, with the graph as history. |
| Dependencies and implementable slices | 17 | Graph experience is declared, but concurrency with ordinary graph flush was underspecified. |
| Observable acceptance and baseline evidence | 17 | Restart and integration proof were named, but interleaved flush proof was missing. |
| Failure, recovery and compatibility | 15 | Disk atomicity did not cover already-mutated live graph state; receipt growth and expiry were unspecified. |
| Reviewer total | 87 / 100 | The revision failed. |

Blocking findings: specify how failed commits restore live graph state and how epoch guards prevent stale full snapshots from erasing committed activity. Add an interleaved ordinary-ingest/flush test. Specify inbox and receipt capacities, expiry and retry semantics rather than only payload and batch bounds.

Disposition: revise. Result: FAIL. Rounds used: one; remaining: four. This was source and plan review only; no runtime verification was claimed.

## Round 2 — 2026-09-19

The revised uncommitted plan has SHA-256 `a9b9f2682658abf7cc05fd62e21dfff3ede3f652657e83c1e363e8fb0c606edd`. The coordinator captured existing runtime changes in implementation worktree snapshot `1d1bb31`; these content digests bind the review independently of that snapshot.

| Input | SHA-256 |
| --- | --- |
| Revised plan | `a9b9f2682658abf7cc05fd62e21dfff3ede3f652657e83c1e363e8fb0c606edd` |
| Graph prerequisite PRD | `2d35b8e4552cc2672ab304551b46856f31f44bd2b24017154282087ce0b55e41` |
| `memory.ctg/src/base/src/base_types.rs` | `d79ce2c6f52236afa717112075a95829312ff4353c213918b7cb239142455f95` |
| `memory.ctg/src/graph/src/accept.rs` | `f260f020fc77abb80ff3c654c0afbb297cbc537d2339f48ab4565ba47da0c979` |
| `memory.ctg/src/graph/src/persist.rs` | `b0e76223992d7541beee471072b5efcc3f4f0d45761a9872b425ef5780cace97` |
| `memory.ctg/src/store/core/src/lib.rs` | `cb884dc2f885bffac0fe427147887ff22f1064266e4573bb0f97a2e2f59941f8` |
| `memory.ctg/src/tick/loop/src/tick_cluster.rs` | `e6cb32a1f02e1ce14dc3ed4e103d9a5c222762e9bce0a74a79589fc3a888de65` |
| `memory.ctg/src/tick/loop/src/tick.rs` | `039339bc4d04bf08c4da52f137943d349e9edba2eb0c86e7fd945b5cb24c1c92` |
| `memory.ctg/src/tick/loop/src/tick_tasks.rs` | `5f130dde8df4b1893c043db3fdd28b0d1479e99ab67ded6ead3caf85536e828b` |
| `memory.ctg/src/rpc/src/trace/table.rs` | `3e61d84c55574c754f1d41ca1dce690ea02b4a1a8ad65a54e6f04a226a18ea89` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |

Specs are not yet applicable: this review assesses the executable PRD contract before implementation.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | The authoritative memory outcome remains intact. |
| Ownership and reuse | 19 | Intake, receipts and historical migration share the existing store, without another history engine. |
| Dependencies and implementable slices | 18 | The prerequisite is explicit and the critical commit boundary is concrete. |
| Observable acceptance and baseline evidence | 18 | Interleaved stale flush, failed commit retry, restart and isolated live service proof are named. |
| Failure, recovery and compatibility | 18 | A touched-memory undo set, epoch-guarded transaction, explicit bounded capacities and age refusals address round 1. |
| Reviewer total | 93 / 100 | The revised plan passes. |

All round-1 blockers are resolved in the reviewed contract. Implementation must validate timestamps against the same clock basis used for receipt expiry and reject implausible future timestamps, so receipts cannot expire while a delivery still passes the age gate. Atomic migration must retain old rows on failure. The undo set must include newly created memories and restore ownership/vector indexes, not only entity maps. These are concrete consequences of the stated transaction and retry guarantees.

Validation consisted of rereading the revised plan and the store epoch/flush contract, then executing `shasum -a 256` successfully from `/Users/feb/dev/cartridge`. No runtime test was executed during planning review. Implementation proof remains required.

Disposition: keep. Result: PASS. Unresolved blocking findings: none. Rounds used: two; remaining: three. Next action: implement the reviewed contract and run its named verification, including concurrency failure paths.

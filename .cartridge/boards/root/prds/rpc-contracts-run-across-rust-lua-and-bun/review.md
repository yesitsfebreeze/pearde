# rpc-contracts-run-across-rust-lua-and-bun (root draft) review history

Plan: `@root/rpc-contracts-run-across-rust-lua-and-bun`, `prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md`.
Scope: a leaf created on 2026-09-14 from the restored work memo `.cartridge/memos/work/rpc-contracts-run-across-rust-lua-and-bun.md`. That memo was active and had no PRD or work-map entry.
Round limit: 5. Passing threshold: 90/100 from the agent reviewer. Ratings are delegated to agents.
Inherited rounds: none. No round-1 record exists in `reviews/round-1/` or `OPEN-WORK-REVIEW.json`.

Use the shared [review method](../../../../workflows/review-plan.md).

## Round 1 — 2026-09-14

Presented revision: the working-tree draft. Root is `24aa2be`, cartridge.ctg is `c9ef10b`, and prd.ctg has uncommitted changes.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` at round 1: SHA-256 `e7caf65b2289ece750b82517d20f5583e7008ded7e585c971b0f7ae0e389d296` |
| Specs | Not yet applicable |
| Source memo | `.cartridge/memos/work/rpc-contracts-run-across-rust-lua-and-bun.md` `240868b9…55b2` |
| Contracts | `cartridge.ctg/docs/transport.txt` `23602086…2486`; `src/transport/rpc.rs` `f18c8d6f…a3a`; `src/node.rs` `7c60864b…e7`; `tui.ctg/src/wire.ts` `d4e02182…99a9` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 9 | The draft is built on a TypeScript `wire.ts` peer. cartridge.ctg `ee7e295` says "the transport is internal to the base; provide, call, the Rust SDK crate and wire.ts are gone", and a node is only ever `cartridge node` on `init.lua`. |
| Ownership and reuse | 8 | The transport is internal to cartridge.ctg. A cases file there that a root test reads crosses repositories. The draft also ignores the existing tests in `rpc.rs` and `host.rs`. |
| Dependencies and implementable slices | 9 | The draft says "no hard needs", but its TypeScript checks need either a port or a TypeScript node, and both are out of scope. The root gate files are untracked. |
| Observable acceptance and baseline evidence | 10 | Several checks already pass: error objects, notifications, closed waiters, oversized frames and `timed_out`. The "applicability row" wording lets any failure pass. |
| Failure, recovery and compatibility | 10 | The draft gives no next step after an incompatible baseline. It misses the boundary that is real today: a `cartridge.spawn` helper that exits with requests pending. |
| Reviewer total | 46 / 100 | |

Findings and concrete revisions:
1. BLOCKING: the premise contradicts the current architecture. Resolution: rewrite the plan around the two boundaries that exist, the JSON↔Lua conversion and the `cartridge.spawn` line protocol.
2. BLOCKING: wrong owner, and the fixture crosses repositories. Resolution: rehome to the runtime board with `repo: cartridge.ctg`, keep the tests under `cartridge.ctg/.cartridge/tests`, and use the cargo gates.
3. BLOCKING: the baseline claims work that already exists. Resolution: list the existing tests as proof, remove the escape hatch, and probe the missing behavior first.
4. Non-blocking: the orphaned `wire.ts` copies in tui, live, auth and prd need owner decisions. Resolution: reported to the coordinator, excluded from this plan.
5. Non-blocking: the history was wrong. The deleted file was `.cartridge/tests/unit/src/tests/fixtures/rpc/cases.json` in `939e7d1`. Lua runs inside the Rust node, so there are not three speakers.
6. Non-blocking: transport ids are never reused (they come from an `AtomicU64`). Resolution: the id check now targets the helper's request ids.

Disposition: rehome. The revised plan is [`@runtime/rpc-contracts-run-across-rust-lua-and-bun`](../../../runtime/prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md), which inherits this round. Retire this draft path; nothing was deleted.
Validation: read-only existence checks (ls, grep, git show, shasum). No product gates were run.
Reviewer identity: independent read-only plan-review subagent (claude-opus-5), session_01JsptcAXJhvDpVftHVmataq.
User rating: not required under delegation.
User feedback/provenance: none supplied for this plan.
Result: FAIL.
Unresolved blocking findings: none at this path. All were resolved by the rehomed revision.
Rounds used / remaining: 1 / 4, carried to the runtime plan.
Next action: review round 2 at the runtime path.

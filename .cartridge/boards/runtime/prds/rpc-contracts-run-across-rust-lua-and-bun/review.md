# @runtime/rpc-contracts-run-across-rust-lua-and-bun review history

Plan: `@runtime/rpc-contracts-run-across-rust-lua-and-bun`, `prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md`.
Scope: one leaf, the value fidelity and pending-request lifecycle at the JSON↔Lua boundary and the `cartridge.spawn` boundary in cartridge.ctg `src/node.rs`.
Round limit: 5. Passing threshold: 90/100 from the agent reviewer. Ratings are delegated to agents.
Inherited rounds: 1, from the root draft [`@root/rpc-contracts-run-across-rust-lua-and-bun`](../../../root/prds/rpc-contracts-run-across-rust-lua-and-bun/review.md), which is now marked superseded-recommend-retire.
Source: the restored work memo `.cartridge/memos/work/rpc-contracts-run-across-rust-lua-and-bun.md` (`status: active`, owner `codex-work-2026-09-12/rpc-contracts`, written against the pre-transport core). It stays as history, and its claim was not taken over. The slug is not in `work-map.json`; that mapping is left to the coordinator.

Use the shared [review method](../../../../workflows/review-plan.md).

## Round 1 — inherited, 2026-09-14

Root draft `e7caf65b…d296`, 46/100 FAIL, with 3 blocking findings:
- The TypeScript `wire.ts` peer no longer exists (`ee7e295`).
- The draft had the wrong owner, and its fixture crossed repositories.
- Its baseline claimed behavior that was already tested.

All three were resolved by rehoming the plan here and rewriting it around the real boundaries.

## Round 2 — 2026-09-14

Presented revision: `prd.md` SHA-256 `8f3805125d31f600a1045defa0e863122e9dbf02a6c6d465baff2a877e174350`. Sources: cartridge.ctg `c9ef10b`, root `24aa2be`.

| Input | Content digest |
| --- | --- |
| Plan | `8f380512…4350` |
| Specs | Not yet applicable |
| Contracts | `cartridge.ctg/src/node.rs` `7c60864b…e7`; `docs/transport.txt` `23602086…2486`; `src/transport/rpc.rs` `f18c8d6f…a3a` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | These are the two real boundaries since `ee7e295`. The reviewer confirmed the suspected defect in `node.rs:399-474`: `pending` senders outlive EOF. Two outcomes share one small leaf. |
| Ownership and reuse | 18 | Runtime board, cartridge.ctg fixtures dir, `host.rs` harness reused. The review record link did not resolve. |
| Dependencies and implementable slices | 17 | A `/bin/sh` helper may be denied by the macOS sandbox, which adds only the canonical path. The `spawned` filter matched no new test names. |
| Observable acceptance and baseline evidence | 17 | Checks are bounded and probe-first. "Equal JSON" on the helper path collides with `request` injecting `id` and wrapping in `{data}`. |
| Failure, recovery and compatibility | 18 | Confined to `node.rs` with the API unchanged. A request made after the helper exits was left unspecified. |
| Reviewer total | 87 / 100 | |

Findings (none blocking):
- F1: grant the shell variants and probe helper start under the sandbox first.
- F2: compare `reply.data`, keep `id` out of the value cases, specify that a request after exit fails promptly, and keep the helper marked closed.
- F3: name the tests `a_spawned_…` and filter on that.
- F4: add this review record.

Disposition: revise. Revision `36fbfa7b4ddb90e95f767f360b84ffd2a4e692b8fa94341495653474cf485913` addresses F1–F4 (295 words, 3 checks).
Validation: read-only source reading and existence checks by the reviewer. No product gates were run.
Reviewer identity: independent read-only plan-review subagent (claude-opus-5), session_01JsptcAXJhvDpVftHVmataq.
User rating: not required under delegation. User feedback: none supplied.
Result: FAIL (below 90).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: round 3 agent review of revision `36fbfa7b…5913`.

## Round 3 — 2026-09-14

Presented revision: `prd.md` SHA-256 `36fbfa7b4ddb90e95f767f360b84ffd2a4e692b8fa94341495653474cf485913` (295 words, 3 checks). Source: cartridge.ctg `e8a4da3`. The contract digests are unchanged from round 2: `node.rs` `7c60864b`, `transport.txt` `23602086`, `rpc.rs` `f18c8d6f`. After scoring, only the frontmatter `review-status` changed to `passed`, with no semantic change.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | These are the real `node.rs` boundaries, and the EOF defect is confirmed in source. Two outcomes share one leaf, and the historical slug still says "bun". |
| Ownership and reuse | 18 | Runtime board, cartridge.ctg fixtures, `host.rs` harness, and the review links resolve. The work-map entry is still missing, and the origin memo is still active under its old owner (recorded, not reclaimed). |
| Dependencies and implementable slices | 19 | F1 fixed: sandbox grants for the shell variants and builtins only. F3 fixed: `cargo test --workspace a_spawned` matches `host.rs:395` plus the new tests. |
| Observable acceptance and baseline evidence | 18 | F2 fixed: compares `reply.data` with no top-level `id`. "Fails naming that case" is explicit, but the probe must list the cases that took that path. |
| Failure, recovery and compatibility | 19 | Pending requests and requests after exit both fail within 1 s, the helper stays closed, and the API is unchanged. |
| Reviewer total | 92 / 100 | |

Findings (none blocking):
- N1: record `e8a4da3` as the source, and have the new tests call the existing `trust(dir)` helper before boot.
- N2: add the slug to the work map, or have the coordinator accept the gap, before claiming.
- N3: the probe record lists every value case that failed loudly.

Disposition: keep.
Validation: independent read-only source reading and digest checks. No product gates were run.
Reviewer identity: independent read-only plan-review subagent (claude-opus-5), session_01JsptcAXJhvDpVftHVmataq.
User rating: not required under delegation. User feedback: none supplied.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: the coordinator settles the work-map entry (N2). After that, an implementer may claim, probe first (N1, N3), then implement.

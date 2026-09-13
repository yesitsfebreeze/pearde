# Harness scoped roster proof

Isolated owner commit `df93d5bbc036aee0ac2a08beecb9b18a85fa3835`, based on committed Harness `ca7eeabd38f4eaba69063cf98e2071df694a1dc3`. Every declared source file matches the final captured proof snapshot. The lane is clean. Original `src/main.rs` and `.cartridge/tests/integration/working.rs` remain separately dirty and were not changed by this worker.

The adapter binds an optional actor and environment-backed credential at startup. It captures one Sessions roster during request resolution, validates the actual observed projection, then uses the existing Landscape context collector. A bounded escaped untrusted data block follows template rendering. Captured evidence is reused through inspection and compaction, included in the existing serialized request budget, and never treated as template instructions.

Final disposable composition receipt: `integration/cartridge-roster-verification-OVMUtv.json`; identity `9b7d6e8701371ecb3b6c0c25b2721358b0f0f55c016882496b95a711f3b9d177`. It records every copied source hash/mode, selected repository heads, exact commands and full stdout/stderr, both binary hashes and resulting composed lock hash. Every copy was checked against captured input bytes; source files were checked again after copying. A dedicated debug=0, incremental=0 target limits disk use without reducing test scope.

- Public Harness tests: **44 passed** — 38 unit, 4 process, 1 ring and 1 working test.
- Public `just check harness`, `just build harness`, `just build sessions`: passed.
- Actual native Sessions–Harness SDK bridge: **4 tests / 241 assertions** passed.

The bridge creates 20 scoped records plus an outsider and legacy forged parent. It verifies exactly one roster lookup per request, bounded output with correct omissions, escaped closing-frame and template-like text, hidden other-scope/transcript/inbox/pending content, and live phase changes without new posts. Watched unread counts appear in the prompt and update after explicit acknowledgement. Disabled configuration makes no roster call; copied JSON config and credentials cannot override host bindings. Wrong request actor avoids the roster call. Invalid source identity/digest, upstream failure containing a synthetic secret, and deadline expiry remain explicit nonfatal evidence states. A 1024-byte block retains source revision and omission metadata. Corrupt actual channel state yields partial evidence while session phases remain available. Forced compaction invokes the summarizer, reuses one captured roster, retains the latest user request and leaves the original transcript unchanged.

The verifier retains failed development snapshots as evidence: an omitted Frame initializer caused the initial compile failure, then an undersized fixture did not force the intended whole-row omission. Both were corrected; no test assertion was weakened. Subsequent successful snapshots precede the final proof and remain separately identified.

Original-checkout integration and collection remain pending. Coordinator must resolve the separate existing same-file edits, integrate the reviewed owner commit, update the composed Harness dependency list with existing Landscape, and rerun the verifier against the integrated owner (or `--committed` selection for the parent rollup). Prior Harness receipts that bind main.rs also need the new src/roster.rs module and revalidation. This lane proof does not mark the original roster rollup or broader harness-consumes-landscape work complete.

## Reconciled original edits

After independent coordinator review, the original summary-fallback changes were applied unchanged in a separate clean integration lane. Candidate `d3a4187bf946e02a4806082994e0aac662c1d0c3` preserves both the roster and the user's main.rs/working.rs edits, with an added failed-refresh roster bridge case. All 44 public tests and five actual SDK tests pass; see reconciliation-proof.json and original-delta-review.md for exact inputs and outputs. This is the coherent candidate for coordinator integration. The standalone feature commit above remains separately evidenced.

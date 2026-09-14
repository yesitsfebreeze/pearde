# A memory document is discovered, read, executed, and improved live — review

Canonical PRD: [memory-document-works-end-to-end](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [memory-document-works-end-to-end](../../reviews/round-1/memory-document-works-end-to-end.md): reviewer 86/100; Resequence. Separate the first memory execution proof from arbitrary-depth board discovery; retain recursive discovery as an explicit later integration gate.
  Original SHA-256: `3590a83bc0e23ded9383ffa62501916f7a43e2d2fb21f5d66793aac67f15b7ac`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `7c93c0ec10e829710564408bcebae5d0fde7b4fb7d73a0e97f670535b9fdbf27`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: the plan relied on a separate document runner and the landscape composition. Now: memory serves its own surface (memory.ctg `9cc0f0b`; memory.ctg/.cartridge/help.md: `tool.memory` query/ingest, `memory` service, `context.memory`); landscape is dissolved (decision the-fabric-lives-in-core); the runner leaf `@runtime/one-runner-executes-documents/document-artifact-result` names `cartridge.ctg/src/runtime.rs` and `service.rs`, which do not exist; the memory-tool submodule was dropped (root `9e4cde8`/`bc2c190` per direction digest), mooting `memory-consumer-parity`. Rebased onto the existing isolated smoke profile (`.cartridge/tests/integration/smoke.test.ts` already composes memory), dropped the three needs, added concrete ingest/readback/denial/restart checks and gate `just smoke memory` (to be created). Pre-revision SHA-256 `b728bb7e7c051bee9168c1697522b6f5642b3df36a0338279f69c48509bd9f01`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 17 | First end-to-end proof of an owner surface, still wanted. -3: 'document' framing replaced; improvement-loop part of the old title dropped. |
| Ownership and reuse | 18 | Reuses the smoke fixture and memory's own surface. -2: fixture lives in the root composition while behavior is memory's. |
| Dependencies and slices | 18 | No remaining hard needs. -2: dropping three needs held in other boards needs coordinator acknowledgement. |
| Acceptance and baseline | 19 | Four observable checks with exact-id readback, policy denial via `config.lua`, restart persistence and a named configuration error. -1: new smoke target must be created. |
| Failure and compatibility | 18 | Disposable profile, no user bank, run alone while mcp/proxy smoke is red, discovery/quality deferred to the composed gate. -2. |

Agent score: **90/100 — PASS**.
Findings: Dependency edges removed from this PRD only; the targets themselves are left to their boards.
Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator acknowledges the dropped needs; then implement the smoke target.

### Citation correction after the round above — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Coordinator correction: decision memo `the-fabric-lives-in-core` is outdated; cartridge.ctg `939e7d1` deleted core `src/graph.rs`, `src/fabric.rs`, `src/evidence.rs`. The fabric graph is `memo.ctg/src/fabric_graph.rs` and the evidence contract is the crate `memo.ctg/evidence` (memo `8d6a803`); owner memo, gate `just test memo`.
Change (citation only): replaced the link to that decision memo with source/commit evidence.
- Before: `the landscape board is dissolved ([the-fabric-lives-in-core](../../../../../../.cartridge/memos/decision/the-fabric-lives-in-core.md))`
- After: `the landscape board is dissolved (no landscape.ctg; its fabric graph now lives in `memo.ctg/src/fabric_graph.rs` after cartridge.ctg `939e7d1`)`
SHA-256 before `7c93c0ec10e829710564408bcebae5d0fde7b4fb7d73a0e97f670535b9fdbf27`, after `691ea69e0aa0c2a939fe4aa894793d3cd598b3018bfd19ba7d46cdf4ca5e371f`. No acceptance, need, owner, gate or scope changed, so the score, result and round count above stand; no round consumed. Earlier mentions of that decision in this history refer to the outdated memo; the facts relied on (op renamed to `fabric`, landscape dissolved, fabric owned by memo) are verified in source.

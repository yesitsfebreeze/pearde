# A document reads bounded session history — review

Canonical PRD: [@sessions/sessions-document](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [capabilities-live-with-their-owners](../../../root/reviews/round-1/capabilities-live-with-their-owners.md): reviewer 84/100; Split. Create independently claimable owner migrations; connect shell work to PTY input ownership and preserve direct-FS parity before retirement.
  Original SHA-256: `990147ebe7129477ba49047e365acf0292465529cb96a5c5c1d6b91b6ddc58e6`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE**. The prior need `@mcp/clients-share-document-execution` is an open, stale rollup whose shared document runner has no implementation in current mcp, agent or proxy source (`rg -i document` finds only embedded `cartridge.json` constants and proxy's `documents` contributor). Decision `a-cartridge-brings-its-own-surface.md` (decided_by user, 2026-09-14) places each cartridge's surface in the cartridge and marks read-only ops via `reads` (memo, memory, fs, docs already do). Outcome still wanted: `list` is unpaged (`sessions_inner` in `sessions.ctg/src/main.rs`) and sessions provides no `tool.*` descriptor.
Stale revision: `24389261b3f1d55bf53885cb5b0e773aa3dc192909685b8dd9d83f0d6ff1a14f` (dead start link, dependency on a mechanism that does not exist).
Presented revision: prd.md SHA-256 `9dc447077f0a50feeff7b5a9bbb136b3006dd60de212bfc89487781b6973c450`. Source inspected at sessions.ctg e9725e8 (ported to transport 0d4310f), memo.ctg 9a1cf99, agent.ctg working tree, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: dropped the mcp need (recorded here); paged `list` with stale-cursor refusal; distinct `get` outcomes; mutation-free proof by hashes; tool binding and `reads` delegated to the chat leaf.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Bounded inspection is useful. -3: renamed outcome; the original "document" intent is replaced by decision rather than confirmed with the requester. |
| Ownership and reuse | 19 | Owner-local, reuses `recovery.rs` diagnostics. -1: sibling `*-document` PRDs (router, pty, …) still assume the runner. |
| Dependencies and slices | 19 | No hard needs; independent of chat leaf. -1: shared `main.rs` footprint. |
| Acceptance and baseline | 18 | Stale cursor, three distinct outcomes, byte-hash non-mutation. Current gate baseline: `.cartridge/memos/note/release-status.md` records 8 failing sessions workspace tests; the plan requires naming them before judging new failures. -2. |
| Failure and compatibility | 17 | Opt-in paging, legacy shape kept. -3: cursor encoding/lifetime across restart unspecified. |
| Reviewer total | **90 / 100** | |

Result: **PASS**. Blocking findings: none. Coordinator: the `capabilities-live-with-their-owners` family and `@mcp/clients-share-document-execution` need the same reconciliation.
Validation: file existence; `rg` over mcp/agent/proxy for a document runner; `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: claimable now.

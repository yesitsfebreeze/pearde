# Landscape answers across kernel, directories, memo, memory, and live state — review

Canonical PRD: [@landscape/landscape-composes-system-context](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [landscape-composes-system-context](../../../root/reviews/round-1/landscape-composes-system-context.md): reviewer 85/100; Split. Freeze contributor/status/read contracts and baseline first; stage memory, live-state and file adapters separately and include their actual owner footprints.
  Original SHA-256: `a42df9f537bf0a35558deb445fce5cb9b51b47bde400c3f5e2b51e65b54fd2eb`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE**. Composition now happens in memo's `context` op (`memo.ctg/src/context.rs`), which serves `documents`/`kernel` and asks injected `context.<kind>` providers: `context.memory` in `memory.ctg/src/source.rs`, `context.file` in `fs.ctg/src/main.rs`, consistent with decision `a-cartridge-brings-its-own-surface.md`. Children: context-contributor-contract done, memory-context-contributor done, @memo/landscape-context-facade done, live-file-context-contributors open (its live-owner facade is `stale-after-owner-split`). Not DELIVERED: no `context.<live>` provider exists in source.
Stale revision: `ef941f40741d8598e22dee5c665cc937a6bfb5cd586937c8ab1f01d78c19407a` (typo owner key, repo cartridge.ctg, landscape naming, no integration gate).
Presented revision: prd.md SHA-256 `1c1e7b52d9be8342879e60da5cfda5454e658e012b307501ce440d4d37bad3ac`. Source inspected at memo.ctg 9a1cf99, memory.ctg c25af4d, sessions.ctg e9725e8, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: owner memo; delivered children stated; end-to-end and provider-removal acceptance plus concrete integration gate.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | One query across sources; residual live/file scope identified. -1: live owner not named. |
| Ownership and reuse | 19 | Providers owned by their cartridges per decision. -1: board alias landscape. |
| Dependencies and slices | 18 | All four needs resolve; three done. -2: the open child is itself a rollup with a stale-after-owner-split facade. |
| Acceptance and baseline | 18 | Provider-removal `absent` status already exercised in `memo.ctg/.cartridge/tests/integration/context.test.ts`. -2: the TS integration test is not wired into `just test memo`; the bun command is named separately. |
| Failure and compatibility | 18 | Removal leaves other rows unchanged. -2: no rollback statement for the integration fixture itself. |
| Reviewer total | **92 / 100** | |

Result: **PASS**. Blocking findings: none.
Validation: file existence; `rg` for `context.<kind>` providers across cartridges; `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: coordinator rehomes to memo board; the live-file rollup needs its own reconciliation.

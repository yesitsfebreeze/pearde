# The root landscape searches every child cartridge's development record — review

Canonical PRD: [@landscape/recursive-development-graph](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [recursive-development-graph](../../../root/reviews/round-1/recursive-development-graph.md): reviewer 91/100; Keep. Strong identity, traversal and inactive-source checks; turn depth/count/byte bounds and cursor invalidation into explicit fixture parameters during analysis.
  Original SHA-256: `7c6fda62b070e70f1ce2276761ad99be78c275d6c4b87a0762184791c893534b`.

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
Reconciliation verdict: **REBASE**. Census and search live in memo (`memo.ctg/src/sources/census.rs`, `sources/search.rs`, `source_search.rs`; memo.ctg a458148 exposed recursive search natively). Board records are reached only through prd's `source.board` key (`prd.ctg/cartridge.json`, `prd.ctg/src/service.ts`), per decision `a-cartridge-brings-its-own-surface.md` / `invert-memo-context-sources`. Children: census done; root-search specced (round 3 passed); refresh open/stale.
Stale revision: `ec2531257457ec98c4c7cd82328dc9977b3467b47f0d5fcb7d449ae7edd0909c` (typo owner key, repo cartridge.ctg, no integration gate).
Presented revision: prd.md SHA-256 `5789053f9b3ed791fa15d33b40eeb74efade33b5777f6ebd915420d354b0914d`. Source inspected at memo.ctg 9a1cf99, memory.ctg c25af4d, sessions.ctg e9725e8, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: owner memo; source.board boundary; three-level integration and provider-absent acceptance; gates `just test memo`, `just test prd`, bun source-search test.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Root reads every descendant record. -2: bounds (depth/count/bytes) deferred to children without restating limits. |
| Ownership and reuse | 19 | memo search, prd provides source.board. -1: board alias landscape. |
| Dependencies and slices | 18 | needs resolve; census done. -2: refresh leaf still cites landscape paths. |
| Acceptance and baseline | 18 | Provider-absent behavior matches `declaration_failure("unavailable")` in `source_search.rs`. -2: edit-refresh check duplicates the refresh leaf rather than integrating it. |
| Failure and compatibility | 18 | Cartridge roots survive board absence. -2: no statement on source-only vs callable runtime state in integration. |
| Reviewer total | **91 / 100** | |

Result: **PASS**. Blocking findings: none.
Validation: file existence, `source.board` provider confirmed, `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: coordinator rehomes to memo board; rebase recursive-source-refresh.

# Landscape quality and cost are tested against a versioned corpus — review

Canonical PRD: [@landscape/context-quality-is-measured](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [context-quality-is-measured](../../../root/reviews/round-1/context-quality-is-measured.md): reviewer 86/100; Resequence. Capture the corpus and old-path baselines before the replacement selector lands; define measurable regression tolerances and fixture sizes.
  Original SHA-256: `d4357ac7cf0b610600f4e48d5a080cfa891ac4845efd645d36f379b0a6a928e9`.

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
Reconciliation verdict: **REBASE**. The selector under test moved from the dissolved landscape library to memo (`memo.ctg/src/context.rs`, `memo.ctg/evidence`, `memo.ctg/src/fabric_graph.rs`; cartridge.ctg 939e7d1, memo.ctg 8d6a803). Round 1 asked to capture the old-path baseline *before* the replacement landed; it has landed, so that sequencing premise no longer holds.
Stale revision: `857a0c4ea094b58af525e3ff40e4ccbcf2972fb8f949f193107a4841626fd687` (frontmatter key typo `capability-capability-owner`, repo cartridge.ctg, no integration gate).
Presented revision: prd.md SHA-256 `96fee5f05ba9accb3dbed8222b65260fd7b0b127f9222659e2ac88c95974c0fa`. Source inspected at memo.ctg 9a1cf99, memory.ctg c25af4d, sessions.ctg e9725e8, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: owner key fixed and set to memo; baseline default is the memo revision pinned at corpus freeze, with the landscape snapshot optional; integration acceptance and gate added.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Measurable context quality/cost remains wanted. -2: baseline redefinition should be confirmed when the corpus leaf is claimed. |
| Ownership and reuse | 18 | memo owns both selectors under test. -2: board alias landscape. |
| Dependencies and slices | 17 | needs resolve (`prd check` exit 0). -3: both child leaves still cite `landscape.ctg` and `just test landscape` and are not executable until rebased. |
| Acceptance and baseline | 19 | Parent adds one-invocation comparison and a named failure for missing baseline. -1: comparison command does not exist yet (explicitly created by the gate leaf). |
| Failure and compatibility | 18 | Missing checkout fails by name. -2: no statement on corpus fixture storage location under `.cartridge/tests/`. |
| Reviewer total | **90 / 100** | |

Result: **PASS** (parent plan). Blocking findings: none for the parent; the two child leaves must be rebased before any claim.
Validation: file existence, `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: coordinator rehomes to memo board and assigns rebase of context-baseline-corpus and context-comparison-gate.

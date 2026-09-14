# parked-memory-remains-recallable — review

Canonical PRD: [@memory/parked-memory-remains-recallable](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [parked-memory-remains-recallable](../../../root/reviews/round-1/parked-memory-remains-recallable.md): reviewer 86/100; Merge. Reconcile with MEMORY-004 and current hot/cold retrieval implementation; add pre-top-k mixed/cold fixtures and bounded cold readback without hiding parked candidates.
  Original SHA-256: `4377d15088d909157c49941adc6ff426b8e85182cdf361f5c36011a208bf33ba`.

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

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.
Reconciliation verdict: **REBASE — much of the tier behaviour exists (`cold_candidates` joins fusion pre-top-k in `src/retrieval/piece/src/retrieval_query.rs`; cold fallback in `id_detail.rs`; tier invariants in `.cartridge/tests/integration/memory_contract.rs`). Gaps: no three-layout invariant test; a cold read error fails the whole query (`src/rpc/src/server.rs`, `src/commands/src/commands_query.rs`); cold scan unbounded in I/O. Old starting files wrong.**

Presented revision: `prd.md` SHA-256 `ea42abbd0a31dbed49c0774e6cc6cf387a8cf0635f266941221bd1d715019d07`. Rebased in this round (prior text `817a960d5efe304abde1fa322b95d441ac92d462daebd433e45fffd11fc5078d`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Availability of recall under cold faults. -2. |
| Ownership and reuse | 19 | Reuses contract tests and replay fixture; config key unset preserves behaviour. -1. |
| Dependencies and implementable slices | 19 | Hard need on memory-004 removed (fixtures exist; decision not a prerequisite). -1: coordinator must update work-map. |
| Observable acceptance and baseline evidence | 18 | Three checks incl. partial shape and fault injection. -2: fault-injection seam for cold reads unprobed. |
| Failure, recovery and compatibility | 18 | No-fault byte identity; read-only. -2: adding `partial` field is a response-shape change for strict decoders. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: Absorbed partial cold status from memory-004; dropped hard need on memory-004; paths corrected.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Write the three-layout test first.

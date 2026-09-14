# the-track-record-is-reachable-across-stores — review

Canonical PRD: [@memory/the-track-record-is-reachable-across-stores](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-track-record-is-reachable-across-stores](../../../root/reviews/round-1/the-track-record-is-reachable-across-stores.md): reviewer 85/100; Revise. Fits current cross-project recall; add explicit scope authorization, same-ID/different-store, unavailable-store and bounded federation acceptance with current hub APIs.
  Original SHA-256: `5e78b8616a1702df24ef267562d2a143d317a3e09d10e219d475143972c7e5a2`.

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
Reconciliation verdict: **REBASE — cross-project recall exists via the machine hub (`memory query --all`, `search` in `src/hub/src/lib.rs`, `SearchReq` in `src/transport/src/hub_rpc.rs`, `skipped` partial misses). Missing: caller allowlist, contributor bound, store-qualified IDs. Cross-machine federation is void (memory decision `the-federation-tier-is-void-not-closed`). Cartridge config sets `hub.auto_start = false` (`src/cartridge.rs`), so this is a CLI/hub outcome. Old starting files wrong.**

Presented revision: `prd.md` SHA-256 `207c4e4098cfce14078f02a79c8fcf2097c0cde2d619260e12cbbb729642e7bf`. Rebased in this round (prior text `ea8bdfef3bfe3d08683f27728df335b0fd97645c9b2adcf079aaeb8a605a6ea1`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Scoped, privacy-relevant fan-out control. -2: who needs a subset allowlist is not evidenced. |
| Ownership and reuse | 19 | Extends existing SearchReq/hub; no replication. -1. |
| Dependencies and implementable slices | 19 | No needs; one test file to start. -1. |
| Observable acceptance and baseline evidence | 18 | Qualified IDs, never-asked roots, skipped within deadline. -2: 'per-root call record' may need a test seam. |
| Failure, recovery and compatibility | 18 | `--all` unchanged; no writes. -2: `root:id` qualification changes hit shape for existing consumers. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: Recorded delivered fan-out; narrowed to allowlist, bound and qualified IDs.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Extend hub_search_test with two roots.

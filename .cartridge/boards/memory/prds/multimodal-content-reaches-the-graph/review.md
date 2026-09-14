# multimodal-content-reaches-the-graph — review

Canonical PRD: [@memory/multimodal-content-reaches-the-graph](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [multimodal-content-reaches-the-graph](../../../root/reviews/round-1/multimodal-content-reaches-the-graph.md): reviewer 77/100; Revise. Keep engine media ingestion scope; specify supported media, fixture provenance, embedding/index compatibility and explicit unsupported cases before selecting implementation.
  Original SHA-256: `e50fc2f8a605f816a9f7927574a2977b2f54070885044b1b9c1bcc9a4dbc42d7`.

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
Reconciliation verdict: **REBASE — media ingest absent (`IngestArgs`, `Source` text-only); embedding identity is a store-wide `EmbedStamp` that deliberately fails open at save (`src/graph/src/persist.rs`, `check_embed_stamp`). Old starting files wrong. Model access stays memory's (memory decision `memory-alone-owns-model-access`).**

Presented revision: `prd.md` SHA-256 `0d4a5236375a405b8867bf26fd5884490bf6ba7563f4a6c721f385669588f004`. Rebased in this round (prior text `bd9d4fbf816b7e482e549bd862da88ed236ca67a28074768c5a9ba1a2ae6189e`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Requested capability, bounded to one format. -3: no current consumer measurement. |
| Ownership and reuse | 19 | Configured reason endpoint, existing stamp, no second store. -1. |
| Dependencies and implementable slices | 17 | Size L with provider-capability probe and stop/split condition. -3. |
| Observable acceptance and baseline evidence | 19 | Four checks incl. refusals and offline stubs. -1. |
| Failure, recovery and compatibility | 18 | Text ingest and save fail-open preserved; private-image approval noted. -2: mismatch refusal scoped to media only leaves text mismatch as today. |
| Reviewer total | 90/100 | |

Agent score: **90/100 — PASS**.
Findings: (1) Paths corrected. (2) Reconciled acceptance with the deliberate fail-open stamp: refusal at media admission only. (3) Provider capability made a first probe with split rule. Body ~317 words.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Probe llm.rs image support; split if absent.

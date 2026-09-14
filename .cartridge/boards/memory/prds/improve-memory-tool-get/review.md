# Retrieve a recalled fact by stable ID — review

Canonical PRD: [@memory/improve-memory-tool-get](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memory-tool-get](../../../root/reviews/round-1/improve-memory-tool-get.md): reviewer 86/100; Rehome. Move exact-ID readback into the memory-owned adapter/query contract; reconcile with the Landscape readback prerequisite before wrapper retirement.
  Original SHA-256: `132d171166497d0c1314f52236b5f359d2d3e3463fbb2e13384d7dd3a6569a12`.

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
Reconciliation verdict: **REBASE — 'use it for Landscape memory references' is obsolete: landscape.ctg is gone (root `bc2c190`), and the fabric graph now lives in memo (`memo.ctg/src/fabric_graph.rs`, cartridge.ctg `939e7d1` removed the core copies). Memory needs no fabric-specific consumer, because any consumer reads by ID through the tool. The service `get` already exists and is tested (`operation` in `src/cartridge.rs`, `query_by_id`, `.cartridge/tests/integration/cartridge.rs` get cases); only the agent tool lacks it. `tool_describe` declares `reads: ["query"]`, per decision `a-cartridge-brings-its-own-surface`.**

Presented revision: `prd.md` SHA-256 `44b22de4c9a69fa224d537d46c2115cf5447cb6ef674c01f646bf470f114d7e8`. Rebased in this round (prior text `781dba16597fb2734f291c0df0e68bc9f47dbb6dbdf341f5db6e29b85d12781e`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Exact readback for agents; narrowed to the missing tool surface. -1. |
| Ownership and reuse | 20 | Reuses the tested service get and owner read validation; descriptor `reads` updated per decision. |
| Dependencies and implementable slices | 19 | Single file, first of three tool leaves. -1: adapter-core need is open on paper though apparently delivered. |
| Observable acceptance and baseline evidence | 18 | Four checks with concrete limits (k 1..20, 65536). -2: consumer relay through mcp.ctg not in the proof. |
| Failure, recovery and compatibility | 17 | Read-only; attached-owner disconnect explicit. -3: rejecting undeclared `sync` on query/get may break a caller sending it today; probe should grep consumers. |
| Reviewer total | 93/100 | |

Agent score: **93/100 — PASS**.
Findings: (1) Landscape reference removed. (2) Recorded that service get is delivered; scope narrowed to tool exposure and strict input validation. (3) Undeclared `sync` read in `tool_call` recorded as a defect. (4) Owner key typo fixed. Body ~306 words.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Implement first among tool leaves after coordinator confirms adapter-core.

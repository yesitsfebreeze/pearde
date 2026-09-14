# Context regressions fail an explicit comparison gate — review

Canonical PRD: [@landscape/context-quality-is-measured/context-comparison-gate](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [context-quality-is-measured](../../../../root/reviews/round-1/context-quality-is-measured.md): reviewer 86/100; Resequence. Capture the corpus and old-path baselines before the replacement selector lands; define measurable regression tolerances and fixture sizes.
  Original SHA-256: `d4357ac7cf0b610600f4e48d5a080cfa891ac4845efd645d36f379b0a6a928e9`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **REBASE**. Aligned with the parent's round-3 REBASE.
- The old/new comparison of the landscape selector (`landscape.ctg`, `just test landscape`) no longer exists. The candidate and the baseline are both memo revisions, compared on the frozen corpus.
- The need `@landscape/landscape-composes-system-context` is dropped. It is a roll-up that stays open until the live providers exist, and every corpus scenario (documents, memory, files, kernel, mixed, budget) uses contributors that already exist (`memo.ctg/src/context.rs`, `context.memory`, `context.file`). It was context, not a hard prerequisite.
- Revision: one named comparison command with both revisions, five alternating paired runs, per-ability recall and median latency (the round-1 tolerance of 20% is a finding), independent bound and truncation checks, the parent's named failure for a missing baseline, and a test file covering the broken-ranker and missing-baseline cases.

Stale presented revision: `ce77208ac6ff3b65f35f2b1d3da85875abe9f13c3c2c3b57146e29143ac691fe`. Revised revision: `prd.md` SHA-256 `412c8b828c655393918e7fc4e9a3be76217a6fd55eb0c4fd2b0f7e3a30e64930`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | An explicit regression gate for context quality is bounded to one command. -1: latency is advisory only. |
| Ownership and reuse | 19 | memo-owned; reuses the baseline runner and raw format. -1: the board alias is landscape. |
| Dependencies and implementable slices | 18 | One hard need, which resolves; the dropped roll-up need has a stated reason. -2: blocked until the baseline leaf lands. |
| Observable acceptance and baseline evidence | 18 | Exit status, broken-ranker fixture, named failures, both revisions reported. -2: `compare.ts` and `compare.test.ts` are to be created. |
| Failure, recovery and compatibility | 18 | Refuses an existing output directory, keeps earlier reports, requires one host and toolchain for latency. -2: no rule for a corpus revision bump (it would need a new baseline). |
| Reviewer total | 92 / 100 | |

Result: **PASS**. Word count 260 body / 290 with frontmatter.
Findings: the coordinator should acknowledge the dropped cross-roll-up need.
Unresolved blocking findings: none.
Validation (read-only): `ls`/`rg` existence checks on memo.ctg `83bf1ad` (main = ws branch `transport`: `src/context.rs`, `evidence/`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/{host.ts,context.test.ts}`), fs.ctg ws `03f360e` manifest, sessions.ctg `118b784`, ws/pty.ctg `c003065`, ws/router.ctg `ab184a1` (`src/context.rs`, `src/proxy.rs` `explain_routes`), ws/cartridge.ctg `ba198f4` `docs/transport.txt` and coordination `PORTING.md` (`--dir <dir> run <event>`); reads of the analysis files in context-baseline-corpus; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md`, footprint paths on main or ws, and every relative link; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: wait for `context-baseline-corpus`, then implement. Coordinator: rehome to memo with the parent.

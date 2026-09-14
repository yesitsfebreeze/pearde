# Tool probes run and locate a failing provider — review

Canonical PRD: [tool-probes-run-and-locate-a-failing-provider](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [tool-probes-run-and-locate-a-failing-provider](../../reviews/round-1/tool-probes-run-and-locate-a-failing-provider.md): reviewer 84/100; Merge. Use the current exposed capability census instead of the historical two-tool assumption; merge real-provider probe execution into the owner-document release gate.
  Original SHA-256: `0f63fdfb10dda11fc2aef9e7a8a0dff3fd2cd711a9291a6a32775a11c51b05fc`.

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

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `859e398e83b5f7fea65131a57f6d47772d19d29a889ae42c19e7f791257cea0f`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: failure attribution and isolation already exist in source (`run_contracts` failure lines `<id> <obligation> `<key>` returned false`, `verify_one` needs-closure, `stalled` report in cartridge.ctg/src/host/run.rs), but only a passing contract is tested. Rebased from a probe-runner build to regression fixtures for those paths; dropped the need on every-enabled-tool-ships-a-contract-probe (not a hard prerequisite, shared footprint noted instead). Pre-revision SHA-256 `826a595a08b138461317392291f7637dcfb10d60c3c2dd44b78e591334f6548f`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 17 | -3: the behavior is largely delivered; remaining value is proof against regression. |
| Ownership and reuse | 17 | Reuses host.rs helpers and tempdirs. -3: host-owned work in the root board; rehome to runtime recommended. |
| Dependencies and slices | 19 | No hard needs; sequencing with the contract-coverage item stated. -1. |
| Acceptance and baseline | 19 | Three concrete fixtures with expected output and gates `just test cartridge`, `just check cartridge`. -1: unsettled-profile path explicitly excluded. |
| Failure and compatibility | 18 | Fix code not expectations; tempdir isolation keeps user stores out; exclusion reason (`settings::host()` is process-wide) recorded. -2. |

Agent score: **90/100 — PASS**.
Findings: Largely delivered in source; the item now owns the missing failure-path tests only. If the coordinator prefers, it can be closed as delivered once those fixtures exist.
Unresolved blocking findings: none.
Disposition: keep (narrowed); rehome to `@runtime` recommended.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: add the three fixtures; land after or before the coverage item, not concurrently.

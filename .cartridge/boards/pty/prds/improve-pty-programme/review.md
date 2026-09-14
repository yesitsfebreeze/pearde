# PTY and shared shell improvement plan — review

Canonical PRD: [@pty/improve-pty-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-pty-programme](../../../root/reviews/round-1/improve-pty-programme.md): reviewer 89/100; Revise. Settle preemption and command-busy behavior once; shell metadata and output retrieval can proceed independently.
  Original SHA-256: `07745ae2fdd04118801e98eeec0715bee3f164884b9da4ff0e6dd57069bb509c`.

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

Reconciliation verdict: **CURRENT**. Evidence: roll-up names no architecture-bound paths; `@pty/improve-pty-shell-identity` done (pty e8e6b31); input ownership and command wait open (both rebased round 3); pty on transport (0a21768).
Revision reviewed: `prd.md` SHA-256 `7a732f8b419724cb759c1c6a6a6a273572038280ee9dd1db0efd86eabc58224d` (prd.ctg 077e57a2, pre-revision).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | -3 round-1 finding "settle preemption and busy once" not reflected; `@pty/pty-document` overlapped both leaves. |
| Ownership and reuse | 19 | -1 no statement which leaf owns busy/ids. |
| Dependencies and implementable slices | 19 | Needs resolve; -1 shared footprint of the two open leaves not coordinated. |
| Observable acceptance and baseline evidence | 15 | No integration gate; release-status lists two pty failures. |
| Failure, recovery and compatibility | 15 | No exhaustion or integration-failure rule. |
| Reviewer total | 85 / 100 | |

Result: **FAIL**.
Findings: Preemption/busy ownership unsettled; shared footprint unordered; no gate or failure rule.
Unresolved blocking findings: none (below threshold only).
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **CURRENT** (unchanged from round 3).
Revision reviewed: `prd.md` SHA-256 `c3e78fd06d6b9f26615bded1d58b58e5a852fb6aa43ec0869c403245f5b35a8b` (working tree, uncommitted). Change: busy/preemption assigned to input ownership, ids/waits to command wait, pty-document relation stated; sequential landing for the shared files; `just test pty` gate; exhaustion rule.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | -1 limitations list open-ended. |
| Ownership and reuse | 19 | Single owner per behaviour; -1 none. |
| Dependencies and implementable slices | 19 | Landing order stated; -1 order of the two leaves not chosen. |
| Observable acceptance and baseline evidence | 18 | Gate with cwd; -2 closing with named failures allowed. |
| Failure, recovery and compatibility | 18 | Exhaustion rule; -2 no rollback note. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 4 / 1.
Next action: implement open leaves; this parent closes only on its integration acceptance.

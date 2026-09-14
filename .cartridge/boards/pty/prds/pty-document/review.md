# A shell document uses the owned persistent terminal — review

Canonical PRD: [@pty/pty-document](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [capabilities-live-with-their-owners](../../../root/reviews/round-1/capabilities-live-with-their-owners.md): reviewer 84/100; Split. Create independently claimable owner migrations; connect shell work to PTY input ownership and preserve direct-FS parity before retirement.
  Original SHA-256: `990147ebe7129477ba49047e365acf0292465529cb96a5c5c1d6b91b6ddc58e6`.

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

Reconciliation verdict: **REBASE**. Evidence: decision `the-tool-contract-is-a-memo.md` keeps document execution wanted; the runner is not built (`@runtime/one-runner-executes-documents` open); decision `a-cartridge-brings-its-own-surface.md` limits pty to a declared need; decision `the-agent-surface-preserves-the-visible-shell.md` keeps one visible `shell` interface; pty ported to transport (0a21768); `pty.ctg/src/tool.rs` already refuses at non-prompt phase and cancels only the matching context. Pre-revision text (SHA-256 `287948baaaa04578699f9f43322ca3174999288f682e041949fb4884986eee2d`) duplicated busy/ID/cancel scope owned by the two pty leaves, depended on the whole clients rollup (including agent and proxy leaves it does not need) instead of the contract leaf, lacked the command-id prerequisite, and had broken links. Blocking.

Revision reviewed: `prd.md` SHA-256 `a87ddf68c85dbfea6188eada67d2db03dd1abb502143e8ecac8edc3c2ed15a44` (working tree). Changes: narrowed to adapting the contract's one-shot invocation to `tool.shell`; needs are the contract leaf, input ownership and command wait; footprint on real files including `.cartridge/help.md`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Thin, non-duplicating adapter; -2 value only exists once the runner lands. |
| Ownership and reuse | 19 | Reuses pty leaves and `tool.shell`, respects surface decision; -1 help.md change not in acceptance. |
| Dependencies and implementable slices | 18 | Three hard needs resolve, acyclic; -2 contract leaf is stale and its shape unfrozen. |
| Observable acceptance and baseline evidence | 18 | Three observable checks; -2 fixture depends on contract fixtures that do not exist yet. |
| Failure, recovery and compatibility | 18 | Denial writes nothing, uncertain completion, direct calls unchanged; -2 retry/replay rule inherited from contract, not restated. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of repo, source, test and doc paths (ls/rg); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke` and `.cartridge/memos/routine/cartridge-development.md` accepts the named owners; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: blocked on three needs.

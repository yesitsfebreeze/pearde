# semantic-tool-recovery-retires-failed-generations — review

Canonical PRD: [@runtime/semantic-tool-recovery-retires-failed-generations](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [semantic-tool-recovery-retires-failed-generations](../../../root/reviews/round-1/semantic-tool-recovery-retires-failed-generations.md): reviewer 42/100; Rehome. Editor/LSP service recovery is host tooling, excluded from memory; retain generation-safe teardown and positive-control checks with an explicit current owner.
  Original SHA-256: `4a7154ea8de52d393f063e81102a4a8396a3607b7acd38a391407c991378efe7`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 12 | No maintained editor/LSP provider and teardown API has been identified in the current runtime/tooling owners. |
| Dependencies and slices | 14 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **80/100 — FAIL**.
Finding: No maintained editor/LSP provider and teardown API has been identified in the current runtime/tooling owners.
Blocking review findings: No maintained editor/LSP provider and teardown API has been identified in the current runtime/tooling owners.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: resolve the named prerequisite and review a substantive revision.

## Round 3 — 2026-09-14 (reconciliation, no score)

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `605a3ce27bcef1d27558e6f8ac7e8fe70e69b1f7519db2d86f396d469df27c88` (frontmatter review fields only; body unchanged).

Reconciliation verdict: **CONFLICT**. The round-2 blocker persists: no editor/LSP provider exists in any cartridge (`rg -il "lsp|language server|rust-analyzer"` across all `*.ctg` outside prd.ctg returns nothing). Assigning provider-specific lifecycle to the runtime would contradict decisions `tui-and-tools-are-cartridges` / `core-composes-and-the-cli-selects-services` (behavior belongs to cartridges) and `a-cartridge-brings-its-own-surface` (no sibling knowledge in shared cartridges). The generic host part already exists: node generations in `src/host/process.rs` `start(…, generation)` and `a_restart_keeps_its_dependents_working`.
Alternatives for the user:
- (a) Retire this item. No semantic tool is planned, and generation-safe restart is covered by the host.
- (b) Create an `lsp` (or editor) cartridge with its own board. This PRD is rehomed there, with provider and teardown API chosen as its first probe.
- (c) Keep the item parked here until a provider is named.

Recommended default: (a).
Validation: `rg` across the repository, reading of `src/host/process.rs`, decision memos. No product gates were run.
Rounds used / remaining: 3 / 2.

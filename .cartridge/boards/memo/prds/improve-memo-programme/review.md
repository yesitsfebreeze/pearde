# Memo improvement plan — review

Canonical PRD: [@memo/improve-memo-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memo-programme](../../../root/reviews/round-1/improve-memo-programme.md): reviewer 88/100; Reconcile. Place compact context and freshness responsibilities under the agreed Landscape/library facade split while retaining memo record APIs.
  Original SHA-256: `225ab7d8e91b247979c99f47185eb1eec9b73594814bd8858d2572e0df1ea1dd`.

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

## Round 3 — 2026-09-14 (reconciliation)

Reconciliation verdict: **DELIVERED**.

Reviewed revision: prd.md SHA-256 `64e8e040c5c2cc720e0f5b702eea3df75c37071d33dfa4b56a085cf0ebf44187` (frontmatter afterwards set to review-round 3 / delivered-pending-verification; body unchanged). Source revisions: memo.ctg 9a1cf99 (post transport port 1d2fa92), cartridge.ctg c9ef10b, prd.ctg 077e57a2 (dirty tree).

Evidence: all three linked leaves are `state: done` with recorded commits — `@landscape/improve-memo-compact-landscape` (cartridge.ctg 422c521, review passed), `@memo/improve-memo-stale-evidence` and `@memo/improve-memo-types-drilldown` (memo.ctg a458148, review accepted). Their behaviors survive the transport port in the current memo tool contract (`memo.ctg/src/service.rs` line 112): `index` returns compact kind metadata before reading one declaration path (types drilldown); `resolve` items carry kind and status "so a done or superseded item is not read as current" (stale evidence); `fabric` returns 5 entries by default with limit 1–20 and cursor paging (bounded discovery, formerly the landscape op, renamed per `.cartridge/memos/decision/the-fabric-lives-in-core.md`).
Remaining for closure (not a plan defect): acceptance 2 wants an integrated-revision record; run `just test memo` and `just check memo` from /Users/feb/dev/cartridge at memo.ctg 9a1cf99 and record the result before marking done.
Findings: (1) child link `../../../landscape/prds/improve-memo-compact-landscape/prd.md` still resolves but the landscape board must be rehomed to fabric (coordinator); (2) frontmatter key `capability-capability-owner` is a migration typo present in 68 PRD files board-wide (coordinator, not edited here).
No score recorded (delivered verdict). Validation: ls/grep of child frontmatter, rg of memo source; no product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required. User feedback: none supplied.
Result: DELIVERED — pending verification gate. Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: coordinator runs the memo gates and marks the roll-up done.

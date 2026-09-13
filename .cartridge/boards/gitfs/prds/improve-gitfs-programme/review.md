# GitFS and ship improvement plan — review

Canonical PRD: [@gitfs/improve-gitfs-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-gitfs-programme](../../../root/reviews/round-1/improve-gitfs-programme.md): reviewer 90/100; Keep. Good coverage of disk/overlay mismatch and irreversible shipping; split the ship leaf before claiming it.
  Original SHA-256: `529f6f79ab199915ae6b9aa38eb94a0b03349ce6cde2afb11d3213e7ed3b0219`.

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

## Round 3 — independent /root/proxy_continuation review — PASS 97/100

Dimensions: scope19, ownership20, dependencies20, acceptance20, failure18. Exact three direct and seven transitive contracts, nineteen-path GitFS union, current completion/reviews and pinned real composition proof validated against clean b4b95bb. Public/native/composition candidate gate passed. No product changes or new grant. No blocking findings.

Corrected receipt wording: snapshot-selection remains collected at55cc8aae27575ded5950737c46a99aa358b95980 with unchanged source footprint valid at current b4b95bb. It was not recollected at b4. Corrected inherited capability-owner metadata typo. These are factual/metadata corrections, no acceptance or proof scope changed. Remaining limits include explicit unknown remote outcomes/no replay/no rollback and default ask policy. Three rounds used.

# every-mutation-holds-the-store-writer-boundary — review

Canonical PRD: [@memory/every-mutation-holds-the-store-writer-boundary](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [every-mutation-holds-the-store-writer-boundary](../../../root/reviews/round-1/every-mutation-holds-the-store-writer-boundary.md): reviewer 88/100; Revise. Critical in-scope invariant; enumerate current mutation entry points and add concurrent writer/crash tests with exact runnable gates before claiming universal coverage.
  Original SHA-256: `c0f6a9798f18b1ded938d5452f7a3fb160175afbad1f3e3ca9aeb63006ffbd15`.

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

## Round 3 — independent /root/proxy_continuation review — PASS 96/100

Dimensions: value/scope19, ownership/reuse20, dependencies/slices19, acceptance/baseline19, failure/compatibility19. Reviewed retained failing baseline and concrete spec against actual with_graph, guarded flush, link, clean, register, hub, queue, lock, daemon and native paths at09bfaaef. Existing lock inode is authoritative; explicit stale refusal removes resurrection without new merge semantics. Deterministic dual-store claims and preserved cleanup inode close concrete gaps. No blocking plan findings.

Implementation checks: unnamed-promote's ID-resolution load belongs inside the shared claim; defer success printing until persistence succeeds; dual-store tests distinguish a first legitimately acquired claim label from an actual held-lock loser. These clarify existing acceptance without changing it. Three rounds used; no user rating invented.

## Round 4 — independent /root/proxy_continuation review — PASS 96/100

Dimensions: value/scope19, ownership/reuse20, dependencies/slices19, acceptance/baseline19, failure/compatibility19. Reviewed the source-bound amendment after the unchanged lifecycle canary exposed live CLI ingestion compatibility and the mutation census found unclaimed compression. The private operator RPC preserves existing provenance through the daemon owner; source/destination compression claims and immediate persistence-error returns complete the same invariant. No blocking plan findings.

Implementation checks: reject nested unknown Source fields; preserve shutdown admission and asynchronous worker crossing semantics; refuse explicit endpoint overrides while an owner is live or compare against its actual configuration. These enforce the reviewed strictness and compatibility contract. Four rounds used; no acceptance weakened or user score invented.

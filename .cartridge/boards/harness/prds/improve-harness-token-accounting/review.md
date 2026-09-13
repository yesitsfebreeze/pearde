# Show token estimates alongside serialized bytes — review

Canonical PRD: [@harness/improve-harness-token-accounting](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-harness-token-accounting](../../../root/reviews/round-1/improve-harness-token-accounting.md): reviewer 88/100; Resequence. Tokenizer accounting can represent unknown capability today; avoid making all accounting wait for the capability-routing feature.
  Original SHA-256: `b9709afdd46b083df01ae430ae58cfeb5ddb13811019c1ece8711f3ff279329d`.

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

## Round 3 — 2026-09-13

Reviewer: Codex `/root`, self-review under session delegation policy.
Inputs: [review-round-3-inputs.json](review-round-3-inputs.json).
Baseline a282c877 passes the harness gate. The real-process inspector regression
fails at “inspection must label a token estimate”; only byte accounting exists.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Adds requested inspection without coupling to capability routing. |
| Ownership and reuse | 20 | Existing serialized Wire and journal metrics; no tokenizer dependency. |
| Dependencies and slices | 19 | Local accounting module and inspector only. |
| Acceptance and baseline | 19 | Multilingual/schema/exchange fixtures and real no-model inspection. |
| Failure and compatibility | 19 | High uncertainty is explicit, bytes enforce limits, usage remains historical. |

**96/100 — PASS**, no blocking findings, 3/5 rounds used. This heuristic is not
an exact tokenizer or a promised upper bound; resolved provider framing remains
unknown until a later request is actually assembled and measured.

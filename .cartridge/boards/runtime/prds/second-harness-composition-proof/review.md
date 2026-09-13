# Second harness composition proof — review

Canonical plan: [second-harness-composition-proof](prd.md).
Reviewer: side-conversation assistant, self-review; sub-agents are unavailable in
this conversation. This new integration experiment has no previously used rounds.
Related composition implementation plans remain separate and retain their history.

## Round 1 — 2026-09-13

User request: create a work item to verify harness composition, create repair work
when it fails, and give the base cartridge particular attention.

Inputs: original plan and contract digests in [review-inputs-round-1.json](review-inputs-round-1.json), with [original plan bytes](prd-round-1.md) retained.
No implementation specs or experimental results exist yet.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 20 | One measurable composition experiment, with explicit baseline and custom harness behavior. |
| Ownership and reuse | 19 | Runtime coordinates; repair work stays with capability owners. Fixture file boundaries must be narrowed during analysis. |
| Dependencies and slices | 19 | Probe can start now; existing composition work is context rather than a barrier that hides current failures. Discovered repair dependencies require evidence. |
| Acceptance and baseline | 18 | Clean checkout, zero upstream implementation edits, real service calls, default-harness parity and three repetitions. Setup time is measured; no unsupported usability or latency target is invented. |
| Failure and compatibility | 18 | Explicit lifecycle, authority, data and isolation checks; concrete interleavings and deadlines must be fixed in the implementation specs. |

Agent score: **94/100 — PASS** for the verification plan. Blocking plan findings:
none. Product behavior remains unverified.

Validation: local links, referenced starting files, five unchecked acceptance
criteria, 344-word body and review digests checked. No product gates were run.

Rounds used: 1/5; remaining: 4. User rating: not required under the recorded
delegation. Future repairs inherit consumed rounds when they refine this scope;
reuse existing repair identities and their histories rather than resetting them.

Next: select this open work item for the disposable experiment. Keep it open when
any required case fails, link each repair, and rerun the complete matrix before
claiming the composition promise is verified.

## Round 2 — 2026-09-13

The user selected concise writing as the concrete composition experiment.
Replace the generic evidence-review harness with one separately defined
[writer cartridge](../../../harness/prds/concise-writer-cartridge/prd.md).
Its real-model evaluation must demonstrate shorter output with retained meaning;
the existing service and base-lifecycle matrix still applies. Baseline probing
can start independently; completing the trial needs the writer contract.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 20 | The experiment now demonstrates the requested writing behavior. |
| Ownership and reuse | 19 | Runtime owns integration; harness owns the isolated writer slice. |
| Dependencies and slices | 19 | One explicit writer prerequisite; existing repair identities remain reusable. |
| Acceptance and baseline | 18 | Real-model writing quality is separate from deterministic service wiring; fixture details still require implementation. |
| Failure and compatibility | 18 | Base parity, isolation, cancellation, reload and repair/retest requirements remain intact. |

**94/100 — PASS** for the revised plan. No blocking plan findings.
Current inputs: [review-inputs.json](review-inputs.json). Round 1 remains archived
above. Local links, dependency direction, word limits and content digests checked;
no product tests run. Rounds used: 2/5; remaining: 3.

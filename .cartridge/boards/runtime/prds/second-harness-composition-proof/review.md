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

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `2c8c85f4892154f453e05cf9b797d91611ae7eb748eed409ec6884a0fee64d8f`.

Reconciliation verdict: **REBASE**. Starting files are gone:
- `cartridge.ctg/src/sdk.rs`: the transport crate is now `cartridge.ctg/src/transport` (`813521f`).
- `cartridge.ctg/.cartridge/default/init.lua`: cartridge.ctg is the base, not a composition (`b1494bb`), and the composition is the root `.cartridge/init.lua`/`config.lua`, currently untracked.
- `harness.ctg/README.md`: harness now documents itself in `.cartridge/help.md` (decision `a-cartridge-brings-its-own-surface`).
- The `src/tests/fixtures` link is superseded by `cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs`.

The known red baseline is in `.cartridge/memos/note/release-status.md`. Revision: current files; failure vocabulary aligned with the event host (undeclared needs, grants, deadlines); step one commits/pins the profile and records the baseline; body trimmed from 344 to 306 words. The `@harness/concise-writer-cartridge` need resolves (claimed, review passed, round 5).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The user-requested composition experiment is unchanged; −1: 306 words, slightly above the 300 target. |
| Ownership and reuse | 19 | Runtime integrates and repairs go to owners; −1: gitfs/pty/router/sessions repairs may queue behind current test failures. |
| Dependencies and slices | 18 | One hard need resolves; −2: the uncommitted root profile is a precondition outside this item. |
| Acceptance and baseline | 17 | Five checks with a matrix and repetitions; −3: the baseline is already red in several owners, so "every required case passes" needs those repairs first. |
| Failure and compatibility | 18 | Attributable outcomes, no replay or orphans, fixture-only teardown; −2: deadline values are still undeclared. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Blocking findings: none.
Validation: `ls` of the named files (harness `.cartridge/help.md`, `docs/creating-cartridges.txt`, root `init.lua` untracked per `git status`), `just --list` (`smoke` present), the `harness` owner case in `cartridge-development.md`, needs resolution. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: commit the root profile, then run the baseline probe.

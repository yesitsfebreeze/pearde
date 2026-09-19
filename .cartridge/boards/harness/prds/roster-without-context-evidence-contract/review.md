# Inherited review history

This slice inherits [rounds 1 and 2](../../../runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted/review.md) from the [approved deletion decomposition](../../../runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted/split-plan.md). Round 1: independent reviewer /root/context_split_reviewer, FAIL 66/100. Round 2: independent reviewer /root/context_split_reviewer2, PASS 94/100. Two of five rounds used; three remain. No executable specification has yet been reviewed for this leaf. Splitting does not reset the allowance.


# Round 3 — PASS 94/100

Canonical plan: `@harness/roster-without-context-evidence-contract`.
Independent reviewer: `/root/roster_reviewer`, 2026-09-19.
Two inherited decomposition rounds (FAIL 66, PASS 94); this is the first executable-plan review and third total round. Three used, two remain. User rating is not required under delegated review. This is a plan approval, not implementation or acceptance proof.

| Dimension | Score /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Removes the generic discovery collector while preserving the authenticated roster. One accountable owner and observable outcome. Fixture modernization is necessary proof work for the same outcome. |
| Ownership and reuse | 19 | Existing Config, response validator and Snapshot are retained; capture/render responsibilities are specific to roster. No generic provider scheduler, reference reader or renamed Contribution/Prepared facade survives. Two added module paths are already in the canonical footprint. |
| Dependencies and implementable slices | 18 | Delivered roster receipt is explicitly historical. Current Harness and actual Sessions source are pinned; real-base module fixtures are feasible using the current exports. Dirty overlapping owner changes are acknowledged as a reconciliation gate. Integration fixture preparation is the principal remaining implementation risk. |
| Observable acceptance and baseline evidence | 19 | Seven named roster units, all five restored integration behaviors, four process tests, working-memory test and complete owner checks. Named tests are parsed by the actual engine; all blocks select the current cwd owner with isolated targets. New test bodies remain subject to independent diff review. |
| Failure, recovery and compatibility | 19 | One call/deadline, dropped pending future, disabled/mismatch zero-call behavior, privacy and digest validation, partial/unknown/tiny-cap outcomes, final-selection revisions and transcript preservation are explicit. Source provenance and local snapshot identity are not conflated. |
| Total | **94/100** | **PASS; no unresolved blocking plan findings.** |

## Source and boundary review

I read the current `src/roster.rs`, generic `src/evidence.rs`, all three roster units and all five legacy integration bodies, the current Request capture site and frame append site, actual Sessions roster implementation, both module manifests/init scripts, committed integration support and committed process/working test names. Harness HEAD is `c8305341bb30b058c481bf023ebf977304248dab`; Sessions HEAD/source pin is `499191501e7e3cbb1ac1537ea75a5f1906f97f21`. The prerequisite PRD records integration commit `698a4dc9555a6b3ad8d46dcc5dd3a14463048e70` and is done. The approved split explicitly permits this owner slice and requires preservation of the same roster behavior.

The generic collector's only production caller is roster. Its reference ordering explains the specified id ordering. Existing rendering computes a revision before final row removal and has an unconditional metadata fallback that can exceed very small block caps; the plan explicitly fixes both while deleting the obsolete layer. It also preserves the validated source digest rather than claiming a globally atomic revision. Validation is before field allowlisting, so digest verification continues to cover the complete producer envelope while private extensions are excluded from rendered observations.

Actual source confirms default max_rows=200 against Sessions limit 1..100. Preserving configuration is explicit inherited scope; supporting explicit 20-row configuration is adequate for this removal task. That mismatch is a separate observed defect, not an undisclosed successful-default claim. Do not change defaults inside this leaf.

The old Bun integration transport requires process binaries although both owners currently build cdylibs. Rewriting it against the real base and actual archived Sessions module is necessary. The stock Harness module init and declared credential prefixes support the proposed composition. A Sessions adapter may count and intercept calls but must continue to delegate real store/authentication/projection operations. Existing tests' old numeric configuration assumptions may need explicit fixture settings (for example output headroom and automatic-refresh thresholds) when moved to stock manifest defaults; retaining their behavioral assertions matters more than retaining obsolete fixture boilerplate.

## Execution and recovery notes

- No substantive spec change is requested. Proceed with the approved design after satisfying its owner reconciliation prerequisite. The current live dirty changes in `src/lib.rs`, README and help are not approved by this review. Keep candidate work isolated and do not sweep those changes into collection.
- Make the new fixture's startup, build and shutdown timeouts concrete, including kill-and-wait cleanup for startup/preparation failures. The enclosing 120-second engine timeout is not a substitute for cleanup inside the fixture. Prewarming is allowed by the spec; success must still include the complete gate.
- Final composition hashing must follow final selection/status resolution, including timeout and metadata-cap failure. Reserve fixed digest space while fitting the rendered body and check the deadline after bounded CPU work. Unit assertions specified in this plan are sufficient to expose stale pre-render hashes.
- Preserve malformed-but-correctly-resealed response cases. Mutating identity without resealing only proves the digest check; the plan explicitly requires structural validation independently.
- These are implementation/verifier focus points already covered by the plan, not additional approval conditions or expanded scope.

## Validation performed

Cwd `/Users/feb/dev/cartridge` throughout. `./task prompt` exited 1 (`memo is not provided`); no daemon action was taken, and the inherited coordinator instructions governed this read-only review. Applied Rust router and anti-pattern review skills.

`CARGO_TARGET_DIR=/tmp/cartridge-roster-analyst-target cargo test --manifest-path harness.ctg/Cargo.toml --locked --lib roster::tests -- --nocapture` exited 0: all three current roster unit tests passed, zero failed. This exercises the current owner with foreign assessment changes, so it is baseline evidence only. I also inspected the analyst's separate process/working passes and obsolete-Bun failure without representing those as my own executions.

A Bun script imported actual `verificationBlocks` and `testBlock` from `prd.ctg/src/lifecycle.ts` and parsed canonical spec01: six executable blocks, including four test blocks requiring 7/5/4/1 passed names. Exit 0. Reviewed lifecycle parser and runner: named Cargo/JUnit results are supported, heading is recognized and the 120-second execution bound matches the template. All named pre-existing process/working tests exist at committed Harness HEAD. No source writes, board transitions, checkboxes or commits were made. All commands started by this reviewer are terminal.

## Revision binding

Hashes are SHA-256 of exact current files, before coordinator appends this round to the review history. The state/claim in the PRD remain analyzing/coordinator-codex-6 at review time.

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/harness/prds/roster-without-context-evidence-contract/prd.md` | `009e1a96fb4889db7c56502241b7c6df741fad77de975e4196cb7c886ccaa5f2` |
| `prd.ctg/.cartridge/boards/harness/prds/roster-without-context-evidence-contract/specs/spec01.md` | `a5eb64f405e311651e926a1d8afefcfd8c9de77cafb1f5f0e08a9f51e125d456` |
| `prd.ctg/.cartridge/boards/harness/prds/roster-without-context-evidence-contract/review.md` | `47af2a9b1dc48175c8f215592b4229decec112c841b97d3d5070ae7f2a74da68` |
| `prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/prd.md` | `84c1012b689a076f2a382ea8c5bafa2ddbaaf7b748a4d0c2a727af24d9facf2f` |
| `prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/specs/spec01.md` | `fb74dd1d9dc23b9f4654ee9c6a83692effaae6bf24788b73b86908bfd5100671` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted/split-plan.md` | `394235e55b7a9828b7a3c07605178b946511c7756ad13601b4bdd838e93e1597` |
| `prd.ctg/.cartridge/templates/spec.md` | `0350746f33dde5398bf620c7982e5fe3c8163ff2e0c4879436631393704020ad` |
| `harness.ctg/src/roster.rs` | `273e87072ace0a16a1ae0d58a16e6aefa73b00521897b66d0df0ec76c90cc2f6` |
| `harness.ctg/src/evidence.rs` | `8606caf9a4cff4bef137978a6194844d8c5e9a191513a8c673673b1ba84f2079` |
| `harness.ctg/.cartridge/tests/unit/roster_tests.rs` | `be4b5c0c58b2d58eb1f5e9320458d3ac74e9f4048417524519df16bfd5f61e75` |
| `harness.ctg/.cartridge/tests/integration/roster.test.ts` | `5f9420c7595487810ff5701631e5b1d6fa1a5d555619da2b53be4966959730fc` |

Committed dependency inputs are additionally bound by the Harness and Sessions commits above; Sessions artifact preparation must archive that exact commit, never consume the dirty live sibling. The actual external base executable hash is to be recorded by the implementer and independent verifier for each proof run, as specified.

Disposition: keep; executable revision passes. Next action: coordinator records this attributed, digest-bound round, reconciles the ownership prerequisite, and dispatches isolated implementation. Acceptance remains unticked until independent implementation verification and integrated proof.


## Coordinator disposition after round 3

The reviewer clarified the existing approval in [reviewer-codex-3-clarification.md](../../../.state/loop/roster-without-context-evidence-contract/reviewer-codex-3-clarification.md). This does not consume another round. Implement in a clean lane at Harness c8305341bb30b058c481bf023ebf977304248dab. The inspected foreign lib.rs changes concern assessment_context and assessment calls; README/help changes concern task commands and assessment behavior. They do not change roster integration. Preserve those live files untouched and exclude their changes from this candidate. Integration and collection remain pending while overlapping foreign changes remain. Any eventual combined revision needs fresh integrated verification; a substantive plan change still needs another available round.

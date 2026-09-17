# an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver review history

Plan: @router/an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver, prds/an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver/prd.md.
Scope: the compatibility-rule guard in the router proxy.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

## Round 1 — 2026-09-16

Presented revision: PRD revision 567fe04eb51c40f96ddeb0b5050022bd37fdedfc9757964028b66ff0cf9c535f, router dirty tree at effe3c5f57b634996a810c98bef756c90c630682 and later dirty edits.

| Input | Content digest |
| --- | --- |
| Plan | prd.md observed and ticked in this session |
| Specs | specs/spec01.md added in this round |
| Material contracts/dependencies | router.ctg/src/proxy.rs, router.ctg/src/health.rs, router.ctg/.cartridge/tests/unit/proxy/capabilities.rs |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | Unblocks the six remaining router cause PRDs; the inert-adaptation defect is recorded from live evidence in the PRD body. |
| Ownership and reuse | 20 | The guard, the rule kinds and the tests all live in the router proxy's own files; no new surface. |
| Dependencies and implementable slices | 19 | The slice is one guard rewrite plus two tests, verified runnable in an isolated target dir this session. Deduct 1 because the diff sits in a shared dirty tree with sibling router PRDs in the same files. |
| Observable acceptance and baseline evidence | 19 | Both named tests ran green under CARGO_TARGET_DIR isolation in this session; the source guard and DROPPABLE list were read directly. Deduct 1 because box 1's "reports which keys changed" is a unit-level shape rather than an end-to-end wire probe. |
| Failure, recovery and compatibility | 18 | Denied worlds are scripted in the spec: restoring the old guard fails the router-added clause; removing preserves fails the rename test; re-adding the exemption list fails the source check. Deduct 2 because no pre-implementation failing log from the original code is on record. |
| Reviewer total | 96 / 100 | PASS |

Findings and concrete revisions: no blocking findings.
Disposition: keep.
Validation: `cargo test --lib an_adaptation_applies_where_a_waiver_is_refused` and `cargo test --lib no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields`, cwd router.ctg, exit 0 both, CARGO_TARGET_DIR isolated; the guard and rule code read directly in this session.
Reviewer identity: coordinator cartridge-2e (self-review; the fresh worker attempt died to a harness-proxy timeout without producing a report).
User rating: not supplied.
User feedback/provenance: none this round.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: `prd specced @router/an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver`.

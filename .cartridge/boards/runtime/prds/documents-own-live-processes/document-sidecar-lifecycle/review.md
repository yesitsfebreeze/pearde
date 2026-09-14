# A sidecar belongs to one ready owner generation — review

Canonical PRD: [@runtime/documents-own-live-processes/document-sidecar-lifecycle](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [documents-own-live-processes](../../../../root/reviews/round-1/documents-own-live-processes.md): reviewer 85/100; Split. Separate sidecar lifetime from event activation; settle event acknowledgement/deduplication and handoff of exclusive listeners or writers before implementation.
  Original SHA-256: `75f4d40c468a29f7c36d7ca8c32ca4d4111e67422c49c65aa3986eb3b1101404`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **REBASE**. Aligned with the parent's round-3 REBASE.
- The old footprint (`src/runtime.rs`, `src/service.rs`, justdown sidecars) is gone. "Sidecars" are now helper programs from `cartridge.spawn` (ws/cartridge.ctg `transport-design` `ba198f4`, `src/node.rs`), each belonging to one node process and generation (`src/host/mod.rs` `stop_slot` increments `generation`).
- As the coordinator directed, the clause "replacement preserves the old usable service until a valid handoff" and the exclusive-handoff refusal are dropped; `@runtime/extension-loader-plugin-tree` owns refusal at planning and excludes overlapping handoff.
- Nested-child teardown is left to `@runtime/launch-authority` (acceptance 3).
- The need `@runtime/one-runner-executes-documents/document-command-result` is dropped. Helper lifetime does not depend on a document runner, and that leaf is CONFLICT in this pass.
- The remaining gap, from source: the reader task ends silently on helper exit, and `status` keeps the node `active`.

Stale presented revision: `ee2b82a410c82f62c7256788a7e12aaa2408739557b7ea47856f602e46276cd4`. Revised revision: `prd.md` SHA-256 `e93ff2bb99bd423ae56926f02595b6cdfa29a064f077cc29df86afe3bfc810b7`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | A silently dead helper behind an `active` TS cartridge (auth, live, tui, prd) is a real diagnosis gap; the scope is bounded to exit visibility and the generation boundary. -2: after the overlaps were removed, acceptance 3 is a negative guard rather than new behavior. |
| Ownership and reuse | 19 | The base owns `cartridge.spawn` and `status`; the leaf reuses the existing test helpers and status publishing. -1: the shape of the status field is left to specs. |
| Dependencies and implementable slices | 18 | No hard needs; overlaps are named with their owners. -2: `src/node.rs` is a shared footprint with launch-authority and needs coordinated landing. |
| Observable acceptance and baseline evidence | 18 | Three checks with a fixture helper, next to named existing tests; the gates exist. -2: the silent-exit baseline is unreproduced source reading. |
| Failure, recovery and compatibility | 18 | Additive status field, rollback named, no restart policy invented. -2: the retention bound of the stderr tail is unspecified. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Word count 279 with frontmatter (`wc -w`; leaf bound 150–300).
Findings: reproduce the silent exit before specs; land in coordination with `@runtime/launch-authority`.
Unresolved blocking findings: none.
Validation (read-only): source reading on ws/cartridge.ctg branch `transport-design` `ba198f4` (`src/node.rs` `spawn`/`Spawned`/reader task/`request`/`kill`, global `subscribe`; `src/transport/cartridge.rs` `join`/`leave`/`subscribe`, connection loop subscribe/unsubscribe/disconnect; `src/host/mod.rs` `stop_slot`/`replace_locked`); existence of the named tests in `.cartridge/tests/unit/src/tests/host.rs`; main cartridge.ctg `e8a4da3` carries the same files; needs resolution under `boards/<owner>/prds/<slug>/prd.md` (`@runtime/launch-authority`, `@runtime/extension-loader-plugin-tree`, `@runtime/a-listener-subscribes-to-event-types` exist, passed round 3); root `.cartridge/justfile` `test`/`check` and the `runtime` routing in `.cartridge/memos/routine/cartridge-development.md`; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: failing test for a helper that exits after one answer. The parent `documents-own-live-processes` can be re-reviewed.

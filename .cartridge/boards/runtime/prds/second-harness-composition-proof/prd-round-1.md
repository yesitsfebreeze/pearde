---
state: open
origin: requested
priority: 95
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
capability-owner: runtime
canonical-scope: second-harness-composition-proof
review-round: 1
review-status: passed
---

# A second harness works by composing existing cartridges

Verify that an author can build a distinct evidence-review harness by adding its
cartridge and composition profile. Reuse the shipped runtime, SDK and capability
cartridges unchanged. Here, **base** means that shipped foundation and its default
composition; both must remain reliable and easy to use. Owner: runtime.

## Acceptance

- [ ] From a clean disposable checkout, follow a short author guide to compose
  the new harness. A deterministic task proves different context selection and
  structured evidence output. Record elapsed setup time, commands and the diff;
  require zero edits to existing runtime, SDK or capability implementations.
- [ ] Exercise real memory, GitFS, PTY, policy, routing and session boundaries
  with a deterministic model endpoint. Discover capabilities, call them and read
  back effects; registration alone does not pass. A profile-only swap restores
  the default harness, which passes the same shared-capability checks.
- [ ] Test the base for missing/incompatible providers, denied access, malformed
  results, cancellation, restart and failed reload. Require attributable errors,
  preserved committed data, no uncertain-mutation replay, no duplicate writers,
  no orphan processes and no expanded grants. Declare deadlines before running.
- [ ] Capture revisions, fixtures, expected/observed outcomes and supported
  platforms in a compact pass/fail matrix. Run three clean repetitions; report
  startup/call timings and every manual workaround. Every required case must pass.
- [ ] For each failure, reuse a matching open PRD or create one small owner-local
  repair PRD with reproduction, expected behavior, acceptance and retest command.
  Prioritize base defects; link blockers here. Filing tickets does not satisfy
  this verification: close it only after repairs and a complete successful rerun.

## Proof and recovery

Start at [SDK](../../../../../../cartridge.ctg/src/sdk.rs), [runtime fixtures](../../../src/tests/fixtures),
[default composition](../../../../../../cartridge.ctg/.cartridge/default/init.lua) and
[harness contract](../../../../harness.ctg/README.md).
Add fixtures to existing test entry points; run `just test runtime`,
`just test harness` and `just smoke` from the composed root. These are proposed
gates. Use disposable stores/profiles; teardown only fixture-owned resources.

## Dependencies and review

No prerequisite blocks the initial probe. Consult [composition work](../cartridges-compose-recursively/prd.md)
and the [source map](../../../root/work-map.json) to reuse repairs.
Record discovered blockers before implementation. [Review](review.md): round 1/5.

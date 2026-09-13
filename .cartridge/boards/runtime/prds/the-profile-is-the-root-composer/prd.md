---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: the-profile-is-the-root-composer
footprint: ["src/loader.rs",".cartridge/tests/unit/src/tests/mod.rs",".cartridge/tests/unit/src/tests/composition.rs",".cartridge/docs/composition.md"]
commit: "bd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df"
---

# the-profile-is-the-root-composer

Audit current root/nested composition and remove only a demonstrated duplicate implementation. The target is equal semantics at different depths, not a grep-count quota. Preserve scoped keys, shared default providers, explicit isolation, transactional replacement and existing launch authority.

## Acceptance

- [x] One parameterized real fixture reaches, replaces and rejects a bad replacement at depth zero and nested depth with equivalent results.
- [x] A private child key remains private and a shared router/PTy provider is not duplicated by nesting.
- [x] The current default profile and foreground APIs retain behavior; any removed path has mapped callers and equivalent tests.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [a-nested-cartridge-is-a-first-class-entry](../../../../memos/work/root--a-nested-cartridge-is-a-first-class-entry.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-profile-is-the-root-composer`; maximum five rounds.

## Historical prerequisite resolution

The linked historical nested-entry memo is still active and has no canonical row in the root work map. Baseline at runtime8e514eac establishes the current nesting, explicit privacy and shared-provider behaviors needed here; it also demonstrates the root/nested replacement reply discrepancy. This leaf retains all three original acceptance checks. Historical bank/checkpoint/automatic source-watch work is not declared complete or added to this bounded replacement repair. Exact observations and source revision are recorded in baseline.json.

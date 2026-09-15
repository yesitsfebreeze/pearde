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
needs:
- "@root/a-nested-cartridge-is-a-first-class-entry"
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

## From the retired work memo

Folded 2026-09-15 from `work/the-profile-is-the-root-composer.md` (status open, estimate 2d). The PRD state above is authoritative.

> Composition lives in one place that a fiber can own, and the host profile is its depth-zero instance

### Outcome

There is one implementation of composition — validate the entries, resolve their
needs, spawn, watch, bank, replace — and it does not care how deep it runs. The
host profile is that implementation at depth zero. A cartridge whose config
carries an entry list composes those entries by the same rules, with the same
lifecycle guarantees, and is itself a cartridge to whoever composes it. No second
entry-instantiation path remains in the tree.

### Check

- [ ] One test body, parameterized by depth, passes identically for a profile
      entry and for the same entry composed inside a cartridge: it reaches the
      service, replaces the entry on a source edit, and keeps the bank.
- [ ] A fixture cartridge whose config names two child entries serves a key that
      one child provides and the other consumes, with no key of either visible
      to the profile that composed the parent unless the parent provides it.
- [ ] Composing the default profile through the same composer keeps `just run`
      and `zirkle run tool.memo` behaving as before, proven by the existing
      profile, lifecycle and foreground tests passing unchanged.
- [ ] A grep-backed count in the result shows one entry-instantiation site, not
      two, and the old path is deleted rather than deprecated.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. `Loader` owns composition end to end and only at the root:
`entries()` reads `.zirkle/<profile>/init.lua`, `expand` resolves globs
(`core/loader.rs:365`), `instantiate` spawns and banks each entry
(`core/loader.rs:677`), `reconcile` drives the set (`core/loader.rs:703`), and
`spawn` folds the entry's `isolate` list into the context (`core/loader.rs:671`).
A cartridge can already spawn a child (`core/context.rs:138`) but inherits none
of that. The two paths are the duplication this memo removes; per the repo's
no-legacy rule the flat one does not survive alongside the general one.

### Spec

Extract the entry set and its lifecycle into a composer value that takes a
directory, an entry list and a context, and returns handles. `Loader` keeps what
is genuinely the host's: the profile file, the file watcher, the build, the
socket. The composer is what a fiber can hold, so a cartridge that wants children
holds one.

The recursive case then needs no new concepts: a parent's `needs` are resolved in
its own scope, its children's keys default to its realm, and a child need declared
private (from [a-cartridge-declares-what-it-needs](../../../root/prds/a-cartridge-declares-what-it-needs/prd.md)) gets a fresh realm through
`Ctx::isolate` (`core/runtime.rs:545`), which descendants inherit
(`core/runtime.rs:184`). Sharing stays the default at every depth; otherwise a
tree of four cartridges that each need `router` gets four routers fighting over a
loopback port.

Deleting the old path is part of the work, not a follow-up: one composer, the
profile as its depth-zero call, and the fixtures that covered the flat path
rewritten against the parameterized test rather than kept beside it.

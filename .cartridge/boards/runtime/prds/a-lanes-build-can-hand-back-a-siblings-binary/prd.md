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
review-status: accepted
canonical-scope: a-lanes-build-can-hand-back-a-siblings-binary
commit: "6d1f9569296d9ce7dd310eed23236b035adeaefc"
---

# a lane's build can hand back a sibling's binary

Retain the measured cache-contamination evidence and move the executable outcome to runtime development tooling. Give each operation an isolated target and a wrapper cache key that distinguishes source revisions; if the wrapper cannot prove that property, disable it for isolated builds and measure the cost. Memory consumes correctly built artifacts but owns no host lane automation.

## Acceptance

- [x] Two worktrees change the same crate differently and executing each resulting binary proves its own behavior.
- [x] Repeating with the wrapper enabled/disabled identifies whether target isolation alone is sufficient; a wrong artifact fails the gate, not a manual strings warning.
- [x] The report preserves cold/warm timing, actual binary digests and source identities without changing unrelated worktrees or global cache configuration.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-lanes-build-can-hand-back-a-siblings-binary`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--a-lanes-build-can-hand-back-a-siblings-binary.md` (status open, claim b424ceba 2026-09-09 15:55, estimate 4h). The PRD state above is authoritative.

> `.cargo/config.toml` pins one shared `target-dir` and kache remaps every worktree to `/kache/workspace`, so a lane's build answers with a sibling lane's bytes — a binary that held none of its own change, and an rlib for a type absent from the worktree; a private `CARGO_TARGET_DIR` does not fix it, only `RUSTC_WRAPPER=""` did

Measured 2026-09-09 by the lane that landed
[the-installed-binary-answers-for-a-memory-that-is-gone](../../../memory/prds/the-installed-binary-answers-for-a-memory-that-is-gone/prd.md). It edited `commands`,
ran `cargo build --bin memory` in its own worktree, got `Finished in 0.11s`, and
the resulting `target/debug/memory` contained none of its change. It was caught
only by `strings`-grepping the binary for a literal the lane had just written.
Building with `CARGO_TARGET_DIR` set to a private directory cost 42 s cold and
was correct.

The mechanism is two things that are each reasonable alone. The trunk's
untracked `.cargo/config.toml` points every worktree at one `target/`, and kache
remaps every worktree path to `/kache/workspace`, so two lanes with different
source produce the same cache key for the root `memory` unit. Cargo then answers a
sibling's artifact as fresh. [[lanes-not-a-shared-tree]] names cross-lane kache
miscaching as its own overturn condition, and this is that condition met.

**This is the same vacuous pass as the memo above, one level down.** Six lanes
today checked their work against a daemon they built in-lane, precisely to
avoid the stale installed binary — and this defect means a lane that did that
may have measured a sibling's binary instead. Every clean answer from a lane
build is only as good as the binary that answered it.
[lane-gates-run-a-stale-cached-test-binary](../../../memory/prds/lane-gates-run-a-stale-cached-test-binary/prd.md) is the same root cause seen
through the test harness, and its branch is parked on the trunk's dirty
`justfile`.

**A private `CARGO_TARGET_DIR` is not enough, measured 2026-09-09 the same
day.** The lane that landed [memory-integration-cloud-disclosure](../../../memory/prds/memory-integration-cloud-disclosure/prd.md) set one and
kache still handed it a *sibling lane's* `store_core` rlib: `health` failed to
compile against an `EmbedRead` type that exists nowhere in that worktree. Only
`RUSTC_WRAPPER=""` — kache off — built the lane's own source. So the remap is
inside the wrapper's own cache key and not merely in cargo's target directory,
and every instruction issued today to "use a private target dir" was
insufficient advice.

Refined the same day by the lane that landed [memory-integration-template-hygiene](../../../memory/prds/memory-integration-template-hygiene/prd.md):
`/Users/feb/dev/memory/.cargo/config.toml` sets `target-dir = "target"`, so *every*
lane shares the trunk's, and a sibling rebuilding `hygiene-piece` mid-run handed
that lane a bogus `E0432: no is_unresolved_template in the root` for a symbol it
had just written. A private target dir under `/private/tmp` did not work either
— kache and dsymutil both failed on the workspace link — and only a target dir
**inside the lane's own worktree** built correctly. That is the third
independent sighting today, on three different crates.

### Do

Make a lane's build be the lane's own, or make a wrong one impossible to miss.
Two levers, and the measurement above rules the cheaper one out: a per-worktree
`CARGO_TARGET_DIR` is necessary and **not** sufficient, so the fix has to reach
kache's key — either the wrapper stops remapping distinct worktrees onto one
`/kache/workspace`, or `just lane` turns the wrapper off for lanes and pays the
cold build. Measure both before choosing: 42 s cold against a 0.11 s wrong
answer, and whatever a kache-less lane build costs across the workspace.

Do not fix this by telling people to `strings` their binaries.

### Check

Two lanes edit the same crate differently, both run `cargo build --bin memory`,
and each resulting binary holds its own lane's change — asserted by running the
binary, not by reading the cache's word for it. The cold-build cost per lane is
recorded here.

---

kind: work
level: 10
status: open
claim: b424ceba 2026-09-09 15:55
estimate: 4h
description: "`.cargo/config.toml` pins one shared `target-dir` and kache remaps every worktree to `/kache/workspace`, so a lane's build answers with a sibling lane's bytes — a binary that held none of its own change, and an rlib for a type absent from the worktree; a private `CARGO_TARGET_DIR` does not fix it, only `RUSTC_WRAPPER=\"\"` did"
read_when: "building a binary in a lane to check that lane's work, or reading a green check from a worktree"
---

# a lane's build can hand back a sibling's binary

Measured 2026-09-09 by the lane that landed
[[@prd/work/memory--the-installed-binary-answers-for-a-memory-that-is-gone.md]]. It edited `commands`,
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
[[@prd/work/memory--lane-gates-run-a-stale-cached-test-binary.md]] is the same root cause seen
through the test harness, and its branch is parked on the trunk's dirty
`justfile`.

**A private `CARGO_TARGET_DIR` is not enough, measured 2026-09-09 the same
day.** The lane that landed [[@prd/work/memory--memory-integration-cloud-disclosure.md]] set one and
kache still handed it a *sibling lane's* `store_core` rlib: `health` failed to
compile against an `EmbedRead` type that exists nowhere in that worktree. Only
`RUSTC_WRAPPER=""` — kache off — built the lane's own source. So the remap is
inside the wrapper's own cache key and not merely in cargo's target directory,
and every instruction issued today to "use a private target dir" was
insufficient advice.

Refined the same day by the lane that landed [[@prd/work/memory--memory-integration-template-hygiene.md]]:
`/Users/feb/dev/memory/.cargo/config.toml` sets `target-dir = "target"`, so *every*
lane shares the trunk's, and a sibling rebuilding `hygiene-piece` mid-run handed
that lane a bogus `E0432: no is_unresolved_template in the root` for a symbol it
had just written. A private target dir under `/private/tmp` did not work either
— kache and dsymutil both failed on the workspace link — and only a target dir
**inside the lane's own worktree** built correctly. That is the third
independent sighting today, on three different crates.

## Do

Make a lane's build be the lane's own, or make a wrong one impossible to miss.
Two levers, and the measurement above rules the cheaper one out: a per-worktree
`CARGO_TARGET_DIR` is necessary and **not** sufficient, so the fix has to reach
kache's key — either the wrapper stops remapping distinct worktrees onto one
`/kache/workspace`, or `just lane` turns the wrapper off for lanes and pays the
cold build. Measure both before choosing: 42 s cold against a 0.11 s wrong
answer, and whatever a kache-less lane build costs across the workspace.

Do not fix this by telling people to `strings` their binaries.

## Check

Two lanes edit the same crate differently, both run `cargo build --bin memory`,
and each resulting binary holds its own lane's change — asserted by running the
binary, not by reading the cache's word for it. The cold-build cost per lane is
recorded here.

---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
needs:
- "@memory/lane-gates-run-a-stale-cached-test-binary"
estimate: "4h"
actual: "3h"
---

# Eighteen sites still take their repository root from a compile-time CARGO_MANIFEST_DIR that the shared target directory can bake with another worktree's path — a count that moves both ways, so read it from the tree rather than from here

## Do

`env!("CARGO_MANIFEST_DIR")` is resolved when the test binary is built, and
the workspace shares one `target/` across every lane, so `cargo nextest run
--workspace` can pick a binary another worktree built and walk a path that
no longer exists. On 2026-09-07 this failed `test_support` and `util` in
three herd gates in a row; both now read `std::env::var("CARGO_MANIFEST_DIR")`
at run time, which cargo and nextest set per package for the tree being
tested. Do the same at the remaining sites, all under `tests/` and
`src/*/src/tests/`: `rg -n 'env!\("CARGO_MANIFEST_DIR"\)' src tests --type rust`
lists them, including the three `concat!` forms in `tests/e2e/eval_ground.rs:10`,
`tests/bench/src/ground.rs:57` and
`src/commands/src/tests/commands_mcp_test.rs:17`, which become a
`PathBuf::from(var).join(..)`.

**Count it before sizing the job.** Eighteen sites on 2026-09-08, against the
seventeen this memo was filed with the same day, even though `8bf0b358` and
`267bcdde` converted two in between — the set loses members to this work and
gains them from every new test that reaches for the macro, so the number is
the tree's to report and not this memo's to hold.

**Ordered behind the cause, 2026-09-08.** [lane-gates-run-a-stale-cached-test-binary](../lane-gates-run-a-stale-cached-test-binary/prd.md)
measured why the wrong binary runs — the trunk's `.cargo/config.toml` points
every worktree at one `target/`, and cargo's integration-test artifact name
does not vary with the worktree path, so two lanes overwrite one file — and
gives each lane its own target dir. That memo's `Do` also refuses the runtime
read as *its* fix, because it would hide the overwrite from every other test
using the macro. So these eighteen sites are defence in depth behind a fixed
cause, not the fix, and they wait for that branch to land.

**Nineteen sites, landed 2026-09-09.** The tree reported nineteen that day, not
the eighteen in the description: fourteen plain `PathBuf::from(env!(..))`, two
`Path::new` borrows that need an owned `PathBuf` to hold, and the three
`concat!` forms that became `PathBuf::from(var).join(..)` because a macro cannot
take a run-time read. All nineteen now call
`std::env::var("CARGO_MANIFEST_DIR")`, in two commits on `main`.

`rg -c` prints nothing and `cargo nextest run --workspace --no-fail-fast` is
1461 of 1462. The one red is a lane artefact and not this work's:
`memory::cited_paths` reports `src/rpc/src/plan.rs:2` citing a path in a
gitignored nested clone that lives only in the trunk, so no worktree can
resolve it — which is exactly what an
honest run-time read exposes and a baked path hid. It is owned by
[the-plan-crate-cites-an-untracked-file](../the-plan-crate-cites-an-untracked-file/prd.md).

Two other reds met on the way were main's and were fixed there first: three
citations that followed the exit test out of the `commands` crate, and
`one_llm_client`'s path-based `is_test_code`, blind to an inline `#[cfg(test)]`
module.

## Acceptance
`rg -c 'env!\("CARGO_MANIFEST_DIR"\)' src tests --type rust` prints nothing, and
`cargo nextest run --workspace` is green from a lane whose sibling lane was
removed after building the same crates.

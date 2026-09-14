---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: development-tooling-has-one-home
footprint:
- /Users/feb/dev/cartridge/.cartridge/tests/integration/source-layout.test.ts
- /Users/feb/dev/cartridge/*.ctg/cartridge.json
---

# Development documents work from a clean checkout

In a fresh recursive clone, every documented development command resolves to a recipe that exists. The existing [source-layout.test.ts](../../../../../../.cartridge/tests/integration/source-layout.test.ts) already clones the composition with its submodules into a temporary folder and checks the memory pin. It does not check commands. They are stale today. For example, `tools.ctg/cartridge.json` `commands` run `just --justfile ../cartridge.ctg/justfile build|check|test|process|verify tools`. That justfile only has `build *args`, `test *args`, `check` and `fmt`, and forwards extra arguments to `cargo --workspace` (commit b1494bb: the base is not a composition). The composed recipes live in the root `.cartridge/justfile`.

## Acceptance

- [ ] In the temporary recursive clone, the extended test resolves every `*.ctg/cartridge.json` `commands.*.argv` that invokes `just` against its justfile (`just --justfile … --summary` holds the recipe) from its declared `cwd`.
- [ ] Stale entries found on first run go into a checked-in baseline list next to the test. A stale entry not on the list fails the test and is named. A listed entry that now resolves also fails, so the list only shrinks.
- [ ] Tracked files in the clone contain no absolute developer-home path (`/Users/`, `/home/`) outside `prd.ctg` records and memo history.

## Proof and recovery

Run the check first and record the stale list as the baseline. Gate, cwd `/Users/feb/dev/cartridge`: `bun test .cartridge/tests/integration/source-layout.test.ts`, which `just test` also runs. Not run. Fixing the listed manifests is each owner's own follow-up and is not this leaf's acceptance. Rollback: delete the check. The host never executes `commands` while reading.

## Dependencies and review

No hard prerequisites. The earlier needs (runtime-development-package, preflight, provenance, worktree-resume) are independent outcomes. The shim clause is dropped because no shim exists. [Review](review.md): inherits 2 rounds.

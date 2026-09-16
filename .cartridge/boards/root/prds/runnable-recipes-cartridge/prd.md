---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: runnable-recipes-cartridge
---

# A recorded procedure is runnable, not just readable

`memo.ctg` records what was decided and why. Nothing records a procedure in a form that can be run again. A sequence of steps that worked once is re-derived from prose every time, which is how a step gets dropped. Port pi's `recipes` as `recipes.ctg`: a recorded procedure is searchable and executable, and a run reports which step it stopped at.

A recipe is not a shell script under another name. Its steps are declared, its inputs are named, and a step that cannot run because an input is missing is reported as such before the recipe starts, not discovered at that step. Where a recipe's steps are themselves a flow, `flow.ctg` owns that; recipes stay the linear, human-recorded form.

## Acceptance

- [ ] A recorded recipe is retrievable by search over its name, its steps and its declared inputs, and the result names the recipe's source record.
- [ ] Running a recipe whose declared input is unsupplied reports the missing input before any step runs.
- [ ] A run reports each step's outcome in order and stops at the first failing step, naming that step and its output.
- [ ] A recipe is recorded through `memo.ctg`'s validated write rather than a second store, and an invalid recipe is refused at write time.
- [ ] Recording, search and a full run are tested offline in `just test recipes` with fixture recipes whose steps touch only a disposable directory.

## Proof and recovery

Port from `/Users/feb/dev/pi/packages/coding-agent/src/core/recipes/` (933 lines at survey, verified present). Upstream keeps its own store; here the record belongs to `memo.ctg`, which already owns typed Markdown records with validated writes, so this cartridge adds the execution half and no second store. Confirm at port time that a `kind: recipe` memo type can carry declared steps and inputs; declaring that type is part of this work.

Gates, cwd `/Users/feb/dev/cartridge`: `just test recipes`, `just check recipes`. Not run for this plan.

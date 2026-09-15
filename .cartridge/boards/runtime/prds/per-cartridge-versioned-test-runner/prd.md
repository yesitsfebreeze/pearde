---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: per-cartridge-versioned-test-runner
---

# per cartridge versioned test runner

`just test <owner>` records its result as evidence keyed by what it verified,
and `just verified <owner>` reports that evidence as fresh, stale (with the
changed input named) or missing, without running anything. The key covers the
owner's git HEAD plus a digest of its dirty diff, the digest of `Cargo.lock` or
`bun.lock`, the cartridge.ctg revision it builds against, the digest of the
recipe block, `rustc -V`/`bun --version`, and `uname -sm`. The manifest version
stays descriptive only.

Owner: the composition. Gates are root recipes
(`.cartridge/memos/routine/cartridge-development.md`, run through
`.cartridge/tools/memo-run`), and cartridge.ctg is "the base, not a composition"
(b1494bb). Evidence lives under the ignored `.cartridge/empirical/verification/`,
with no Python (layout decision). Both files are uncommitted in the root
checkout today.

## Acceptance

- [ ] Changing an owner's code without a version bump makes `verified` report stale and name the source input; rerunning the test refreshes it.
- [ ] Changing the lockfile, cartridge.ctg revision or recipe text marks only dependent owners stale; unchanged inputs report fresh with the prior exact result.
- [ ] A failed or interrupted run records a failure and never replaces a prior success as success. Two divergent worktrees keep separate evidence and targets.

## Proof and recovery

Add `.cartridge/tests/integration/verification-evidence.test.ts` using a
disposable git fixture, and extend the `test all` branch of
`cartridge-development.md`, which runs only `source-layout.test.ts` today, to
include it. Gates, from `/Users/feb/dev/cartridge`: `just test all` and
`just check all`. Deleting the evidence directory is a safe reset: gates run as
they do now.

## Dependencies and review

No hard prerequisite. The root board is the natural home. [Review](review.md): round 3/5.

## From the retired work memo

Folded 2026-09-15 from `work/per-cartridge-versioned-test-runner.md` (status open). The PRD state above is authoritative.

> Run a cartridge's own tests when its declared version changes, keyed per cartridge and version

### Outcome

Every cartridge owns its responsibility and is verified individually: its
registration contract runs at apply, and its tests run automatically when the
cartridge changes. The trigger is a version in the manifest — bumping
`version` in `cartridge.json` re-runs that cartridge's suite; an unchanged
version keeps the recorded result.

### Check

- [ ] `cartridge.json` accepts an optional `version`; a bumped version makes
      the runner re-run that cartridge's tests on the next watch cycle.
- [ ] Only the changed cartridge's tests run; unrelated cartridges are not
      re-verified.
- [ ] The runner records `{cartridge, version, result, evidence}` and serves
      the last result without re-running while the version is unchanged.
- [ ] A failing suite reports per cartridge, naming the cartridge, and the
      rest of the profile keeps running.

### Approach

- A runner service records results per `(cartridge, version)` under
  `.zirkle/` state; the watch/reload path already knows which cartridges
  changed (`replace_changed`), so it hands that set to the runner.
- Per-cartridge suites map to what exists: `cargo test -p <name>` for Rust
  cartridges, `bun test` for `ui`, the Python suite for `tools`, plus the
  declared `selftest`/`integration` contracts that `zirkle --profile tools
  verify` already runs.
- The scoped-gate practice ([[fresh-checkout-gates]], "the gates are scoped
  to the diff") becomes mechanical: the version is the diff marker.

### Context

- [[zirkle-diagnostics-leaks-into-pty-tests]] — test runners must scrub the
  parent environment (`ZIRKLE_DIAGNOSTICS`, `ZIRKLE_PROXY_KEY`,
  `ZIRKLE_MODEL_KEY`) before spawning cartridges, or suites fail on
  inherited state the cartridge never chose.

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

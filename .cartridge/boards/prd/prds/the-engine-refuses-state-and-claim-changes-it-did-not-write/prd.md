---
state: "analyzing"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/prd.ctg"
footprint:
  - src/records.ts
  - src/lifecycle.ts
  - src/engine.ts
  - .cartridge/tests/records.test.ts
  - .cartridge/tests/engine.test.ts
claim: "coordinator-c4-530 2026-09-16T09:33:49.756Z"
---

# the engine refuses state and claim changes it did not write

## Outcome

`state`, `claim` and `commit` change only through engine ops. On 2026-09-16 an
analyst rewrote a whole prd.md from its draft and reset `analyzing` + claim to
`open`, and a second coordinator released another coordinator's live claims.
Nothing flagged either. The engine should detect a frontmatter change it did
not make, for example by keeping a digest of the controlled fields per PRD
under the board's `.state/` whenever `edit()` in `src/records.ts` writes them. `check`
(`src/engine.ts`) then reports the
mismatch, and the next transition on that PRD refuses until an explicit
reconcile op accepts or restores the recorded values.

## Acceptance

- [ ] Hand-editing `state` or `claim` in a claimed PRD makes `prd check` report a problem naming the PRD and the field.
- [ ] `claim`, `release` and `collect` on that PRD refuse with the same reason until it is reconciled.
- [ ] Body edits and engine transitions produce no problem.
- [ ] `bun test ./.cartridge/tests/engine.test.ts` (cwd `prd.ctg`) passes with a test for each case above. `records.test.ts` is red at HEAD for reasons outside this PRD (see `@prd/the-records-test-knows-deferred-and-the-current-root-board`).

## Planning note

2026-09-16, coordinator cartridge-c4, from analyst-1. This guard catches frontmatter written outside the engine. A second coordinator releasing a live claim goes *through* the engine, so this guard can't catch it. PROMPT.md's one-coordinator rule and ListAgents cover that case.

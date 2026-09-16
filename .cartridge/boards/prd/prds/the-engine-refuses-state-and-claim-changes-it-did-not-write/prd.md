---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/prd.ctg"
footprint:
  - src/records.ts
  - src/lifecycle.ts
  - src/engine.ts
  - src/cli.ts
  - .cartridge/tests/engine.test.ts
commit: "14fad070be1b474db3405025042a5bb75c7fa6b6"
---

# the engine refuses state and claim changes it did not write

## Outcome

`state`, `claim` and `commit` change only through engine ops. On 2026-09-16 an
analyst rewrote a whole prd.md from its draft and reset `analyzing` + claim to
`open`, and nothing flagged it. The engine records the values it writes per PRD
under the owner board's `.state/fields/`. `check` (`src/engine.ts`) reports a
mismatch, and every later op on that PRD refuses it until the recorded values
are restored by hand or `prd adopt <ref> --by <id> --reason "<text>"` accepts
the current ones and appends an audit line.

## Acceptance

- [x] Hand-editing `state` or `claim` in a claimed PRD makes `prd check` report a problem naming the PRD and the field.
- [x] `claim`, `release` and `collect` on that PRD refuse with the same reason until it is reconciled; adoption requires `--by` and `--reason` and is logged.
- [x] Body edits, engine transitions and a PRD re-added at a removed path produce no problem.
- [x] `bun test ./.cartridge/tests/engine.test.ts` (cwd `prd.ctg`) passes with a test for each case above. `records.test.ts` is red at HEAD for reasons outside this PRD (see `@prd/the-records-test-knows-deferred-and-the-current-root-board`).

## Planning note

2026-09-16, coordinator cartridge-c4, from analyst-1. This guard catches frontmatter written outside the engine. A second coordinator releasing a live claim goes *through* the engine, so this guard can't catch it. PROMPT.md's one-coordinator rule and ListAgents cover that case.

2026-09-16, review round 2 (B3). The recorded values are keyed by the PRD's path, so a record moved to a new path (`mv prds/one prds/two`) is trusted at that path on first observation. The guard does not stop that; it makes it visible, by logging the values it drops with the old path and warning on the `check` that drops them. spec01's "Out of scope" states the limit.

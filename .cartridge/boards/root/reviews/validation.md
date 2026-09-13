# Small PRD validation

This record covers the authored work map and PRDs, not product correctness.

Validated on 2026-09-13 from the composed repository root:

- `python3 .cartridge/check-work-map.py`: exit 0. All 159 sources map to 180
  canonical PRDs. The 139 leaves have three to five acceptance checks and stay
  below 400 words. Local links, exact review input digests and the DAG pass.
- The installed Pearde scanner finds all 180 PRDs. Its dependency resolver
  resolves 244 explicit and implicit child edges with no cycles.
- `pearde workflow check .cartridge` and `pearde grammar check .cartridge`:
  exit 0.
- Memory documentation was authored and checked in its isolated worktree,
  committed as `67ec7cc`, then fast-forwarded into the composed memory checkout.
  Its staged whitespace check passed. Existing reserved work and stores were
  preserved.

`just board-check` remains red at `pearde memo check`: a concurrent migration
moved native memos into the root record. For example, `archive-formats.md` uses
native `kind:` metadata, while this Pearde validator expects `memo:`, `status:`,
`subject:` and `date:`. The PRD check runs first and passes. This pass preserved
the concurrent move rather than rewriting those records into another format.

A native memo API attempt to extend `plan-cartridge-work` also refused during
that migration because the remaining runtime record lacked the `routine` kind
declaration. It wrote nothing. The invoked root review/read-context/write-specs
workflows and PRD template contain the small-PRD and canonical-alias rules.

Plan review is round 2 of at most 5, attributed to `/root` self-review. There are
178 passing plan reviews and two failures: Linux runtime evidence prerequisites
and the unidentified semantic-tool provider. These scores do not establish
implementation readiness when a dependency or spec is still outstanding.
No product tests were run for these documentation changes.

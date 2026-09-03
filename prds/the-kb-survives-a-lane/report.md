Verdict: SPECCED

workflow: probe-then-spec

## What the build found

The PRD's premise — a lane's `knowledge.py remember`/`conclude` writes into a
tree that `collect` never stages, so the finding dies with the worktree — is
already false on this checkout. Two prior fixes closed it:

- `knowledge.py` `default_root` climbs from the cwd to the board above it
  (`common.board_above`), the same rule every other board reader uses,
  instead of resolving beside its own script copy (fixed after
  `wiki/sources/260902-2085.md` documented the silent 0-notes regression).
- `resources/board/lanes.py` `create` excludes the board dir from a lane's
  checkout with a `--no-cone` sparse-checkout (`wiki/sources/260902-b6be.md`),
  so a lane never materialises a phantom `.pearde` copy to climb into.

A lane's worktree sits at `<board>/.lanes/<slug>` — physically inside the
live board, never a copy of it — so `remember`/`conclude` run from a lane
land in the same `wiki/sources/`/`wiki/conclusions/` the board's own session
writes, immediately, with no collect and no reroute. Verified live: a
`remember` run from inside this lane wrote straight into
`/Users/feb/dev/infra/pearde/.pearde/wiki/sources/`, found by a `query` with
no collect in between (note removed after, kept out of the record). `wiki/`
is absent from `resources/board/shared.py`'s candidate table, so `share
apply`/`share undo` has nothing of the KB's to seed or restore — it is never
duplicated per lane in the first place. `probe/verify.sh` (left in the tree,
uncommitted) proves all four points on disposable fixtures, 5/5, stable
across repeated runs.

## Findings (not specced)

- The PRD's `## Fails when` box — "two lanes conclude the same question at
  once" — describes a real hazard shape (`cmd_conclude` checks
  `target.exists()` then writes, no atomic create), but I could not make it
  fail: 25+ concurrent same-title `conclude` trials always produced exactly
  one success and one clean refusal, never a merge and never two silent
  successes. A check that could not fail — no spec written for it.
- The source doc the PRD cites, `docs/content/docs/improvements/knowledge-share.mdx`,
  is genuinely gone from the working tree (confirmed absent); recovering it
  is outside this PRD's footprint and not attempted.
- Query against the record returned 103 hits, no gap enqueued (`103 notes on
  record`, top hit was 260902-2085 above); no `wiki/pending/` entry is mine.

## Scores

complexity: 5
blast-radius: low
workflow: probe-then-spec

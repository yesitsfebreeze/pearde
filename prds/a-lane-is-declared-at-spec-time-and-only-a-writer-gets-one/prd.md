---
state: open
origin: requested
priority: 70
complexity: 0
blast-radius:
---

# a lane is declared at spec time and only a writer gets one

`pearde claim` cuts a lane — a full git worktree — for every PRD,
including the ones whose worker only reads. Measured 2026-09-03: 51 lanes
under this board holding 341 MB, 37 of them clean and claimless; among the
clean ones, several were cut for analysts and researchers that never wrote
a file (an analyst's probe sometimes stands, mostly nothing does). The
`every-worker-runs-in-its-own-worktree` PRD fixed a real collision —
unlimited workers in one tree — but its cost was paid at the claim, where
the worker's intent is already known: the analyst's own brief, the
workflow slug, the footprint.

When this is done: the spec, not the claim, declares whether the PRD's
work is a write. A frontmatter key (`lane: write` / `lane: read`, or
absent — default `write`, because every PRD on the board today carries an
implementer that edits) states the contract, the analyst writes it as part
of speccing, and `claim` honours it: `lane: read` cuts no worktree, the
brief names the checkout as `<repo>` (exactly the pre-lane path, which
`brief.repo_of` already falls back to when no lane dir is on disk), and
`collect` merges nothing for it. The claim gate, the baseline snapshot and
the sweep are unchanged — a read PRD still snapshots and still reclaims.
The key joins `FRONTMATTER_KEYS` in `init.py`, so `claims.py bad_keys`
does not refuse it and `pearde grammar check` stays green.

Must not change: the lane branch name and `plan.LANE_RE`'s reading of it;
`lanes.create`'s idempotent-return rule; the default — a PRD that says
nothing gets a lane, because the cost of a wrongly-cut lane is disk and
the cost of a wrongly-shared tree is the collision
`every-worker-runs-in-its-own-worktree` was filed over.

Pointers: `resources/board/transitions.py` (`cut_lane`, the `transition`
claim edge), `resources/board/lanes.py` (`create`), `resources/board/
brief.py` (`repo_of` — the no-lane fallback is already the read path),
`resources/board/init.py` (`FRONTMATTER_KEYS`),
`.pearde/prds/every-worker-runs-in-its-own-worktree/prd.md`.

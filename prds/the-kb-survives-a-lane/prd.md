---
state: done
origin: requested
priority: 36
complexity: 5
blast-radius: low
workflow: probe-then-spec
commit: 4a0cf19
---


# The KB survives a lane

*Source: `docs/content/docs/improvements/knowledge-share.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** knowledge · **Axis:** integration (7 → 8) · **Pulls the score up
by ~4 points**

## Why now

The KB writes only under `.pearde/wiki/` — gitignored, machine-local. A
worker running in its own worktree (every worker does) that captures a
finding or concludes a synthesis writes it into a tree that collect never
stages: the finding dies with the worktree. `share` regenerates what every
lane rebuilds — node_modules, the graphify cache, the Obsidian bundles —
but the KB is not regenerable; it is accumulated judgment, and the one
directory whose loss is real is the one `share` cannot carry.

## The change

Capture and conclude write through the board's shared directory when they
run outside the board's own tree — the same rule `collect` uses to move
board state: the note lands under the git common dir's KB store and is
symlinked or copied back by the same `share apply` that seeds the regenerable
dirs. The board's own session (writing in place) is unchanged; only a
lane-rooted write is re-routed.

## Done when

- A worker in a lane worktree runs `knowledge.py remember <title>` and the
  note exists in the board's `wiki/sources/` after the lane collects — the
  check is a collect followed by a board-side `query` that finds it.
- The same command run on the board itself writes in place, byte-identical
  to today — no lane, no rerouting.
- `share apply` after the write finds the note already seeded and does
  nothing; `share undo` puts the checkout back as it was.

## Fails when

- Two lanes conclude the same question at once — two notes, one slug. The
  slug collision is resolved the way the board resolves two children with
  `settings.md`: refuse and name both, never merge by guess.

## What stays out

No un-gitignoring of `wiki/` — machine-local remains true for hand edits and
the dashboard; only the tool's own writes are re-routed, because a lane
cannot be trusted to push what git cannot see.

## History

**failed, retried 2026-09-03 21:37**

**2026-09-03 21:4x — the claim is dead; the report is the analyst's**

The report on disk is the analyst's SPECCED (mtime earlier than the claim's
`since`), so no implementer ever returned. The worker's session was reaped —
no process on this machine holds it. The claim only reads live because its
footprint names shared files other sessions keep writing
(`silence-measures-the-workers-own-tree` names the artefact). The analyst's
work stands in `specs/`; the next implementer continues from it.

## Blocked

**2026-09-03 21:57 — the lane will not rebase**

`lane/the-kb-survives-a-lane` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-kb-survives-a-lane` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-kb-survives-a-lane`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/the-kb-survives-a-lane` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-kb-survives-a-lane` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-kb-survives-a-lane`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/the-kb-survives-a-lane` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-kb-survives-a-lane` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-kb-survives-a-lane`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/the-kb-survives-a-lane` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-kb-survives-a-lane` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-kb-survives-a-lane`.

**2026-09-04 02:40 — the lane will not rebase**

`lane/the-kb-survives-a-lane` does not land on `session/s85810`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-kb-survives-a-lane` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-kb-survives-a-lane`.

## Report

spec01: exit 0
== A: a lane-shaped cwd resolves default_root to the board above it ==
  ok   default_root from <board>/.lanes/some-slug == <board>/wiki
== B: remember run from that lane-shaped cwd lands in the board's wiki/sources, no --root, no rerouting ==
  ok   remember from the lane-shaped cwd added one note under the board's wiki/sources
== C: the same command run with cwd == the board itself writes the identical layout (no lane, no rerouting) ==
  ok   remember on the board itself wrote wiki/sources/ beside prds/ and settings.md, same as a lane would
== D: wiki/ is not on share's candidate list — it is never duplicated per lane, so nothing needs seeding back ==
  ok   shared.py names no wiki/ candidate — a lane never gets a copy of it to seed back
== E: two conclude calls racing the same title do not silently merge or drop one body ==
  ok   exactly one of two racing conclude calls on the same title succeeded, the other refused

== summary: 5 ok, 0 fail ==

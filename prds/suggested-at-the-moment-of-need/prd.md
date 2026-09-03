---
state: open
origin: requested
priority: 0
complexity: 0
blast-radius:
needs:
  - the-capability-registry
---
---

# Suggested at the moment of need

*Source: `docs/content/docs/improvements/integration-suggest.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Layer:** suggest · **Tool:** board (the brief) · **Unblocked by:**
[the registry](/docs/improvements/integration-registry)

## Why now

The loop already suggests, but only three kinds of things, at three fixed
moments: the brief names the unhealthy files (health's pointer), routes
`workflow: <slug>` when a PRD declares one, and the pass carries the board's
own verbs in the manual. What no moment carries: scout's reading list when a
dependency question opens mid-pass, the knowledge verbs when a conclusion is
half-formed, the view's URL when a person is waiting on the pass, the vault
when a wiki note is due. The capabilities exist; the *timing* is missing —
every suggestion mechanism fires at session start or not at all, and a
worker past its first compaction holds none of it.

## The change

The brief gains one section: **applicable capabilities** — registry rows
whose *reads and writes* intersect the pass's footprint. A pass whose
footprint touches `.pearde/wiki/` carries the knowledge verbs; one opening
a question about a dependency carries scout's `route`; one the user is
waiting on carries the view URL. Session start gets the same one section,
computed from the board's state (a board with pending asks surfaces the
asks view; a board unscored in 30 days surfaces `health score`). **Three
rows maximum** — a suggestion wall is a wall.

## Done when

- A brief for a PRD whose footprint names `wiki/conclusions` carries the
  five knowledge verbs' rows — and a PRD with no knowledge footprint
  carries none; the check is two PRDs, two briefs, one diff.
- The section is cut by the same compaction the rest of the brief
  survives: the rows ride in the pass file (@@pass), so the suggestion
  outlives the compaction that killed the manual.
- Every row in the section is a registry row — the suggestion composes the
  registry verbatim, never paraphrases a verb into a second description.

## Fails when

- The intersection rule over-suggests: a PRD touching ten directories
  carries a wall. Guard: rows are ranked by how much of the footprint they
  meet (whole-footprint rows first), capped at three, and the cut names
  what it cut — the reader can always ask for the rest.

## What stays out

No model choice, no scoring in the injection — selection is set
intersection on paths the footprint already declares, deterministic and
reviewable in the brief itself. Where a *judgment* is needed (which of two
verbs), the tie is broken by the usage ranking the third page builds, not
by the injector.

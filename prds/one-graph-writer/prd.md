---
state: done
origin: requested
priority: 36
complexity: 21
blast-radius: mid
workflow: probe-then-spec
---


# One graph writer

*Source: `docs/content/docs/improvements/knowledge-one-graph.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** knowledge · **Axis:** complexity (6 → 7) · **Pulls the score up by
~4 points**

## Why now

One note graph, four writers and readers: `graph.sh extract` maps the repo
(semantic passes included), `knowledge.py relink` maps the KB from
wikilinks, `graphs/` renders communities as wiki pages, `Dashboard.md`
renders Dataview views over the whole. Relink symmetrizes `related:` and
writes `.pearde/wiki/.graphify/graph.json`; graphify writes *its* graph.json
over the repo. The two formats answer the same question — what links to
what — with two schemas, and every reader (health's fan-out axes, the
dashboard's sources) must know which one it is reading. Health's graph read
already carries the scar: "a graph naming fewer than half the scored files
was built from another root and reads as none".

## The change

One graph format, one writer: `.pearde/wiki/.graphify/graph.json` gains a
`root:` field (`repo` | `kb`) and edges typed the same on both sides, and
relink's writer merges the KB graph *into* the repo graph as a second root
instead of a sibling file. `graphs/` and the dashboard read the merged
graph through one loader. Health's graph reader stops guessing the root —
the file says which it is.

## Done when

- One `graph.json` holds both roots; `python3 -c` reading it finds a `root`
  field per node, and no second graph file exists under `.pearde/`.
- Health's fan-in/fan-out read the merged file and its "built from another
  root" summary line is gone — the graph now says its own root.
- `relink` after a `graph.sh extract` run leaves the repo's edges intact
  (merge, not replace) — the check is a byte-diff of the repo edges across
  the relink.

## Fails when

- The merge doubles an edge when both roots record it. Guard: edges are
  keyed by (source, type, target) and the merge is a set-union, checked by
  the same self-check that proves the repo edges survived.

## What stays out

No schema redesign, no LLM pass — the KB graph stays hand-built wikilinks.
The page is a merge plus a loader, and the loader is the deliverable: one
reader of the graph format, where four exist today.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 21:01 — claim impl-graph-writer 2026-09-03 17:46, silent 3.3h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/one-graph-writer`, whose worktree this sweep removed — the branch is kept.

## Blocked

**2026-09-03 21:56 — the lane will not rebase**

`lane/one-graph-writer` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-03 23:39 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s5285`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-03 23:40 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s5285`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/one-graph-writer` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-04 02:42 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s85810`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/one-graph-writer` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-graph-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-graph-writer`.

## Report

spec01: exit 0
knowledge.py compiles
  ok    relink runs clean
  ok    one graph.json, root field per node, no sibling file
  ok    relink leaves the repo edge intact (merge, not replace)
  ok    a second relink does not double the edge or the kb nodes
  ok    relink after a fresh graph.sh extract carries the new repo edges through
  ok    doctor reports no false staleness against the repo's own (far larger) node set

6 checks · 6 pass · 0 fail

spec02: exit 0
health.py compiles
  ok    health drops kb nodes/links by root before file_of and the link scan
  ok    fan-in/fan-out compute correctly off the root-filtered links
  ok    the 'built from another root' guess is gone from health.py's wording

3 checks · 3 pass · 0 fail

---
complexity: 7
workflow: probe-then-spec
footprint:
  - resources/health.py
---

# spec02 — health reads the merged graph by `root`, and drops the "another root" guess

Once `graph.sh extract`'s own file also carries the KB's nodes and edges
(spec01), `health.py`'s `load_graph`/`graph_axes` — the only other reader of
`graphify/graph.json` — must not let a KB node or edge into its code-only
view: a KB node has no `source_file`, so it was already silently skipped, but
a KB edge's `relation` (`derives`, `links`, `related`) is not in
`GRAPH_RELATIONS`, so those were already skipped too — this unit makes both
skips explicit, by `root`, rather than incidental.

**All of it already stands in the tree, uncommitted.**

## What already stands

- `load_graph` (`resources/health.py:556-587`) — a node or link tagged
  `root: kb` is dropped before it reaches `file_of` or the returned `links`
  list; a node or link with no `root` at all (graphify's own output before
  any `relink` has ever run) still counts as the repo's, unchanged from
  today.
- `graph_axes` — its match-ratio guard is unchanged in mechanics (it still
  measures how many scored files the graph's nodes cover), but the message it
  returns when that ratio is low no longer says "built from another root?" —
  `file_of` is now built only from nodes the file itself marks `root: repo`
  (or leaves unmarked, the pre-relink case), so a low match is staleness or a
  partial extract, not a guess about whose graph this is. The wording is
  `"graph paths match {n} of {m} files — stale or partial extract?"`.

## What is left to finish

Nothing to build.

## Acceptance

- [x] `load_graph` on a merged `graph.json` (repo nodes/links tagged
      `root: repo`, KB nodes/links tagged `root: kb`) returns a `file_of` map
      holding only the repo's `source_file`s, and a `links` list holding only
      the repo's links — no KB id and no KB link survives.
      `ok    health drops kb nodes/links by root before file_of and the link scan`
- [x] `graph_axes` computed off that filtered graph reports the same
      `fan_out`/`fan_in` it would have reported against a repo-only file —
      the KB entries change nothing about the count.
      `ok    fan-in/fan-out compute correctly off the root-filtered links`
- [x] The string `"built from another root"` no longer appears anywhere in
      `resources/health.py`.
      `ok    the 'built from another root' guess is gone from health.py's wording` (grep -c: 0)
- [x] `python3 -m py_compile resources/health.py` — compiles.
      `health.py compiles`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -m py_compile resources/health.py && echo "health.py compiles"
bash .pearde/prds/one-graph-writer/probe/verify_health.sh
```

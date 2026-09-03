---
state: open
origin: requested
priority: 0
complexity: 0
blast-radius:
needs:
  - usage-snapshots-ranked-over-time
---
---

# Scout reads our own deltas

*Source: `docs/content/docs/improvements/integration-scout-self.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** scout · **Unblocked by:**
[usage snapshots](/docs/improvements/integration-usage)

## Why now

Scout runs the complete discovery loop — buckets, snapshots, deltas, routes,
findings, a reading list mapped to *a specific tree* — and every mechanism
is aimed outward at GitHub. Nothing stops it from aiming inward: a bucket is
a `name<TAB>query` line and the taxonomy is *the knob*. Our own usage
snapshots land in the same TSV shape scout's star snapshots keep; our own
deltas are diffs over them; our verbs are repos-with-a-state-column in
miniature. The tool that answers "what is worth studying" has never been
pointed at the one corpus it is cheapest to study — ours — and the gap is
invisible because the answer "we already know our own tools" is exactly the
answer scout exists to distrust.

## The change

Two rows in the existing files, no new tool:

1. **A self bucket.** `buckets.txt` gains `pearde-tools<TAB>` — a query
   against our own capability registry (the local TSVs, not GitHub): the
   sweep folds our verbs into the same snapshot file the star deltas read,
   so `scout.sh delta` names `pearde.view.reap` beside every trending repo,
   same output shape, same findings record.
2. **A reading-list row per our own docs.** `reading-list.md` gains rows
   mapping *our improvement pages* to what they teach the tree — the curate
   layer already holds "what this teaches this tree"; our own pages are the
   cheapest rows it will ever carry, and the check page gives them the same
   staleness marking every other row gets.

## Done when

- `scout.sh sweep` produces a TSV containing the `pearde-tools` bucket's
  rows (verb, calls, suggestions), and `scout.sh delta 7` ranks a dead verb
  beside a dead repo — both named on the same findings page.
- `reading-list.md` carries one row per improvement page under
  `docs/improvements/`, mapping it to the tree's need, checked by the same
  check every other row passes.
- The buckets knob still decides everything: removing the row removes the
  bucket, no code changed.

## Fails when

- The self bucket's query is shaped like a GitHub query and finds nothing —
  the sweep's one-search-per-bucket contract assumes a search backend.
  Guard: the row's query names the *local* source (`usage/<date>.tsv`), and
  the sweep reads a file where it would have searched — the bucket layer
  has always been about *what to watch*, not where the watch runs.

## What stays out

No new ranking algorithm, no second cron — the snapshots, the diff, the
findings record and the pruning cap all exist. The page is two data rows
and the honest admission that the cheapest corpus to study is the one we
wrote.

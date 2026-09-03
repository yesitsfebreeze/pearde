---
state: open
origin: requested
priority: 0
complexity: 0
blast-radius:
needs:
  - the-capability-registry
  - suggested-at-the-moment-of-need
---
---

# Usage snapshots, ranked over time

*Source: `docs/content/docs/improvements/integration-usage.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Layer:** rank · **Tool:** guard + scout's pattern · **Unblocked by:**
[the registry](/docs/improvements/integration-registry),
[the suggestion](/docs/improvements/integration-suggest)

## Why now

"Every tool used to its best capability" is a claim with no measurement
behind it. The guard already counts calls — the view's analytics section
renders calls per transition and refusals per session, both off the guard's
count, and the count is the named proxy for spend. But the count is kept
**per transition**, rolling thirty — a verb nobody has called in a month
reads as *no data*, not as *dead capability*. An unused capability is
invisible in every ranking the repo keeps: health scores files, scout ranks
other people's tools, and our own verbs are counted only to answer "what
did this transition cost".

## The change

One snapshot per day, in the board's shared dir beside the scout snapshots
it copies: `usage/<date>.tsv` — one row per registry verb, the guard's
count for the day, suggestion-taken / suggestion-ignored columns included
once the injector exists. `pearde capabilities delta [days]` diffs two
snapshots — the exact mechanics scout's delta already proves — and the
report page gains the ranking: verbs with zero calls in the window, **the
capability page that never happened, worst first**. The docs site's
improvement pages are the *response* mechanism: an unused verb is either
promoted (suggested where it applies), retired (its tool was wrong), or
renamed (it exists but nobody can find it — the fire check's job).

## Done when

- Two consecutive days of a working board produce two TSVs, and `delta 1`
  prints per-verb movement — same output shape as scout's star delta.
- A verb with zero calls across the window is named in the ranking with its
  registry row beside it — the reviewer sees the verb *and* its contract in
  one line.
- Snapshots are pruned to a cap (`SCOUT_SNAP_KEEP`'s twin), so the ranking
  grows no forever-file.

## Fails when

- The ranking punishes verbs whose *moment* rarely comes — `pearde vault`
  runs once a month and is fine. Guard: the ranking is **per capability,
  per opportunity** — the injector already knows how often a row was
  applicable (its suggestion count), so the ranking divides calls by
  suggestions, naming verbs that were *suggestible and never taken* over
  verbs that were never applicable at all.

## What stays out

No auto-retirement, no auto-promotion — the ranking names, the way health's
score points and never verdicts. Whether a verb is fixed is the board's
call, and this page only makes the case visible enough to be made.

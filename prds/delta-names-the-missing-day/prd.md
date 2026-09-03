---
state: done
origin: requested
priority: 42
complexity: 15
blast-radius: low
workflow: probe-then-spec
commit: 6578857
---

# delta names the missing day

*Source: `docs/content/docs/improvements/scout-delta-gap.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** scout · **Axis:** reliability (6 → 7) · **Pulls the score up by
~3 points**

## Why now

`delta [days]` diffs our own snapshots — today's count against the TSV from
~N days ago. When a machine was off, a cron gap ate a day, or the sweep
failed silently, the older TSV is further back than asked — and the delta
reports a bigger movement than happened. The output carries no signal that
the reference day is not the one asked for, so a quiet week reads as a
momentum spike, and the worst reading of the tool's output is the plausible
wrong one.

## The change

`delta` prints the window it actually used: `delta 7 · diffed against
2026-08-29 (4 days back, nearest to 7)`. When the nearest snapshot is
outside a tolerance (the window doubled or worse), the line reads `gap:
no snapshot within 2× of 7 days — run sweep first` and the delta table is
suppressed rather than printed on a stretched window. The `NEW` marker keeps
its meaning — it is about entering top-N, unaffected by the window's age.

## Done when

- A clean 90-snapshot history prints the exact reference date on every
  `delta` run.
- A tree with three snapshots, newest 20 days old, prints the `gap:` line
  and no rows, instead of a 20-day diff named as 7.
- The daily cron's first run after a machine's week off shows the gap line,
  then the sweep, then an honest delta.

## Fails when

- The tolerance silently swallows a legitimate long window — `delta 60` on
  a young tree (first sweep last week) must still diff against the oldest
  snapshot and say so, not refuse. The rule is *name the window*, never
  *narrow the window*.

## What stays out

No backfilling, no fetching history from the API — the stargazers
restriction is why self-diffing exists, and this page only makes the diff
honest about its own age.

## Blocked

**2026-09-03 20:41 — the lane will not rebase**

`lane/delta-names-the-missing-day` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/delta-names-the-missing-day` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock delta-names-the-missing-day`.

## Report

spec01: exit 0
spec01: all checks passed

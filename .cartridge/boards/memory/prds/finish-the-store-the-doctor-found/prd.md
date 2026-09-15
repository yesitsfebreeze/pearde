---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: blocked
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "2h"
---

# the format half closed itself when the build moved to v14 and the daemon's own flushes rewrote every row; 2,120 unkeyed thoughts, 290 dangling edges and 3 duplicate pairs remain, and every repair for them refuses under the daemon's writer lock

## Do

`memory doctor` on this repo's store, 2026-09-05 23:47, with the daemon up:

- `format_older_than_build` — rows are stored in v11 while the build writes v12
  and converts on read (`format-version`). Recall works; the store stays old
  until something writes it whole. `memory migrate` finishes it in one pass.
- `store_stale_identity` — 2120 thoughts are keyed by content alone, without the
  origin they came from. Recall is unaffected, but export/import and
  `memory hub merge` union on the id and would land one document as two.
  `memory rekey` is the named repair, and `inline-names-no-origin` is why the
  keying changed under them.
- `dangling_reasons` — 99 reason edges point at thoughts that no longer exist,
  weight every walk pays (`recall-pipeline`).
- `bare_labels` — 1 thought is a heading with no paragraph, retrievable as if it
  were a claim; the heading glue `session-names-no-origin` added is why there
  is one and not many.
- `near_duplicates` — 15 live pairs sit at or above the ingest dedup threshold,
  twins the gate let through; each folds into the older one.

**Re-measured 2026-09-06 05:07, daemon down, 80.5 s.** Two of the five numbers
above no longer hold and one finding is gone:

```
                        2026-09-05 23:47   2026-09-06 05:07
format_older_than_build  v11                v11
store_stale_identity     2120               2120
dangling_reasons         99                 1822
near_duplicates          15                 8
bare_labels              1                  absent
```

The v11 and 2120 figures are unchanged to the row, so nothing has written the
store whole and nothing has rekeyed. `dangling_reasons` is 18x the figure this
item was written against, having passed through 910 immediately after the bulk
forget ([the-forget-cascade-leaves-no-dangling-edge](../the-forget-cascade-leaves-no-dangling-edge/prd.md), whose fix landed
between these two readings and stops new ones from that path). What produced
the rest is not established here, and there are two candidates on the record:
the reap that takes a dead memory's reasons without counting them
(`the-reap-drops-edges-it-never-counts`), and a refused flush unioning disk
reasons back beside entities another writer removed
(`a-refused-flush-undoes-another-writers-removals`,
`memory-deletes-hard-and-merges-by-union`). A repair run should record the
count before and after so the next reading has a baseline that means something.

Three of the five carry repairs. The order matters: `memory migrate` first so the
rows are v12, then `memory rekey`, then
`memory doctor --json > manifest.json`, read the manifest, and
`memory repair manifest.json` for the dangling edges, the bare label and the
duplicate pairs. Repairs refuse while the writer lock is held
([[the-writer-lock-is-advisory-on-purpose]] — advisory on purpose, one holder
to name in the error), so this runs with the daemon stopped — and this
tree is shared, so say so before stopping it.

## Acceptance
`memory doctor` reports no `format_older_than_build`, no `store_stale_identity`,
and zero dangling reasons; the near-duplicate and bare-label counts are zero or
the manifest records why a pair was kept.

`memory repair` ran 2026-09-06 with the writer lock free and no daemon serving,
against a manifest read the same minute. Measured before and after by `memory
doctor`: `dangling_reasons` 1822 -> 1 and `near_duplicates` 8 -> 2, with the
command reporting "dropped 1822 dangling reason(s), reaped 0 empty memory(s),
folded 8 near-duplicate(s), retired 0 bare label(s)". The residue is arrivals
since the snapshot, not a partial repair — a daemon took the writer lock during
the check that followed, and the intake keeps draining.

`migrate` and `rekey` are untouched and are the larger half: `migrate` rewrites
every row to v12, and `rekey` changes 2,120 ids that export, import and `hub
merge` all key on (`cli-ingest-is-its-own-source`). Neither was run because
the repair is reversible in effect — the dropped edges pointed at nothing and
each folded pair kept its older row — and an id rewrite is not.

Numbers in a work part decay: this item was written with 99 dangling edges, read
1,774 an hour before the repair and 1,822 at it, because the intake drain is
still replaying a deleted worktree's captures
(`the-artifact-storm-collapsed-the-graph`). Re-measure before acting on the
two that remain rather than trusting these (`a-copied-fact-has-no-dissent`).

**Repaired again 2026-09-06 08:07**, by a [[quality]] pass, with the daemon
stopped through `memory hub unload` — this root only, no `pkill`. The doctor read
the same two counts with the daemon up (08:05) and down (08:07):

```
                        05:07 after repair   08:05   08:07 after repair
dangling_reasons         1                    56      0
near_duplicates          2                    2       0
format_older_than_build  v11                  v11     v11
store_stale_identity     2120                 2120    2120
```

The 56 grew in three hours with the cascade fix in place, so they came from
one of the two candidates named above and not from a forget. `migrate` and
`rekey` are still the open half; the v11 and 2,120 rows have not moved since
the item was written.

**Check read 2026-09-07 08:07, and it fails on all four clauses.** `memory
status` first: daemon "not serving this directory", writer lock "free" — so
this reading is the one the repairs would have run against, not a doctor
peering past a live writer. `memory doctor --json`:

```
                        08:07 2026-09-06 (after repair)   08:07 2026-09-07
format_older_than_build  v11                              v11
store_stale_identity     2120                             2120
dangling_reasons         0                                214
near_duplicates          0                                5
bare_labels              absent                           absent
```

`migrate` and `rekey` have still not run — v11 and 2,120 are unchanged to the
row across three days and four readings — and the two repairable counts have
regrown from zero in 24 hours, which is the same regrowth
(`the-reap-drops-edges-it-never-counts`,
`a-refused-flush-undoes-another-writers-removals`) this part already names and
neither candidate has been closed.

What blocks it is not the daemon. The writer lock was free at this reading, so
`memory migrate` and `memory rekey` could be typed right now; what stops them is
that `rekey` rewrites 2,120 ids in a shared store and is not reversible, and
the tree is shared with other sessions. That is a person's call, and this
sweep records it as one rather than re-picking it next pass
([[the-eight-unread-work-checks]]).

**Check read 2026-09-08 16:31, daemon up, and it now fails on two clauses
rather than four.** `memory doctor --json` against `/Users/feb/dev/memory/.memory`,
which reads the store directly and never asks the daemon
([[the-doctor-is-safe-only-because-it-never-asks-the-daemon]]), so a live
writer costs the reading nothing but its snapshot:

```
                        08:07 2026-09-07   16:31 2026-09-08
format_older_than_build  v11                absent
store_stale_identity     2120               2120
dangling_reasons         214                290
near_duplicates          5                  3
bare_labels              absent             absent
```

`format_older_than_build` is closed, and `memory migrate` did not close it. The
build's `FORMAT_VERSION` went to 14 on 2026-09-07 (`ef91d0d3`, the scoping
trio's deletion), a memory row is re-encoded at the current version the moment
something saves it, and the daemon has been saving all 221 memory rows since.
The doctor decodes every row on load and reports the oldest version byte it
saw; it saw none older than 14. So the half this item called the larger one
was retired by ordinary writing, and `migrate` on this store would now report
nothing to do. `store_stale_identity` sat at 2,120 across all five readings
because `rekey` is a content migration and no save performs it.

**Blocked, on two separate things.** `memory status` at this reading: writer
lock "held by daemon pid 22604", so `migrate`, `rekey` and `repair` all refuse
([[the-writer-lock-is-advisory-on-purpose]]), and the trunk is shared — the
session that would clear the lock is not the session that owns the daemon.
Clearing it is one person's call; accepting an irreversible rewrite of 2,120
ids in a store other sessions are writing is another, and neither is an
agent's to take. The repair half is cheap once the lock is free; the `rekey`
half is not, and it is the one that has never moved.

The same reading turned up three findings this item does not cover and does
not claim: `data_mdb_bloated` (data.mdb at 974 MiB, which the next daemon boot
self-heals), `vectorless_entities` (63 thoughts with no embedding, invisible to
dense search), and `empty_memories` (1). They are somebody's new work memos, not
this one's scope.

---
kind: work
level: 10
status: done
estimate: 4h
actual: 2h
description: a lane daemon's cold boot over a cloned record is four full DiskANN reconciles and not a compaction — `MEMORY_SKIP_SELF_HEAL` drops two of them and an unchanged spill threshold drops a third, taking the socket from 290 s to 82 s
read_when: "starting a daemon in a lane, or blaming a compaction for a slow boot"
---

# a-lane-daemon-pays-twelve-minutes-to-open-its-eyes

Measured 2026-09-09 on a `cp -c` clone of the record (`data.mdb` 974 MiB,
`diskann/` 429 MiB, 222 memories / 27,404 thoughts / 142,222 reasons), release
build, own store and own socket, the trunk daemon untouched. The clone itself
is free: 16–20 ms and zero bytes for `data.mdb` and the index together, so
lever one was never the cost.

**The compaction is not the cost, and it is not what invalidates the index.**
`store_core::compact_dir` took ~1.2 s to write 974 MiB down to 229. And the
very first `open_snapshot`, *before* any compaction ran, already read
`snapshot_epoch=22425` against `store_epoch=40631`: the record's on-disk
DiskANN snapshot is eighteen thousand epochs behind its own `data.mdb`,
because a running daemon folds new vectors into its in-RAM delta and nothing
rewrites the snapshot. A clone is stale on arrival, with or without self-heal.

**The cost is that `rebuild_index` runs four times before the socket binds**,
each one 66–81 s, and 60–71 s of each is the reason index reconciling 42.5 k
vectors into the delta overlay (snapshot 79,988 ids, `arm="delta"`). Twice
because one `load_graph` rebuilds twice — once inside `from_saved_with_mode`
at threshold 0, once in `apply_graph_config`, which re-applied the *same*
configured threshold 0 and rebuilt everything the load had just built — and
twice over because `maybe_self_heal_store` loads a whole throwaway graph to
reap empty memories before it compacts. It is the same `reconcile_disk → insert`
loop [[@prd/work/memory--a-killed-daemon-pays-a-full-index-rebuild.md]] watched burn ten minutes at
98% CPU, and the load phase [[every-cli-invocation-pays-a-minute]] could not
decompose.

| boot, fresh clone, to the socket | |
|---|---|
| before, self-heal on | 290.4 s — 4 × rebuild_index (81 + 69 + 66 + 66 s), compaction 1.2 s |
| after, `MEMORY_SKIP_SELF_HEAL=1` | 82.5 s — 1 × rebuild_index (78.4 s), `apply_graph_config` 0 ms |
| after, no flag, dirty store | 201.8 s — `self-heal compacted data.mdb 974 MiB -> 229 MiB` |

Both daemons report 222 memories / 27,404 thoughts / 142,222 reasons off the same
clone, so the skip loses nothing. The `memory health` that prints those counts
still pays its own load beside the daemon it just asked —
[[@prd/work/memory--memory-health-loads-its-own-graph-beside-the-daemon.md]] is that defect, found
here and not fixed here.

## Do

Landed: `MEMORY_SKIP_SELF_HEAL` (any value but empty or `0`) returns from
`maybe_self_heal_store` before it reads `data.mdb`, and `apply_graph_config`
returns without rebuilding when the configured spill threshold is the one the
indexes were already built at. The variable is opt-in and never a default — a
daemon that opens a store nobody handed it sees nothing set and self-heals as
before, proved by the third row above. The threshold guard is not lane-only:
every daemon boot and every graph-loading CLI call paid that duplicate.

## Check

Ran 2026-09-09, both timings in the table above. A lane daemon on a freshly
cloned `.memory/` binds its socket in 82.5 s with the source store's counts, and
an unflagged daemon on the same clone still compacts 974 MiB to 229.
`cargo nextest run -p commands -p graph -p bootstrap -p store`: 308 passed,
with `apply_graph_config_spills_to_disk_when_threshold_enabled` failing when
the new guard is removed and passing with it.

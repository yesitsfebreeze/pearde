---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the graph load costs about a minute per CLI invocation and emits no trace, so name the phases before anyone proposes a fix

## Do

`every-cli-invocation-pays-a-minute` measured the cost and could not
decompose it: `RUST_LOG=debug memory list` emits one line, about reaped LMDB
reader slots, for 63 seconds of work.

Put a span or a timed log line around each phase of the load in
`bootstrap::load_graph` and `GraphGnn::open_snapshot`: the LMDB scan and decode,
the per-memory entity/reason decode, `open_snapshot` per index (entity, gnn,
reason) with which arm it took — fresh, stale-and-reconciled, or full rebuild —
and the reconcile's item count. Use the `memory.diskann` target that already
exists for the warnings there.

Do not change behaviour in this item. The next reader needs to know whether the
minute is decode, reconcile or Vamana build; proposing a fix before that is the
error `health-is-quadratic-in-entity-count` made, attributing a measured 51 s
to the only quadratic in sight.

Worth checking while there, because it is the cheap hypothesis
`every-cli-invocation-pays-a-minute` names and does not test: a CLI invocation
never writes a refreshed snapshot back, so if the stale path is what costs, every
invocation pays the same reconcile forever and one write would end it.

Wanted: a reader who has not formed a hypothesis. Two sessions declined it on
2026-09-06 for that reason — one seventeen items deep and expecting the stale
snapshot, and the author of `every-cli-invocation-pays-a-minute`, who wrote
that hypothesis down and is the worst reader for it. Instrument every phase
uniformly, not the suspected one, so the spans can say the suspicion is wrong.

## Acceptance
`RUST_LOG=info memory list` names each phase with its duration, the three indexes
are distinguishable, and the arm `open_snapshot` took is in the output. `just
all` green.

Landed 2026-09-06 on branch `worktree-agent-a85691e7482ae3921` (commit
`6c202439`, on top of `825925fb`), blocked on the merge into `main` because
`src/graph/src/graph.rs` and `src/store_core/src/lib.rs` sit uncommitted in the
shared tree under a session no longer live. One `info` line per phase —
`memory.store` for the LMDB scan and the per-memory decode, `memory.diskann` for item
collection, each `open_snapshot` (subdir, arm, both epochs), the reverse-map
fill, each `reconcile` (arm, snapshot size, deleted, inserted, diff time) and
the lexical rebuild, `memory.persist` for the three steps of `load_graph`. What a
debug-build `list` against the 331 MB store (83 memories, 12,907 entities, 29,943
reasons, store epoch 6683 against snapshot epoch 5930) said, 107 s wall: LMDB
scan and row decode 4.0 s, vector decode 0.3 s, items collected 0.05 s, all
three `open_snapshot` stale-and-reconciled in 11 / 0 / 21 ms, reverse maps
85 ms, reconcile entity `delta` 9.5 s (11,475 in the snapshot, 62 deleted, 825
inserted, the diff itself 0.4 s), gnn 0 ms over an empty snapshot, reconcile
reason `delta` 43.3 s (22,427 in the snapshot, 2,951 inserted, the diff 0.9 s),
lexical 2.9 s — and then `apply_graph_config` runs `rebuild_index` a second
time and pays the whole reconcile again, 46.4 s, because `from_saved_with_mode`
already ran it once with no store bound, so `store_epoch` reads as absent there
and nothing can ever be fresh on that first pass. The minute is neither decode
nor the diff: it is 3,776 HNSW inserts into the delta overlay at ~12 ms each,
paid twice. The cheap hypothesis holds: the three `epoch` files kept their
09:19 mtime across two runs at 09:39 and 09:41, so a CLI invocation never
writes a refreshed snapshot back and every invocation reconciles the same
3,776 items.

Merged into `main` 2026-09-06 as `5c3d28d5`, cleanly, once the two dirty
files it touched were committed by their own sessions.

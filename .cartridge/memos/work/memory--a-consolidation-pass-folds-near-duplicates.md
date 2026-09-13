---
kind: work
level: 10
status: done
description: one operator pass lays a `Ratification` edge between near-duplicate rows across origins — the same-origin fold it was first written to add already stands, unrun, in `memory doctor --repair`
read_when: "executing the convergence plan"
---

# a-consolidation-pass-folds-near-duplicates

The first child of [[@prd/work/memory--the-graph-converges.md]]. Blocked until
`does-a-merge-cross-origins` is answered — every `Q:` in it changes what this
item writes, and two of them change whether it is a fold at all.

## Do

`graph::accept::merge_duplicate` already folds one entity into another: text,
confidence evidence, TTL, and a `rephrase_id` that drives supersede. Its only
production caller is `ingest_dedup.rs:51`. Give it a second one that runs over
the store rather than over one arrival.

For each resident memory, search each entity's vector against the entity index
and fold hits above the merge threshold. The filtered walk this needs already
exists — `hnsw::beam_search_filtered` admits every visited node to the frontier
and only keep-matches to the result heap, which is what let the ingest gate
reach a survivor at rank 201 (`filtered-search-termination`); the predicate
here is whatever `does-a-merge-cross-origins` settles, not `same_origin`.

Two properties the pass must hold, both learnable from the ingest gate's
history: a fold is not symmetric, so the survivor must be chosen by a stated
rule and not by iteration order; and a pass that folds A into B and then B into
C in one run must not leave an edge pointing at B.

Where it runs is the last `Q:` of the question part — a `TaskKind`, or a verb
beside `gc` and `rekey` that takes the writer lock. If it becomes a task it
must be ranked above the LLM tasks in
[[@prd/work/memory--maintenance-survives-a-saturated-queue.md]], or it is shed exactly when it is
needed.

## Check

Ingest the record twice from a cold store — once as `memos/`, once as a copy
under a second path, so every claim arrives twice under a different origin.
Before the pass the thought count is double; after one run it is within 5% of a
single ingest, `memory doctor` reports no dangling edges, and `memory query` on a
claim that existed in both copies returns one entity whose provenance names the
survivor rule's winner.

**Unblocked 2026-09-07, and the `Do` above is superseded.** The block named
`does-a-merge-cross-origins`, which has been `kind: decision`, `status: decided`
and dated 2026-09-06 since before the block was last read, so the block was
stale on its face. Two things follow, both measured in
[[the-convergence-block-outlived-its-question]].

The fold this part describes is already in the tree. `graph::accept::fold_into`
(`src/graph/src/accept.rs:297`) is the second production caller of
`merge_duplicate` the `Do` asks for, reached from `commands_doctor.rs:429`;
`near_duplicates` (`commands_doctor.rs:282`) is the whole-store walk, at each
kind's `dedup_threshold`, skipping pairs whose `Source::origin_id` differ, with
the survivor picked by a stated rule — oldest keeps the id, ties to the smaller
id — which is the non-symmetry the `Do` warns about. It is an operator verb
under the writer lock, and it has never been run: the store read 12,070 thoughts
on 2026-09-06 and reads 20,615 today.

So what is left is only the half the decision chose over the fold: `memory
consolidate`, beside `gc` and `rekey`, laying a `Ratification` edge between two
near-duplicate rows that keep their own `source` — origin-blind, one k=1
filtered nearest search per resident entity under the 4,096-visit budget
([[filtered-search-termination]]), one config key beside `dedup_threshold`, and
a count of new edges only, since `reason_id` is content-addressed.
`ReasonKind::Ratification` (`base_types.rs:103`) has no production minter today;
every reference outside `base_types.rs` is a test. Nothing here folds, so the
`Check` below is wrong too: the count after a run is unchanged, and what is
proved is that a claim ingested twice under two origins comes back as two rows
joined by one `Ratification` reason, with `memory doctor` reporting no dangling
edges.

**Done 2026-09-07.** `memory consolidate` stands beside `gc` and `rekey`
(`Commands::Consolidate`, `commands_admin::cmd_consolidate`), takes the writer
lock, and calls `graph::accept::ratify_near_duplicates` — one k=1 filtered
nearest search per live vectored entity, origin-blind, pairs collected before
any edge is written and oriented oldest-first with ties to the smaller id, so
the two ends of a pair mint one content-addressed `Ratification` id instead of
two. The threshold is `[ingest] ratify_threshold`, beside `dedup_threshold` and
defaulting to it, and the run prints a count of new edges only.
`ReasonKind::Ratification` has a production minter for the first time. The
rewritten `Check` ran as
`consolidate_joins_two_origins_and_folds_nothing`
(`tests/e2e/near_duplicates.rs`): one claim dropped into the intake as two
files is two rows under two origins, one run lays one edge, the row ids and
count are unchanged, `memory get` reads the edge from each end, a second run lays
nothing, and `memory doctor --json` reports no `dangling_reasons`.

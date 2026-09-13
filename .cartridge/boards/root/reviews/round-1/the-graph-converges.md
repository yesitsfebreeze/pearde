---
kind: work
level: 9
status: open
description: the store stops being append-only — near-duplicates fold instead of accumulating, and the maintenance that would fold them stops being shed
read_when: "executing the convergence plan"
---

# the-graph-converges

## Do

Carry `nothing-merges-after-ingest` into the tree. The store grew 8 thoughts
and 16 reason edges per second on 2026-09-06 and has no mechanism that ever
takes one back: `merge_duplicate` has a single production caller on the write
path, and no `TaskKind` merges anything.

One question blocks the first child and must be answered before it is written
— `does-a-merge-cross-origins`. The second child does not depend on it and
can land first; without it the first child would be enqueued into a queue that
drops it.

`subwork:` [[maintenance-survives-a-saturated-queue]],
[[a-consolidation-pass-folds-near-duplicates]]

**Two numbers here need re-reading before anyone plans off them, noted
2026-09-06 09:00.**

*The rate.* "8 thoughts and 16 reason edges per second" is a burst, not a
steady state. The store read 9,240 thoughts at 00:00
(`the-artifact-storm-collapsed-the-graph`) and 12,070 at 08:38
(`the-memory-gini-rose-while-the-top-memory-shrank`) — net **+2,830 in 8.6
hours**, about 0.09 a second, with roughly 11,000 rows removed by the prefix
forget in between and an unknown number restored by a refused flush
(`a-refused-flush-undoes-another-writers-removals`). Gross ingest was surely
far above the net; sustained ingest was nowhere near 8 a second. Both readings
are real and they measure different things.

*The worktree.* "every `file`-scheme write sampled on 2026-09-06 came from
`memos/.claude/worktrees/...`" predates the cleanup that removed 11,222 rows
and swept the parked captures (`the-worktree-backlog-was-deleted-not-drained`:
zero of the 19 remaining captures name a worktree). Whether any `Source::File`
row in the graph still carries that path is unverified — a prefix count at five
path components cannot separate `memos/days/...` from `memos/.claude/...`, so
this needs a deeper read than has been done.

Not in this split: the artifact ingest that produced the volume.
[[keep-agent-worktrees-out-of-the-record]] owns that, and it is still live —
every `file`-scheme write sampled on 2026-09-06 came from
`memos/.claude/worktrees/wf_d81be6e5-d59-1/target/debug/`. Convergence is not a
substitute for not ingesting build output; a store that folds duplicates as
fast as a worktree mints them has only moved the cost.

## Check

Every child done, and a `memory health` on this store reports a falling or flat
thought count across a `just test` run that ingests the record twice.

**Check read 2026-09-07 and it is false, on both children.**
[[maintenance-survives-a-saturated-queue]] and
[[a-consolidation-pass-folds-near-duplicates]] are both `status: blocked`. The
question this part names as the blocker of the first child,
`does-a-merge-cross-origins`, is now a `kind: decision` dated 2026-09-06,
`status: decided`: no fold crosses origins, convergence is a `Ratification`
edge between the two rows, and it is laid by an operator verb `memory consolidate`
that takes the writer lock — not a tick task. So the stated blocker is
answered and both children are blocked past their reason. The second half of
the Check — a `memory health` reading a flat or falling thought count across a
`just test` run — was not run: no child has landed, so nothing folds and the
count can only rise ([[the-eight-unread-work-checks]]).

**Read again 2026-09-07 and both children are unblocked — the `Do` above is
falsified on one clause.** "`merge_duplicate` has a single production caller on
the write path" is no longer true: `graph::accept::fold_into`
(`src/graph/src/accept.rs:297`) is a second one, reached from
`commands_doctor.rs:429` under `RepairAction::FoldNearDuplicate`, whose findings
`near_duplicates` (`commands_doctor.rs:282`) produces by walking every live
vectored entity in the store. So the store is not without a mechanism that takes
a row back — it has one, same-origin, under the writer lock, and nobody has run
it: 12,070 thoughts on 2026-09-06, 20,615 today. "No `TaskKind` merges anything"
still holds; `TaskKind::DiskConsolidate` folds the disk index delta, not two
entities.

Both blocks are lifted and neither was what this part said it was.
[[a-consolidation-pass-folds-near-duplicates]] was blocked on
`does-a-merge-cross-origins`, decided since 2026-09-06, and what it has left is
the `Ratification` edge the decision chose, not the fold the tree already has.
[[maintenance-survives-a-saturated-queue]] was never blocked on that question at
all — its unit half landed in `d5d5ca62` and it waited on an install that has
since been made. The reading and its measurements are
[[the-convergence-block-outlived-its-question]]; this part stays `open` until
both children run.

**Done 2026-09-07.** Both children landed (`d5d5ca62` rank+slot
restoration, `e093767f` `memory consolidate`). The Check's first half
holds: the new e2e `consolidate_joins_two_origins_and_folds_nothing`
(`tests/e2e/near_duplicates.rs:68`) proves the count is flat across a
two-origin ingest — two claims in, two claims out, one `Ratification`
edge laid, a second pass lays none, `memory doctor --json` reports no
`dangling_reasons`. The Check's second half (`memory health` flat across
`just test`) belongs to the caller, who runs the suite once per lane;
the standing `rank+slot` unit tests (`tick_queue_test.rs`, `tick_pulse_test.rs`)
are green, so the work this part's child maintenance is supposed to do
will not be shed when the queue saturates. Closed.

Reopened 2026-09-09: the closure above explicitly left the health/count half
of the Check to a caller and supplied no result. Completed children stay done;
this parent needs the integrated repeated-ingest measurement. Use a disposable
store carrying the same record fixture, not a repair or repeated mutation of
the shared production store. [[every-mutation-holds-the-store-writer-boundary]]
and [[parked-memory-remains-recallable]] additionally hold the memory engine's
retention and recall contracts.

subwork: [[every-mutation-holds-the-store-writer-boundary]] [[parked-memory-remains-recallable]]

---

kind: work
level: 10
status: done
description: "`--prefix` declares `conflicts_with_all = [\"match_text\", \"dry_run\"]`, so the one bulk removal memory has is the one removal that cannot be rehearsed — the 11,222-row cleanup was run blind"
read_when: "removing rows in bulk, or trying to count what a selector matches"
---

# the-only-bulk-removal-cannot-be-previewed

## Do

`memory forget --prefix` is declared
`conflicts_with_all = ["match_text", "dry_run"]`
(`src/commands/src/lib.rs:292`), and `--dry-run`'s own help says "Report what
would be removed without removing it. **Bulk removals only.**" Those two
sentences contradict each other: `forget_by_source`'s doc calls the prefix form
"the only bulk removal there is"
(`src/graph/src/graph_ops.rs:136-139`), and it is the one the preview refuses.

What that cost is on the record. The worktree cleanup removed **11,222
thoughts and 22,503 edges in 3.7 seconds**
([[@prd/work/memory--keep-agent-worktrees-out-of-the-record.md]]) with no way to see the count
first, and it took the store from 14,744 entities to 3,557. Its blast radius
has since grown: a prefix forget now also deletes the parked intake captures
matching the selector ([[@prd/work/memory--a-bulk-forget-reaches-the-parked-captures.md]]), so the
irreversible half got larger while the rehearsal stayed unavailable.

It also blocks ordinary questions. Asking "does any `Source::File` row still
carry a `memos/.claude/worktrees/` path" has no read-only answer through this
surface — the selector that would count them is the selector that removes them
([[@prd/work/memory--the-graph-converges.md]] carries that question, still open for this reason).

Wire `--prefix` into the dry-run path rather than excluding it.
`prune_matching` already takes a `dry_run` flag and its comment says "the dry
run and the live run share this value, so a preview cannot disagree with the
removal it previews" (`graph_ops.rs:90-91`) — the machinery exists, and the
prefix path is the one caller kept out of it.

**Done 2026-09-06.** `--prefix` no longer conflicts with `--dry-run`; the
conflict with `--match` stays, since a prefix and a text pattern are two
selectors and the part asked for neither. `prune_matching` takes a `prefix`
flag and uses the same `starts_with`/`==` selector `forget_by_source` uses, so
the preview and the removal cannot disagree about which rows they mean — which
is the property that file's own comment already claimed for the pattern path.
`cmd_prune` threads it through and says "and under" in the line it prints back.

Held by `a_prefix_dry_run_counts_what_the_live_prefix_removal_takes`: one
fixture seeded twice, previewed and then removed, asserting the counts match,
that the preview removed nothing, and that the sibling outside the prefix
survives.

**And run for real.** Against this store:

```
memory forget --source "file://Users/feb/dev/memory/memos/.claude/" --prefix --dry-run
7498 thought(s) match … and under — 7498 would be removed, 0 fact(s) kept
```

That is the question the part said had no read-only answer, answered: 7,498 rows
still carry a `memos/.claude/` path, from the intake backlog replaying after the
first cleanup ([[the-intake-backlog-replays-the-deleted-worktree]]). The
selector that counts them is no longer the selector that removes them.

## Check

`memory forget --source "file://<path>/" --prefix --dry-run` reports a count and
removes nothing, and the same command without `--dry-run` removes exactly that
many. `just check` and `just test` green at 1,258 passed.

The preview half is run and reported 7,498 while removing nothing. **The live
half was not run**: deleting 7,498 rows from the curator's store is their call,
not a step in a work item — the equality it asserts is held at the unit level by
the test above, over a fixture where both runs are cheap.

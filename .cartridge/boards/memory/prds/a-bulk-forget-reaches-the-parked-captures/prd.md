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

# `forget --source` empties the graph of a source and leaves that source's parked intake captures untouched, so the next drain re-ingests exactly what was removed

## Do

`the-intake-backlog-replays-the-deleted-worktree` measured the hole: 948 of
4,204 captures in `.memory/intake/direct/` carry `.claude/worktrees` paths, and a
prefix forget that removed 11,222 thoughts left every one of them queued. The
operation says "remove every thought from one source" and removes only the ones
that have already landed.

`cmd_forget_source` (`src/commands/src/commands_graph_ops.rs`) sweeps the intake
before it routes the graph removal — before, so a drain running concurrently
cannot re-park what the graph is about to lose. Each capture is a serialized
`DirectJob` whose `source` field deserializes as `base::base_types::Source`, so
the match is `scheme()` and `object_id()` against the same selector the graph
half uses, prefix included, rather than a second opinion about paths. The
count joins the printed line. The daemon is not involved: the intake is a
directory the CLI can read, `rpc` has no business knowing where it lives, and
`memory forget` already runs in the caller's own process for everything else it
does to disk.

**Done 2026-09-06.** `cmd_forget_source` calls `forget_intake_captures`
(`src/commands/src/commands_graph_ops.rs`) before it routes, printing the count
on its own line when it is not zero. The sweep itself is
`intake_capture_sweep`, taking the directory as an argument so a test can hand
it a temp one. What it does not reach is `direct/done/`: a drained capture is
archived there and `prune_done` is the only thing that removes it, so a forget
leaves an archive of exactly what it removed — harmless while nothing replays
`done/`, and worth knowing before anything does.

## Acceptance
`just test` green, plus a unit test: a temp directory holding two parked
captures, one under the selector and one not, keeps exactly the one outside it
after the sweep. Held by
`a_source_forget_drops_the_parked_captures_under_the_same_prefix`
(`src/commands/src/tests/commands_graph_ops_test.rs`); the suite read 1,229
passed.

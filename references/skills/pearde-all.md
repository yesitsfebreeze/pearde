---
name: pearde-all
description: Every board this machine watches merged into one dependency-ordered frontier — what to work next across all of them, cut into the waves that could run at once, with the load-derived slot count and the reading that produced it. Runs from any directory; there need be no board above the cwd. Takes a group as a bare word — `pearde machine work` is the same read over the boards declaring `groups: work` in their own settings. The default mode prints and moves nothing; `machine dispatch` is the one verb that runs that frontier down, launching a pass worker per row. Use for "/pearde-all", "/all", "dispatch the machine", "run every board at once", "work the all board", "work every board", "all my projects at once", "what should the machine do next", "the machine frontier", "what can run in parallel right now", "how many workers should I run", "one plan over every board", "what is ready across all my repos", "just the work projects", "only my private repos", "group these boards", "which group is this board in", "run the work group".
---

Read @references/parts/machine.md — it is the contract: what is merged and
what is deliberately not, what each mark means, how a wave is cut, how the
slot count is derived and why it is never printed without its reading. The
scopes are `@@machine`, `@@all` and `@@settings`.

```bash
python3 @resources/pearde.py machine            # the frontier, the waves, and the reading
python3 @resources/pearde.py machine boards     # what the daemon watches, and each board's cap
python3 @resources/pearde.py machine slots      # the concurrency and the numbers behind it
python3 @resources/pearde.py machine progress   # one progress line over the merged set
python3 @resources/pearde.py machine groups     # the labels the watched boards declare, and who holds them
python3 @resources/pearde.py machine dispatch   # run that frontier down — the one verb that moves

python3 @resources/pearde.py machine work           # the same read over one group
python3 @resources/pearde.py machine work dispatch  # that group run down
```

`machine --json` is the same read as data — `boards`, `rows`, `slots`,
`reading`, `demand`, `group`, `groups`, `waves`, `skipped`, `notes`.

**A group is a label a board writes on itself**, `groups: work infra` in its
own `.pearde/settings.md`, set with `pearde settings groups=work` standing in
that board. Any verb takes it, in either order — `machine work slots`,
`machine work dispatch`. Labels, not a partition: a board may carry several
and most carry none, so `work` and `private` are two labels among any others.
Nothing keeps the list; the board declares itself, the same way the watch set
is the whole configuration. A group no watched board declares is refused by
name rather than answered with an empty frontier. `## Groups` in
@references/parts/machine.md is the contract; the `all` page has no group
filter and renders the whole watch set.

**The default mode reads. It does not move.** No claim, no transition, no
dispatch, no write to any board, any PRD or any settings file. It answers
*what should the machine do next*, and stops there — a person must be able to
look at the whole machine without the looking starting anything.

**`machine dispatch` is the verb that moves**, and moving it is something you
type. It keeps a rolling pool `slots()` wide, starts a queued row when a slot
is free and nothing in flight clashes with its real-path footprint, re-asks
`claim`'s own gate at each launch and prints `skip <addr> · <reason>` for every
refusal, and treats a launch as a worker only once it has survived a grace
window with no `API Error` in its run log — a 402 is a process that starts and
dies, and it is re-dispatched once and then named. `--dry` prints what it would
launch and starts nothing; `--once`, `--workers N`, `--adapter <id>` and
`--deadline S` are the rest. It writes no board's `settings.md`, adds no write
door to `all`, and keeps no registry. @references/parts/machine.md's
`## Dispatch` is the contract.

Two things it will not tell you, and both are by design. A board nobody
watches is invisible — the watch set is the whole configuration, and there is
no registry written here (@references/parts/all.md says the same of its own
merge: *a member nobody watches is not one of them*). And the slot count is a
reading of the local machine, which is a proxy: run `pearde view` on a board
first if it is missing, and read the count beside its numbers rather than
instead of them.

---
name: pearde-all
description: Every board this machine watches merged into one dependency-ordered frontier — what to work next across all of them, cut into the waves able to run at once, with the load-derived slot count and its reading. Runs from any directory, with no board above the cwd. Takes a group as a bare word: `pearde plan work` reads the same over boards declaring `groups: work` in their own settings. `plan` prints and moves nothing; `pearde run` runs the frontier down, launching a pass worker per row. Use for "/pearde-all", "/all", "dispatch the machine", "run every board at once", "work the all board", "work every board", "all my projects at once", "what should the machine do next", "the machine frontier", "what can run in parallel right now", "how many workers should I run", "one plan over every board", "what is ready across all my repos", "just the work projects", "only my private repos", "group these boards", "which group is this board in", "run the work group".
---

Read @references/parts/run.md — the contract: what is merged and what is
deliberately not, what each mark means, how a wave is cut, how the slot count
is derived, and why the count is never printed without its reading. The scopes are
`@@run`, `@@all` and `@@settings`.

```bash
python3 @resources/pearde.py plan all           # the frontier, the waves, and the reading
python3 @resources/pearde.py plan boards        # what the daemon watches, and each board's cap
python3 @resources/pearde.py plan slots         # the concurrency and the numbers behind it
python3 @resources/pearde.py plan progress      # one progress line over the merged set
python3 @resources/pearde.py plan groups        # the labels the watched boards declare, and who holds them
python3 @resources/pearde.py run all            # run that frontier down — the command that moves

python3 @resources/pearde.py plan work          # the same read over one group
python3 @resources/pearde.py run work           # that group run down
```

`plan all --json` is the same read as data — `boards`, `rows`, `slots`,
`reading`, `demand`, `group`, `groups`, `waves`, `skipped`, `notes`.

**A group is a label a board writes on itself** — `groups: work infra` in its
own `.pearde/settings.md`, set with `pearde settings groups=work` standing in
that board. Any window takes one, in either order: `plan work slots`,
`plan slots work`. Labels, not a partition — a board may carry several,
most carry none, and `work` and `private` are two labels among any others. No
list is kept anywhere; the board declares itself, the way the watch set is the
whole configuration. A group no watched board declares is refused by name
rather than answered with an empty frontier. `## Groups` in
@references/parts/run.md is the contract; the `all` page takes no group
filter and renders the whole watch set.

**`plan` reads. It does not move.** No claim, no transition, no
dispatch, no write to any board, PRD or settings file. The answer is *what
should the machine do next*, and nothing follows it — a person must be able to
look at the whole machine without the looking starting anything.

**`run` is the command that moves**, and moving is something you type. `run`
keeps a rolling pool `slots()` wide, starts a queued row when a slot is free
and nothing in flight clashes with its real-path footprint, re-asks `claim`'s
own gate at each launch, and prints `skip <addr> · <reason>` for every
refusal. A launch counts as a worker only after a grace window with no
`API Error` in its run log — a 402 is a process that starts and dies, so the
row is re-dispatched once and then named. `--dry` prints what would launch and
starts nothing; `--once`, `--workers N`, `--adapter <id>` and `--deadline S`
are the rest. `run` writes no board's `settings.md`, adds no write door to
`all`, and keeps no registry. `## Dispatch` in @references/parts/run.md is the
contract.

Two silences, both by design. A board nobody watches is invisible — the watch
set is the whole configuration, and no registry is written here
(@references/parts/all.md says the same of its own merge: *a member nobody
watches is not one of them*). And the slot count is a reading of the local
machine, so a proxy: run `pearde view` on a board first when the count is
missing, and read the number beside its reading rather than instead of it.

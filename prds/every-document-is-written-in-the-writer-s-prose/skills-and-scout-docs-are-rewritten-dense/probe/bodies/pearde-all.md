
Read @references/parts/machine.md — the contract: what is merged and what is
deliberately not, what each mark means, how a wave is cut, how the slot count
is derived, and why the count is never printed without its reading. The scopes are
`@@machine`, `@@all` and `@@settings`.

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

**A group is a label a board writes on itself** — `groups: work infra` in its
own `.pearde/settings.md`, set with `pearde settings groups=work` standing in
that board. Any verb takes one, in either order: `machine work slots`,
`machine work dispatch`. Labels, not a partition — a board may carry several,
most carry none, and `work` and `private` are two labels among any others. No
list is kept anywhere; the board declares itself, the way the watch set is the
whole configuration. A group no watched board declares is refused by name
rather than answered with an empty frontier. `## Groups` in
@references/parts/machine.md is the contract; the `all` page takes no group
filter and renders the whole watch set.

**The default mode reads. It does not move.** No claim, no transition, no
dispatch, no write to any board, PRD or settings file. The answer is *what
should the machine do next*, and nothing follows it — a person must be able to
look at the whole machine without the looking starting anything.

**`machine dispatch` is the verb that moves**, and moving is something you
type. Dispatch keeps a rolling pool `slots()` wide, starts a queued row when a
slot is free and nothing in flight clashes with its real-path footprint,
re-asks `claim`'s own gate at each launch, and prints `skip <addr> · <reason>`
for every refusal. A launch counts as a worker only after a grace window with
no `API Error` in its run log — a 402 is a process that starts and dies, so
the row is re-dispatched once and then named. `--dry` prints what would launch
and starts nothing; `--once`, `--workers N`, `--adapter <id>` and `--deadline
S` are the rest. Dispatch writes no board's `settings.md`, adds no write door
to `all`, and keeps no registry. `## Dispatch` in
@references/parts/machine.md is the contract.

Two silences, both by design. A board nobody watches is invisible — the watch
set is the whole configuration, and no registry is written here
(@references/parts/all.md says the same of its own merge: *a member nobody
watches is not one of them*). And the slot count is a reading of the local
machine, so a proxy: run `pearde view` on a board first when the count is
missing, and read the number beside its reading rather than instead of it.

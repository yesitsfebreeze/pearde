---
name: pearde-machine
description: Every board this machine watches merged into one dependency-ordered frontier — what to work next across all of them, cut into the waves able to run at once, with the load-derived slot count and its reading. Runs from any directory, with no board above the cwd. The read prints and moves nothing. Use for "/machine", "work every board", "all my projects at once", "what should the machine do next", "the machine frontier", "what can run in parallel right now", "how many workers should I run", "one plan over every board", "what is ready across all my repos".
---

Read @references/parts/machine.md — the contract: what is merged and what is
deliberately not, what each mark means, how a wave is cut, how the slot count
is derived, and why the count is never printed without its reading. The scopes are
`@@machine`, `@@all` and `@@settings`.

```bash
python3 @resources/pearde.py machine            # the frontier, the waves, and the reading
python3 @resources/pearde.py machine boards     # what the daemon watches, and each board's cap
python3 @resources/pearde.py machine slots      # the concurrency and the numbers behind it
python3 @resources/pearde.py machine progress   # one progress line over the merged set
```

`machine --json` is the same read as data — `boards`, `rows`, `slots`,
`reading`, `demand`, `waves`, `skipped`, `notes`.

**This command reads. It does not move.** No claim, no transition, no
dispatch, no write to any board, PRD or settings file. The answer is *what
should the machine do next*, and nothing follows it. Dispatching the waves
drawn is the PRD `the-machine-frontier-is-dispatched-in-parallel`, a separate
unit on purpose: a person must be able to look at the whole machine without
the looking starting anything.

Two silences, both by design. A board nobody watches is invisible — the watch
set is the whole configuration, and no registry is written here
(@references/parts/all.md says the same of its own merge: *a member nobody
watches is not one of them*). And the slot count is a reading of the local
machine, so a proxy: run `pearde view` on a board first when the count is
missing, and read the number beside its reading rather than instead of it.

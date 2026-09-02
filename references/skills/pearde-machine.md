---
name: pearde-machine
description: Every board this machine watches merged into one dependency-ordered frontier — what to work next across all of them, cut into the waves that could run at once, with the load-derived slot count and the reading that produced it. Runs from any directory; there need be no board above the cwd. It prints and moves nothing. Use for "/machine", "work every board", "all my projects at once", "what should the machine do next", "the machine frontier", "what can run in parallel right now", "how many workers should I run", "one plan over every board", "what is ready across all my repos".
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
```

`machine --json` is the same read as data — `boards`, `rows`, `slots`,
`reading`, `demand`, `waves`, `skipped`, `notes`.

**This command reads. It does not move.** No claim, no transition, no
dispatch, no write to any board, any PRD or any settings file. It answers
*what should the machine do next*, and stops there. Dispatching the waves it
draws is the PRD `the-machine-frontier-is-dispatched-in-parallel`, and it is a
separate unit on purpose: a person must be able to look at the whole machine
without the looking starting anything.

Two things it will not tell you, and both are by design. A board nobody
watches is invisible — the watch set is the whole configuration, and there is
no registry written here (@references/parts/all.md says the same of its own
merge: *a member nobody watches is not one of them*). And the slot count is a
reading of the local machine, which is a proxy: run `pearde view` on a board
first if it is missing, and read the count beside its numbers rather than
instead of them.

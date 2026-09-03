---
name: pearde-run
description: Dispatch a board, a group of boards, or every board this machine watches — the one command that moves. `pearde run` works the board at the cwd, `pearde run all` every watched board, `pearde run <group>` a labelled group, `pearde run <prd>` the loop over one subtree. Use for "/run", "run the board", "dispatch the machine", "run the work group", "run this PRD to done", "launch the workers".
---

Read @references/parts/run.md — the contract: how a bare word resolves, what
a scope narrows, how a wave is cut, how the slot count is derived, and why the
count is never printed without its reading. The scopes are `@@run`, `@@all`
and `@@settings`.

```bash
python3 @resources/pearde.py run                # the board at the cwd
python3 @resources/pearde.py run here           # the same, said out loud
python3 @resources/pearde.py run all            # every board the daemon watches
python3 @resources/pearde.py run work           # the boards declaring `groups: work`
python3 @resources/pearde.py run <prd>          # the loop over one PRD's subtree
```

`--dry` prints the plan and launches nothing; `--once` fills the pool once and
stops; `--workers N`, `--adapter <id>` and `--deadline S` are the rest.

**This command moves.** It claims, transitions and launches a pass worker per
row. Looking at the same frontier without starting anything is `pearde plan`,
and the two are separate names on purpose: a person must be able to read the
whole machine without the reading dispatching it.

A bare word is a scope, resolved in one order and refused rather than guessed:
`here` and `all` first, then a label a watched board declares in its own
settings, then a PRD on the board at the cwd. A word naming both a group and
a PRD is refused, with both named.

Two silences, both by design. A board nobody watches is invisible — the watch
set is the whole configuration, and no registry is written here
(@references/parts/all.md says the same of its own merge: *a member nobody
watches is not one of them*). And the slot count is a reading of the local
machine, so a proxy: run `pearde view` on a board first when the count is
missing, and read the number beside its reading rather than instead of it.

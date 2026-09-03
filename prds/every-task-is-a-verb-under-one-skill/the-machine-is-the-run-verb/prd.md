---
state: done
origin: requested
priority: 80
complexity: 35
blast-radius: high
needs:
  - the-machine-frontier-is-dispatched-in-parallel
workflow: probe-then-spec
actual: 13.15h
commit: 60f49d1 02af158
---


# the machine is the run verb

`machine` becomes `run`, whole — the verb, the script, the part, the scope
keyword and the skill body. The read `machine` did moves onto `plan`.

Waits on `the-machine-frontier-is-dispatched-in-parallel`: that PRD is in
flight on @resources/board/machine.py and @resources/board/dispatch.py, and a
rename under it loses one side's work.

## The rename

| now | then |
|---|---|
| `pearde machine` | `pearde run` — see the two tables below |
| @resources/board/machine.py | `resources/board/run.py` |
| @references/parts/machine.md | `references/parts/run.md` |
| `@@machine` in @index.md | `@@run` |
| `references/skills/pearde-all.md` | says `run`; the sibling folds the file itself |

`@resources/board/dispatch.py` keeps its name — it is what `run` calls, and
`dispatch` is still the right word for launching a worker. It stops being a
command word.

## `run` moves

`run` is the one command that launches. `machine dispatch` stops existing: the
verb is the command name, and there is no verb under it that moves.

| line | reads |
|---|---|
| `pearde run` | dispatch the board at the cwd |
| `pearde run here` | the same, said out loud |
| `pearde run all` | dispatch every board the daemon watches |
| `pearde run <group>` | the boards declaring `groups: <group>` (@references/settings.md) |
| `pearde run <prd>` | the loop scoped to that PRD's subtree on the cwd board — @references/parts/handles.md's row, unchanged |

`--dry`, `--once`, `--workers N`, `--adapter <id>` and `--deadline S` are
today's dispatch flags on this command. `--group <g>` goes: the scope word is
the group.

## `plan` reads

Every reading `machine` did, under `plan`, which already prints a frontier.
None of it moves anything.

| line | reads |
|---|---|
| `pearde plan` | the cwd board's frontier — today's `plan`, unchanged |
| `pearde plan here` | the same, said out loud |
| `pearde plan all` | every watched board as one ordered frontier, the waves, the slot count and its reading |
| `pearde plan <group>` | the same over one group |
| `pearde plan boards` | what the daemon watches, and each board's own cap |
| `pearde plan slots` | the concurrency and the numbers that produced it |
| `pearde plan progress` | one progress line over the merged set |
| `pearde plan groups` | the labels the watched boards declare, and who holds them |
| `pearde plan --json` | the same read, as data |

A verb and a scope compose in either order — `plan work slots`.

## Resolving a bare word

One order, and it is printed when it refuses:

1. `here` and `all` — reserved. Neither is a group and neither is a PRD.
2. A `groups:` label a watched board declares.
3. A PRD on the cwd board.

A word that is both a declared group and a PRD is **refused, naming both** —
guessing would dispatch the wrong set. A word that is neither is refused with
the groups that exist and the near-miss PRDs, the way `run <prd>` already
lists near-misses.

`boards`, `slots`, `progress` and `groups` stay refused as group labels, and
`dispatch` stops being reserved — @references/parts/machine.md's table of
refused labels moves with the file and loses that row.

## What must not change

- **Reading and moving stay two commands.** The rule survives the rename; it
  is now carried by two names rather than by a verb under one.
- **The slot count is never printed without its reading**, and every measured
  gotcha in @references/parts/machine.md — `vm_stat`'s free pages, `load1`'s
  lag in both directions, the throttle-path second opinion — carries into
  `references/parts/run.md` unchanged.
- **`run.py` writes no board's `settings.md`**, keeps no registry of boards,
  and adds no write door to the `all` page.
- **No legacy.** No alias, no former name, no migration note
  (@references/language.md). `machine` leaves the tree.

## Verify

`git grep -in machine` returns only prose about the physical machine — no
command, no path, no scope keyword, no skill line.

## History

**failed, retried 2026-09-02 18:16**

Built and verified, then destroyed by the tool collecting it.

Between 16:45 and 17:08 on 2026-09-02 the rename was implemented whole across
sixteen files and measured green by hand: `run --dry`, `run all --dry`,
`run private --dry`, `run <prd> --dry`, an unknown scope refused with exit 1,
all nine `plan` lines, `pearde index` clean, `doctor`'s `skills` / `index` /
`grammar` / `health` rows `ok`, `git grep -in machine` down to prose about the
physical machine, and both probe harnesses under
`the-whole-machine-is-worked-as-one-board` green — the read one 33/33, the
parallel one 13 fixture cases plus 9 repo rows.

At 17:08 `pearde collect` ran `specs/spec01.md`'s verify block. The block
exited non-zero on a fault of its own — `grep -q` on a pipe under
`bash -e -o pipefail`, and `.pearde/` paths that do not exist in a lane.
`collect` answered a red verify by calling `unland`, which runs
`git reset --hard` in the orchestrator's checkout. Every uncommitted change
there went, this PRD's implementation included. Reflog:
`HEAD@{0}: reset: moving to 35878179b1a7`.

Not recoverable. The content was never staged — the two `git mv`s are `R100`,
byte-identical to the originals — no lane held it, and no stash carries it.

**Correction, 2026-09-02 17:52, from the skeptic review of the fix.** The
sentence above originally said `land_lane` printed `merged nothing`. It did
not, and could not: that string exists at exactly one place,
`collect.py:1216`, inside the `opts["dry"]` branch, which returns
`(None, None)` — and the old `unland` already skipped that on `if not pre`.
The real mechanism is the reflog: the reset moved to `35878179b1a7` **from
`3587817`**, so HEAD was already on the target sha, `pre == HEAD`, and
`lanes.merge()` returned `0` at its `ahead in ("", "0")` branch. `pre` was
truthy and `landed` was zero, so the old `unland` ran `git reset --hard <HEAD>`
in a shared checkout — pure working-tree demolition with no merge to undo.
The diagnosis was right and the quoted line was wrong; the fix
(`if not pre or not landed: return`, plus `--keep`) closes exactly this.

Two things must happen before this is retried:

1. ~~`collect-must-not-reset-the-checkout-it-did-not-write`~~ — **done and
   committed at 17:52**, `e5abc5b`. `unland` now returns when nothing landed
   and uses `reset --keep`, which refuses rather than deletes. Reviewed by the
   skeptic against the incident: it closes exactly this loss. Two wider holes
   the review found are filed and in flight —
   `a-refused-rebase-must-not-destroy-the-lane-it-was-left-in` (p90, the same
   call in `lanes.py:180`, now the only `reset --hard` left in `resources/`)
   and `a-verify-block-must-not-destroy-the-checkout-it-runs-in` (p92, a verify
   block is arbitrary shell in the shared checkout and runs *before* `unland`
   is reached). Both should land before this rebuild is dispatched.
2. ~~One of the two renames goes first, and a person says which.~~ **Settled
   by fact, 2026-09-02 17:26 — no question to ask.** The board-directory
   rename (`.pearde` → `pearde`) is in the working tree and stashed
   (`git stash list`); this rename is gone —
   `lane/every-task-is-a-verb-under-one-skill-the-machine-is-the-run-verb`
   sits at `5413477`, one commit *behind* HEAD, and holds none of it. The
   unhiding lands first because it exists; this rebuild follows and rebases
   onto `resources/board/plan.py` as it then stands.

`specs/spec01.md` stands with its boxes un-ticked. Every box in it was written
from a run that actually happened; it is the shortest description of what to
build back, and its verify block needs its shell faults fixed before the next
`collect` — no `grep -q` on a pipe, and no `.pearde/` path.

## Report

spec01: exit 0

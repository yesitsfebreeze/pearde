---
state: open
origin: requested
priority: 80
complexity: 0
blast-radius: high
---

# every task is a verb under one skill

The user's words, 2026-09-02: *"lets rename the `machine` in this repo to
`run`, so there is only ONE skill `/pearde` but its an index of all the tasks
that we now have as skills. meaning we can to `/pearde run <group>` for a
specific group `/pearde run here` to run only the cwd project `/pearde run
all` to run over everything, `/pearde doctor` and so on."*

Two contracts, in this order, each its own child:

1. `the-machine-is-the-run-verb` — `machine` becomes `run`, `run` is the verb
   that moves, and the read it used to do moves onto `plan`.
2. `the-skills-fold-into-one-index` — the seventeen `pearde-*` skills become
   tasks named by one `pearde` skill.

## Settled with the user, so neither child re-asks

| fork | answer |
|---|---|
| `run` already means `run <prd>` (@references/parts/handles.md) | `run` takes a scope as its first bare word; `here` is the default. A bare word resolves `here`/`all` → a group a watched board declares → a PRD on the cwd board, and a word that is both is refused naming both |
| does `pearde run all` read or move? | it moves. `run` is a verb, so `machine dispatch` stops existing — the verb is the command name |
| where does the read go? | `plan`, which already computes a frontier. `plan`, `plan here`, `plan all`, `plan <group>`, and the verbs `boards`, `slots`, `progress`, `groups` under it |
| sequencing | this tree waits on `the-machine-frontier-is-dispatched-in-parallel`, which is in flight on the same files |

## What must not change

- **One alias.** `pearde <cmd>` stays the whole shell surface
  (@references/install.md). Folding the skills does not fold the commands.
- **Reading and moving are never the same command.** The rule from
  @references/parts/machine.md survives the rename — it is now carried by two
  names, `plan` and `run`, rather than by a verb under one.
- **No legacy.** @references/language.md: no alias, no former name, no
  migration note. `machine` is gone from the tree when this is done, and
  `git grep -i machine` returns only prose about the physical machine.

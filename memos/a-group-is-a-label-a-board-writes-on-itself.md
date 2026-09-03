---
memo: a-group-is-a-label-a-board-writes-on-itself
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: grouping the watch set is a `groups:` key on each board, never a registry of boards kept beside the machine
date: 2026-09-02
---

# a-group-is-a-label-a-board-writes-on-itself — the configuration stays distributed

`pearde machine` and the `all` page both rest on one sentence: **the watch
set is the whole configuration**. Registering a board is the whole of joining,
nothing writes a list of boards, and a board nobody watches is invisible
(@references/parts/machine.md, @references/parts/all.md). Splitting that set
into *work* and *private* is the first feature that needs configuration the
watch set does not already carry, so where it lives decides whether that
sentence survives.

## Decision

A group is a **label a board writes on itself** — `groups: work infra` in its
own `.pearde/settings.md`, set with `pearde settings groups=work` standing in
that board. `pearde machine <group>` is the same read over the boards carrying
it: same `compute_plan`, same waves, same slot count, fewer boards.
`machine <group> dispatch` runs that group down.

- **Labels, not a partition.** A board may carry several and most carry none.
  `work` and `private` are two labels among any others, so a later `infra` or
  `client-x` costs nothing and no board is forced to declare one.
- **Nothing keeps the list.** The groups a machine has are whatever its boards
  say, read as the walk passes each one. No file names them, and `machine`
  still writes no board's `settings.md`.
- **A group naming no watched board is refused**, not answered with an empty
  frontier — an unwatched board is invisible here, so silence would read as
  *nothing to do* when the truth is *that board was never registered*.
- **Two labels are refused where they are declared**: a verb, so
  `machine slots` keeps meaning the slot reading, and `all`, which is every
  board and never a subset of them.
- **The `all` page gets no group filter.** Grouping is a command-line read; a
  `/board/all/<group>` would put a second answer to *what is the set* on the
  one page whose rule is that the watch set is it.

## Alternatives considered

**One machine-local groups file** — `~/.pearde/groups.md` mapping label to
board paths. It groups a board without touching that repo, and puts the
answer in one place. It also creates the registry both contracts say does not
exist, and with it a second source of truth: a board could sit in a group and
not in the watch set, so `machine work` would name work that is not
discoverable. The rule that makes this command debuggable is that there is
nowhere else to look.

**Both, the file overriding the boards** — the most flexible, and two places
to read when a board is missing from a group. Flexibility bought with an
ambiguity nobody can see from either file.

**An exclusive tree — every board work XOR private** — renders as a tree under
`all` and gives `ungrouped` a real bucket. It also forbids the overlap that a
label set gets free, and the request that prompted this (*work* and *private*)
is satisfied by labels without the ceiling.

## Consequences

- A board with no `.pearde/` cannot be grouped, because it is not a board.
- Grouping a board is an edit in that repo, committed with it — which is also
  what makes it survive a reclone, where a file on this machine would not.
- Two boards disagreeing on a label's spelling are one group: labels are
  case-folded, and that is all the reconciliation there is.

---
memo: the-board-directory-is-pearde-and-the-compat-symlink-is-gone
kind: invariant
status: decided
tags:
  - memo
  - kind/invariant
  - status/decided
subject: the board directory is .pearde and the compat symlink is gone
date: 2026-09-03
verify: test -d .pearde -a ! -L .pearde -a ! -e pearde
---

# the-board-directory-is-pearde-and-the-compat-symlink-is-gone — the board directory is .pearde and the compat symlink is gone

## Decision

This project's board is a real directory at `<project>/.pearde/`. It is not a
symlink, no file it owns is reachable only through one, and no second name —
`pearde/` in particular — resolves to it on disk. `pearde` survives in the code
only as `LEGACY_BOARD_DIR`, so a board that never migrated still resolves.

## Why

On 2026-09-02 the board was renamed `.pearde/` → `pearde/` to get it out of
Obsidian's way: Obsidian skips every path holding a dot-segment, so from a
vault rooted at the project the whole board was invisible. An untracked
`.pearde -> pearde` symlink was left beside it so paths spelled the old way
kept resolving.

Within a day that cost more than it bought, and both costs were measured:

- **One board resolved twice.** `BOARD_DIRS` accepted both names, so `scan` and
  the view daemon registered `pearde` and `pearde-2`. `run all` handed every
  PRD out twice; two workers wrote one lane, and one of them found amends and
  rebases in its reflog it had not made, with its boxes already ticked when it
  arrived.
- **Every collect refused.** In the checkout the two names are one directory.
  In a lane or session worktree they are two separate near-empty real
  directories, because an untracked link materialises the name without the
  content. Five finished PRDs sat jammed behind it, every one reporting DONE.

The premise was also wrong about the remedy rather than about Obsidian. The dot
does hide the board from a project-rooted vault — but the fix is the vault at
`<board>/.obsidian`, which `references/obsidian.md` already specifies, not a
board renamed out of hiding. A symlink cannot bridge it either: Obsidian
refuses a link that resolves back inside its own vault.

The rename hit every board on this machine the same day, and this is the repo
where it bites hardest, because the checkout is itself called `pearde`. Measured
2026-09-03: seven boards — `dotfiles`, `infra/mitosys`, `infra/model`,
`infra/realm`, `infra/shared`, `manola`, `racer/.mi` — still carry the undotted
directory with the symlink beside it, and one, `zirkle/kern`, is dotted. So all
seven carry this defect, and `pearde upgrade` is what moves them.

## Alternatives considered

**Keep `pearde/` and delete only the symlink** — the double resolution goes and
the collects unjam, but this checkout sits at `infra/pearde` beside an `infra`
board, so an ordinary word keeps reading as a board name. Lost on the user's own
sentence: *"we need all files in .pearde not a symlink."*

**Keep a reverse `pearde -> .pearde` link for one release** — proposed by the
PRD as the safe default for the machine's other boards mid-upgrade. Lost on
measurement: this checkout already holds the name `pearde`, so the reverse link
cannot be written here at all, and a compat mechanism that cannot exist on the
board that needs it most is not a compat mechanism. Both readers accept both
names already, which is the compatibility that was actually wanted.

## Consequences

- `pearde upgrade` on a live board strands every lane and session worktree:
  they sit at `<board>/.lanes/` and `<board>/.sessions/` with absolute paths
  under the old name. This repo's move was taken by hand with `git worktree
  repair` over all 33 of them; `upgrade` must do the same, or run only with
  `scan` clean and `session reap --apply` done.
- `doctor`'s vault row now reads **broken** and prints a fix that moves the
  board back. The row argues from the superseded premise and is owed a rewrite
  — `the-vault-roots-at-the-board-not-the-project`.
- Six modules still carry their own literal copy of the two constants, and
  `doctor.sh` and `statusline.sh` still try the undotted name first. Nothing
  breaks, because every reader accepts both — but the name is still spelled in
  eight places. `the-board-name-is-one-dotted-constant` is the one place.
- Seven other boards on this machine still hold the symlink and the undotted
  directory. They are not covered by this memo, which is about this board; the
  invariant's `verify` runs at a project root and passes only where the move has
  been taken. `pearde upgrade` is the thing that has to move them, and it does
  not repair worktree registrations yet.
- A verify block that names a board path cannot spell it relative to the cwd:
  a worktree of the code repo holds an empty `.pearde/`. Four specs were
  repaired this pass to resolve it from `git rev-parse --git-common-dir`.

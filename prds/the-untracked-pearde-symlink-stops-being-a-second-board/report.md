# report — the untracked .pearde symlink stops being a second board

Verdict: DONE

Taken by the orchestrator in its own pass rather than by a worker: the symlink
was refusing every collect on the board, so no worker could have landed
anything while it stood, this one included.

## What was done

- The untracked symlink `<project>/.pearde -> pearde` removed.
- `<project>/pearde/` renamed to `<project>/.pearde/`, the board repo's own
  history intact — the board is a git worktree on branch `pearde`, and its
  `.git` file already pointed at `worktrees/-pearde`, the name it was
  registered under before the 2026-09-02 rename.
- All 33 lane and session worktrees re-pointed with `git worktree repair`;
  `git worktree list` now names no path under the old directory, and
  `git worktree prune --dry-run` is silent.
- Absolute paths rewritten in `.state/sessions.json` and `.state/serve.json`.
- `BOARD_DIR = ".pearde"`, `LEGACY_BOARD_DIR = "pearde"` — commit `19b2774`,
  and carried into `resources/board/boards.py` when
  `the-largest-module-is-cut-by-responsibility` landed the module cut on top.

## Acceptance

- [x] One name resolves this board. `scan` prints `board:
      /Users/feb/dev/infra/pearde/.pearde` from the checkout and from a lane
      worktree, and the view daemon lists `pearde` once — the duplicate
      `pearde-2` registration is gone.
- [x] `collect` runs a PRD's probe from a lane and a session worktree with
      every path resolving, proved on the stuck five: `the-cross-board-parts-
      are-rewritten-dense`, `the-machine-is-the-run-verb`,
      `the-loose-reference-files-are-rewritten-dense`,
      `the-largest-module-is-cut-by-responsibility` and
      `two-harnesses-still-name-a-tree-they-do-not-measure` all closed in this
      pass, four of the five needing a rebase onto main as well.
- [x] The choice is recorded as a memo —
      `memos/the-board-directory-is-pearde-and-the-compat-symlink-is-gone.md`,
      kind `invariant`, `verify: test -d .pearde -a ! -L .pearde -a ! -e pearde`,
      which holds. The link went now; it does not wait for the migration,
      because it *was* the migration.
- [x] No `pearde upgrade` ran while a lane or session worktree was live. None
      ran at all: `upgrade` does not repair worktree registrations, and 29
      lanes plus 4 session trees sat under the directory being moved. The move
      was taken by hand with `git worktree repair`, with no lane written in the
      preceding 25 minutes and the view daemon stopped for the rename.

## What this did not fix, and where it went

Three findings, all carried into the memo's *Consequences* and into
`the-board-is-a-real-directory-at-pearde-never-a-symlink`'s four children:

1. `doctor`'s vault row now reads **broken** and its printed fix moves the
   board back — it argues from the premise this PRD overturned.
2. Six modules still each carry a literal copy of the two constants;
   `doctor.sh` and `statusline.sh` still try the undotted name first. Nothing
   breaks: every reader accepts both names.
3. A verify block cannot spell a board path relative to its cwd — a worktree of
   the code repo holds an empty `.pearde/`, which is the mechanism that made
   this jam look like four unrelated failures. Four specs were repaired this
   pass to resolve the board from `git rev-parse --git-common-dir`; nothing yet
   stops a fifth being written the broken way, and that is worth its own PRD.

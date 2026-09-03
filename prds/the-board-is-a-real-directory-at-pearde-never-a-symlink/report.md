# report — the board is a real directory at .pearde, never a symlink

Verdict: REFINE

complexity 52 · blast-radius high · workflow `probe-then-spec`

## Landed by hand before this report, and why the PRD is still not done

The directory move itself ran in the orchestrator's own pass on 2026-09-03,
ahead of the split, because it was the one thing blocking every other PRD on
the board: the untracked `.pearde -> pearde` symlink made one directory answer
to two names, which fanned every dispatch out twice and refused every collect.

What landed: the symlink removed, `pearde/` renamed to `.pearde/` with the
board repo's history intact, all 33 lane and session worktrees re-pointed with
`git worktree repair`, the absolute paths in `.state/sessions.json` and
`.state/serve.json` rewritten, the view daemon's duplicate `pearde-2`
registration gone, and `BOARD_DIR = ".pearde"` / `LEGACY_BOARD_DIR = "pearde"`
in the one reader that was free to write — commit `19b2774`, carried into
`resources/board/boards.py` when `the-largest-module-is-cut-by-responsibility`
landed on top of it.

What is still owed is everything the four children below name. The six other
modules still each carry their own literal copy of the two constants;
`doctor.sh` and `statusline.sh` still try the undotted name first; `doctor`'s
vault row now reads **broken** and its printed fix is to move the board back,
which is the wrong direction; and the prose still describes the undotted
layout. None of that stops the board working today — every reader accepts both
names — and all of it is a second reader's chance to disagree with the first.

## Why it splits

**The vault is a second contract, and the two sentences are two vault roots you
cannot both have.** A project-rooted vault hides a `.pearde/` board; a
board-rooted vault hides the project's code from the board. The compat symlink
does not rescue it either — Obsidian refuses a link that resolves back inside
its own vault. So `doctor`'s vault row cannot be both green and true while the
vault roots at the project. The fix is the vault at `<board>/.obsidian`, which
`references/obsidian.md` already says; `references/parts/board.md` says the
opposite, and the two files have to stop contradicting each other.

Prose is mostly right already: 462 occurrences of `.pearde` against 149 of the
non-dot name, and only six doc files spell the non-dot name at all.

The build that stood up under this analysis measured clean: fresh `init` made a
real `.pearde/`, `upgrade` moved a board, `scan` printed `board:
<project>/.pearde`, gates unchanged from baseline. It also found that
`init.py`'s `unhide_board` guarded on `os.path.isdir` alone — which would have
renamed this repo's own checkout, since the checkout is itself called `pearde`.
The replacement guards on `is_board_dir`.

## Split

| child | contract | needs |
|---|---|---|
| the-board-name-is-one-dotted-constant | Every resolver reads `.pearde` from one place — one zero-dependency Python module the six duplicating readers import, one shell file both `doctor.sh` and `statusline.sh` source — and `pearde` is only the legacy name | — |
| init-and-upgrade-write-the-dotted-board | `pearde init` makes a real `.pearde/`, `pearde upgrade` moves a board still at `pearde/` into it and rewrites the ignore block whole instead of appending a second, and the guard on the rename is `is_board_dir`, never `isdir` | — |
| the-vault-roots-at-the-board-not-the-project | The vault is `<board>/.obsidian`, every vault-relative path the board writes is board-relative, and doctor's vault row says something a dotted board makes true | — |
| the-prose-and-the-invariants-say-dot-pearde | Every reference page, index row, invariant script and code comment naming the board directory names `.pearde/`, and *Where the board is* reads the new order | — |

Disjoint footprints.

- **name**: `resources/board/name.py` (new), `resources/board/boards.py`,
  `resources/guard.py`, `resources/grammar.py`, `resources/health.py`,
  `resources/memos.py`, `resources/questions.py`, `resources/statusline.sh`,
  `resources/doctor.sh`
- **init/upgrade**: `resources/board/init.py`, `.gitignore`
- **vault**: `resources/board/obsidian`, `resources/board/knowledge`,
  `resources/knowledge.py`, `references/obsidian.md`
- **prose**: `references/parts`, `index.md`, `resources/invariants`,
  `resources/graph/graph.sh`, `resources/board/collect.py`,
  `resources/board/shared.py`, `resources/board/session.py`,
  `resources/board/serve.py`, `resources/board/refuse.py`

Weights 10 / 14 / 18 / 10.

## Ordering hazard the table cannot encode

A real `pearde upgrade` on a live board **strands every lane and session
worktree**: they sit at `<board>/.lanes/` and `<board>/.sessions/` with
absolute paths under the old name, and every sibling here runs in a lane under
that same directory. The move must be last and alone, with `scan` clean and
`session reap --apply` done. This repo's own move is already taken, so the
hazard now belongs to `upgrade` on the eight other boards rather than to this
one. `/Users/feb/dev/infra` is the board where the reverse `pearde` compat link
cannot be written, because this checkout already holds that name — which is the
measurement that ends the argument for keeping a reverse link at all.

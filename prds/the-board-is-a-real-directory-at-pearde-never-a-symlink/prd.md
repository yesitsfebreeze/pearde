---
state: open
origin: requested
priority: 95
complexity: 0
blast-radius:
---

# the board is a real directory at .pearde, never a symlink

The user asked for this on 2026-09-03, in these words: *"we need all files in
.pearde not a symlink."*

**Today.** The board directory is `<project>/pearde/` — no dot — and
`<project>/.pearde` is a relative symlink pointing at it.
`references/parts/board.md` under *Where the board is* documents that layout
and the four-step resolution order that prefers `pearde/`; the code repo's
`.gitignore` ignores both names; the rename happened 2026-09-02.

**What is wanted.** `<project>/.pearde/` is a real directory holding every file
the board owns — `settings.md`, `vision.md`, `prds/`, `memos/`, `workflows/`,
`.state/`, `wiki/`, and the board's own `.git`. Nothing on that path is a
symlink, and no board file is reachable only through one.

## Done means

- `test -d <project>/.pearde -a ! -L <project>/.pearde` passes on this repo and
  on a board `pearde init` has just made.
- Every file that was under `pearde/` is under `.pearde/`, with the board
  repo's history intact — the move is a rename inside the board's own repo,
  never a copy that loses the log.
- `references/parts/board.md` under *Where the board is* says `.pearde/` and
  its resolution order names it first. `references/obsidian.md` already roots
  the vault at `.pearde/`; the two files no longer contradict each other.
- The `.gitignore` block, `init`, `upgrade`, `doctor`, `statusline.sh` and
  every module naming the board directory read the name from one place, not
  from a literal repeated per file. `pearde index scope board` names them.
- `pearde doctor` is green and `pearde scan` prints `board: <project>/.pearde`
  on this repo.
- A board still at `pearde/` is moved by `pearde upgrade`, not by hand.

## Do it when the board is quiet

Live lanes and session worktrees carry absolute paths under `pearde/`, and a
rename under a live claim strands them. `pearde scan` must show nothing in
flight and `pearde session reap --apply` must leave nothing on the ledger but
the running session before the move runs.

## Two calls this PRD makes, and does not ask

1. Whether `pearde/` survives as a compatibility symlink onto `.pearde/`.
   Recommended: yes, for one release, so the machine's other seven boards and
   any board mid-upgrade keep resolving. The user's sentence constrains
   `.pearde`, not its reverse.
2. What the claim in `board.md` — that a dotted board never appears in a vault
   — is worth, given `references/obsidian.md` roots the vault at the board
   itself and reports every child showing. Measure it. Do not repeat either
   sentence.

## Related, and not this PRD

A session worktree is a worktree of the *code* repo and carries no board at
all, because the board is a separate git repo the code repo ignores. Three of
`the-cross-board-parts-are-rewritten-dense`'s verify blocks hardcode
`.pearde/prds/...` and cannot resolve there for that reason. Renaming the
directory does not fix that; folding the two repos into one would. Record it,
do not do it here.

## Children

| child | contract | needs |
|---|---|---|
| `the-board-name-is-one-dotted-constant` | Every resolver reads `.pearde` from one place — one zero-dependency Python module the six duplicating readers import, one shell file both `doctor.sh` and `statusline.sh` source — and `pearde` is only the legacy name | — |
| `init-and-upgrade-write-the-dotted-board` | pearde init` makes a real `.pearde/`, `pearde upgrade` moves a board still at `pearde/` into it and rewrites the ignore block whole instead of appending a second, and the guard on the rename is `is_board_dir`, never `isdir | — |
| `the-vault-roots-at-the-board-not-the-project` | The vault is `<board>/.obsidian`, every vault-relative path the board writes is board-relative, and doctor's vault row says something a dotted board makes true | — |
| `the-prose-and-the-invariants-say-dot-pearde` | Every reference page, index row, invariant script and code comment naming the board directory names `.pearde/`, and *Where the board is* reads the new order | — |

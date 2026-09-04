---
complexity: 10
footprint:
  - resources/board/init.py
---

# spec01 — init writes a real `.pearde/`, upgrade moves a board into it, and the ignore block is rewritten whole

`init.py` makes the board at `.pearde/` and `upgrade` renames a board still at
`pearde/` into that name before any later step reads a path. The machine-local
block in the parent repo's `.gitignore` is rewritten whole from
`ignored_names()` — never appended to — so a board that moved changes every row
at once, and the rename is guarded by `planlib.is_board_dir`, because `pearde`
is an ordinary word and a checkout called that must not be renamed out from
under its owner.

## What already stands

Uncommitted in the lane, and green under the probe (26 of 26). The unit is
review-and-land, not a build from nothing:

- `live_worktrees(board)` — the lanes and sessions checked out under a board.
- `dot_board(d, name=None)` replaces `unhide_board`: `pearde/` → `.pearde/`,
  no symlink left behind, refusing a `--dir` of `pearde`, a name holding a path
  separator, an occupied destination, and a board with a live worktree under it.
  Its guard is `os.path.islink(old) or not planlib.is_board_dir(old)`.
- `IGNORE_HEADER`, `split_ignore_block(text)`, and a `write_gitignore` that
  rewrites the block whole, strips a second block an older append left, and
  keeps every line outside the block byte for byte.
- `cmd_upgrade` calls `dot_board` first and prints the row that says what moved.
- `ignored_names(board)` prepends the whole-directory row `/<board>` when the
  board carries its own `.git`. Without it `git add -A` in the parent stages the
  board as a gitlink, mode 160000 — measured in a fixture, and true of this
  repo, whose board is a worktree of the code repo.
- The header is matched by `startswith` and the block runs to the first blank
  line, so a header a person annotated is healed rather than doubled. This
  repo's own file carried exactly that shape and got a second block appended
  under the equality match.

## What is left to finish

- Read the diff once as a second reader and land it. Nothing else is owed by
  this spec — the checks below are the probe's, and they pass today.
- Keep the docstrings honest to the code: `dot_board`, `ignored_names` and
  `split_ignore_block` each carry the measurement that decided them, and a
  change to the behaviour that leaves the prose standing is the defect this
  board keeps finding elsewhere.

## Acceptance

- [ ] A fresh `pearde init` in a git repo leaves `<dir>/.pearde/` a real
      directory, not a symlink, with `settings.md` in it and nothing at
      `<dir>/pearde`.
- [ ] That run's `.gitignore` holds exactly one machine-local header and rows
      spelled `.pearde/…`.
- [ ] `pearde upgrade` on a board still at `pearde/` moves it to `.pearde/`,
      leaves nothing at `pearde/`, and leaves no row spelled `pearde/…`.
- [ ] A `.gitignore` an older append doubled comes back with one header, and a
      line written after the doubled block survives.
- [ ] A `.gitignore` whose header carries a trailing sentence and comment lines
      under it is healed to one canonical block, its stale rows and its stale
      comment lines gone, and a second `upgrade` writes nothing.
- [ ] A directory called `pearde/` that is not a board — no `settings.md`, no
      `prds/` — is not renamed by `upgrade`.
- [ ] A board carrying its own `.git` gets the whole-directory row, and
      `git add -A` in the parent stages no entry of mode 160000.
- [ ] A board the parent repo tracks gets no whole-directory row, so the PRDs
      stay in the parent's history.
- [ ] `pearde scan` on the fresh board prints `board: <project>/.pearde`.

## Verify and Proof

```sh
bash .pearde/prds/the-board-is-a-real-directory-at-pearde-never-a-symlink/init-and-upgrade-write-the-dotted-board/probe/probe.sh
python3 resources/index.py check
for f in resources/invariants/*.sh; do printf '%s: ' "$(basename "$f")"; bash "$f" >/dev/null 2>&1 && echo ok || echo FAIL; done
```

The probe must print `26 passed, 0 failed`. `index.py check` prints one
finding — `references/parts/commits.md references @pearde/memos/…` — which is
the baseline and belongs to `the-prose-and-the-invariants-say-dot-pearde`.
Three invariants read FAIL from a lane worktree at baseline
(`every-artifact-lands-inside-the-board`,
`no-colour-group-in-the-vault-preset-is-a-path-query`,
`no-destructive-git-runs-in-a-tree-the-session-does-not-own`); none of them may
change count.

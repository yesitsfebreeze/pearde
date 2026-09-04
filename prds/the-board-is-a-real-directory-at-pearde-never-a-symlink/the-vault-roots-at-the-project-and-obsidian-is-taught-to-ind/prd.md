---
state: specced
origin: requested
priority: 95
complexity: 38
blast-radius: mid
supersedes: the-vault-roots-at-the-board-not-the-project
workflow: implementer-continue
---

# the vault roots at the project and obsidian is taught to index the dotted board

The Obsidian vault is the **project root**, not the board. `.pearde/` sits inside that vault as an ordinary indexed folder, and the plugin [polyipseity/obsidian-unhide](https://github.com/polyipseity/obsidian-unhide) is what makes Obsidian index a dot-directory it would otherwise refuse to show. Notes, memos, PRDs and the knowledge base are then reachable from the same vault as the code and the docs, under one graph.

The user asked for this in these words on 2026-09-03: *"https://github.com/polyipseity/obsidian-unhide we also need this, so we can use the project root as the obsidian root and index .pearde"*.

**This supersedes `the-vault-roots-at-the-board-not-the-project`**, which held the opposite contract — the vault at `<board>/.obsidian` with every vault-relative path board-relative. That child was the board's own answer to `doctor`'s red vault row; this is the user's, and the two cannot both be true. The superseded child had no specs and no built work, so nothing is lost by the reversal. It did carry one finding worth keeping: **`doctor`'s vault row currently prints `pearde upgrade` as its fix, which would move the board back to the undotted layout** — that row is wrong under either contract and is in this PRD's scope.

Two facts this must not lose. The board directory is `.pearde/`, a real directory, and no `pearde` symlink comes back — that is an invariant on record (`memos/the-board-directory-is-pearde-and-the-compat-symlink-is-gone.md`). And `pearde init` currently writes into Obsidian's machine-wide vault register with no fixture flag, so a throwaway fixture board registers itself; whatever registers the project root here must not repeat that.

## Done means

- [x] The vault Obsidian opens is the project root, and `.pearde/` is indexed inside it rather than being a vault of its own.
- [x] `obsidian-unhide` is declared as the dependency that makes the dotted board visible, with the version pinned and its absence reported rather than assumed.
- [x] Every vault-relative path the board writes resolves from the project root, and the wikilinks in memos, knowledge notes and PRDs still resolve inside the merged vault.
- [x] `doctor`'s vault row states the project-rooted contract and names a fix that does not move the board back to the undotted layout.
- [x] Registering the vault is opt-in and does not fire for a fixture board.

## Blocked

**2026-09-03 14:14 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s98669`; 4 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-03 15:37 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s98669`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-03 17:15 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s98669`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-03 20:53 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s27323`; 6 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-03 21:57 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `main`; 7 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s62223`; 7 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `main`; 7 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s62223`; 7 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s62223`; 7 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s62223`; 7 file(s) disagree:

- `references/files.md`
- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s85810`; 6 file(s) disagree:

- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 02:56 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `session/s85810`; 6 file(s) disagree:

- `references/knowledge.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/knowledge/Dashboard.md`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 04:03 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `main`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 04:06 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `main`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

**2026-09-04 04:20 — the lane will not rebase**

`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` does not land on `main`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.

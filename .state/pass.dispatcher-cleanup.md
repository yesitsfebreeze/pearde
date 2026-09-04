# pass.dispatcher-cleanup — session pearde-71, 2026-09-02

Not a pass. A dispatcher session that was asked to commit and clean across
every board. `pass.md` is untouched and still holds the pass worker's BLOCKED
handover — do not overwrite it.

## Established

- The pass worker returned BLOCKED. One PRD landed (`33f95b2`); six more were
  finished and unmergeable behind uncommitted paths belonging to ended
  sessions. That blocker is now cleared — the paths are committed.
- Three workers independently proved verify-block shapes that exit 0 on a
  broken tree. **Green acceptance boxes board-wide may be lying until swept.**
- The daemon PRD must not be collected while its verify block runs
  `git stash pop` in the shared checkout.

## Done, in this repo

Five commits on `main`, working tree clean, HEAD ahead of origin by 13:

- `72d5afc` the graph view is coloured by tag, not by folder
- `caa9a21` the all board renders a pass as read-only, with no dead control
- `de8af01` a lane is kept out of the commit by the ignore, not by the board being scratch
- `38d04b8` init carries the lane ignore, repairs the graph preset, names the host gap
- `ac73576` the index answers for pearde-machine, and edit.py names the file that exists

Cleaned: empty `.state/` at repo root, 8 merged lane worktrees (37M) and their
branches, `parse-cache.json` (14M, rebuilt at 1.7M), 34 `__pycache__`,
superseded graphify snapshots and vault backup, empty stray skeletons at
`pearde/pearde/` and `pearde/resources/`. 24 lanes kept — dirty, unmerged, or
touched by a live peer.

Forgot 15 temp board registrations (14 dead `tmp.*` harness fixtures, one
scratchpad probe). 25 watched boards down to 10.

## Done, across the other boards

- **realm** `f503fd1` board rename `.pearde/` → `pearde/`, 67 renames;
  `0e33822` a vendoring memo. Clean.
- **shared** `289d29d` same rename, 77 renames. Clean.
- **model** `202d15c8` memos carry derived tags; `c3c3aa27` a new memo;
  `03815706` five PRDs claimed. Clean.
- **mitosys** `b37264b9` — **a recovery, not a rename.** The move had been left
  half done: `pearde/` held empty directory skeletons, 310 tracked files were
  deleted from the working tree with no copy at the new path, and only HEAD
  still had them. Restored from HEAD into `pearde/`, the 13 files unique to the
  old path moved across, `.pearde` replaced by a symlink. Committing the state
  as found would have recorded the loss.

- **manola** `471f81f` board rename, 442 renames. The ignore was the part left
  behind: the old block named `.claims/` and `.lanes/`, the new one did not, so
  135 machine-local entries were being staged like source. Fixed at the new
  path, superseded vault backup dropped. Clean.
- **dotfiles** `59c4c63` board rename, 383 renames, and `graphify/` + `wiki/`
  dropped from tracking — generated, tracked at the old path by oversight. Then
  `33cf3d2` the tmux Claude-state hook and its scripts, `7b1ad01` the manual.
  Clean.
- **racer** `0681bd0` board move `.mi/prd/` → `.mi/pearde/prds/`, 49 renames.
  Committed by pathspec so another session's staged `src/visual/` renames were
  left in the index untouched.

## Owed

- **racer**, 56 dirty. The `.mi/workflows/` deletions are deliberately NOT
  committed: they are the old `mi` runner scripts (`mi-run.js`, `mi-replan.js`,
  `resources/*.md`), gone from the tree with no counterpart at the new path and
  no clear replacement — superseded or lost is a question for the user. It also
  carries unverified game source: modified `.odin` files, three staged renames
  into `src/visual/`, new untracked `src/race/`, `src/telemetry/`,
  `src/tutorial/`, and junk — `src/main/states.odin.bak`, unexplained `.pi/`,
  `.kern/`, `fzero-x-prompts/`, `math_template/`.
- **kern** 8 untracked, and `kern-ad` was still live in it. Left alone
  deliberately — never commit under another session's feet.
- **mitosys** 15 dirty: 11 modified Rust/JS files and 4 new test files pairing
  with the `plugins-visible` PRD. They need a build check before committing.
- `references/personas/writer.md` is referenced by `references/language.md`
  and does not exist — the one `index` problem left, and real work.
- `origin` row: 1 of 33 derived PRDs has no `from:`.
- Six stashes untouched, including two pre-collect safety nets from other
  sessions. Dropping them is the user's call.
- `pearde` and `pearde-2` are the same board under two watch keys — `.pearde`
  is a symlink to `pearde`. One should be forgotten; the live view is on
  `pearde-2`.

## Watch for

A lane cut before `72d5afc` that runs `knowledge.py board` strips `tags:` from
every PRD note and breaks the colour-group invariant. It happened once during
this session and was repaired by regenerating. Rebase those lanes, or retag at
collect.

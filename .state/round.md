# round

Everything below is in the working tree. **Nothing has been committed and
nothing has been pushed** — the user asked for a push and the round hit its
context ceiling before it could run. That is owed point 1 and it is the first
thing the next session does.

## how to resume

Read this file, then `python3 resources/board/plan.py scan`. It succeeds — the
migration gate is passed. 55 PRDs, 12 open, 8 ready. Nothing is blocking and
no question is open.

## done this round

**The hand migration (last round's owed point 5) is complete.** `prds/` →
`.pearde/`, PRD directories under `.pearde/prds/`, `knowledge/` → `wiki/`, the
five state dotfiles → `.pearde/.state/<name>` with their leading dots dropped,
`memos/` and `workflows/` now siblings of `prds/`, `settings.md`, `vision.md`
and `report.md` at the board root. `.claims/` stayed at `.pearde/.claims/` —
`collect.py` and `transitions.py` still join it from the board, so that is
where it belongs; it was not one of the five files last round named.

`scan` reports every PRD under the name it always had — the `relpath(root,
scan_root)` fix from last round holds.

**A second missed relayout spot, found and fixed:** `add()` in
`resources/board/transitions.py` set `base = board`, so every `pearde add`
wrote its PRD to the board root, where `scan` no longer looks — the same
defect as `init.py`'s, in a different file. Now `base = planlib.prds_dir(board)`.
`py_compile` clean. The seven PRDs it had already misplaced were moved by hand.
**Worth a sweep for more of these:** any `os.path.join(board, ...)` that should
now be `prds_dir(board)`.

**Seven PRDs added** for last round's owed points, all `open`:

    p80  init-writes-a-board-on-the-pearde-layout          (owed 1)
    p75  every-document-names-the-path-the-board-is-on     (owed 3)
    p70  the-doctor-checks-the-path-a-board-is-on          (owed 4)
    p65  the-vault-ignores-the-paths-the-board-writes      (owed 2)
    p60  the-graph-lands-inside-the-board                  (new, user)
    p50  the-other-boards-move-once-and-the-script-goes    (owed 6)
    p40  the-sweep-leaves-nothing-unregistered             (owed 7)

The migrate PRD carries `needs:` on the init, docs and doctor PRDs — it must
not run until the layout is settled everywhere it is read. Owed point 3 was
written as one PRD, not pre-split: its body names the mechanical table and the
ambiguous bare-`prds/` cases as the two halves, and the analyst's split-above
rule will REFINE it if the specs run long. That is the board's own mechanism;
do not hand-split it.

**The install was repointed and rebuilt.** All 14 skill folders under
`~/.claude/priv/skills` and both worker types under `~/.claude/priv/agents`
link into `references/skills/` and `references/agents/`. No dangling links.
`memo check` is silent.

## the user's instructions this round, in order

1. **`graphify-out/` should be `.pearde/graphify/`.** -> PRD
   `the-graph-lands-inside-the-board`. Researched before writing it, and the
   finding is in the body: `graphify extract` and `graphify update` have **no
   output flag and no environment variable** — they write `graphify-out/`
   relative to the cwd, always. Only the read commands take `--graph <path>`.
   So it is either a post-extract move plus `--graph` everywhere, or a
   gitignored symlink at the root. Either way graphify's `.graphify_root`
   marker must be written correctly, because without it `build.py` falls back
   to a `<root>/graphify-out/` grandparent heuristic that is wrong for the new
   path, and its pruning is what suffers.
2. **`agents/` should sit under `references/`.** Already true on disk when
   checked — `references/agents/` holds both worker types.
3. **`skills/` should also move to `references/`.** Also already true on disk —
   `references/skills/`, 14 files. A `git mv` failed with `bad source` for
   exactly that reason. **Both moves were made outside this session** (several
   sessions write this board), so check before assuming a file is yours.
4. **Gitignore every living board state; the repo should be clean to install.**
   **Done, on the wide reading — the user was asked and chose it.** `.gitignore`
   now holds one line, `.pearde/`, and `git rm -r --cached .pearde` took the
   whole board out of the index: 245 paths staged as deletions, every file
   still on disk, `scan` still reporting 55 PRDs. A clone now carries the
   source tree only and `pearde init` writes it a fresh board. The tracked
   history of the 48 PRDs, 16 memos and 18 workflows stops here — that was the
   known cost and it was accepted.
5. **"push everything."** Not done — the guard cut the round at its context
   budget before any git command could run, and git is not one of the commands
   it still allows. Owed point 1.

## edits made this round

- `.gitignore` — the seven `prds/*` lines replaced, first by three `.pearde/*`
  lines and then, on the user's answer, by the single line `.pearde/`.
- `resources/board/transitions.py` — `add()`: `base = planlib.prds_dir(board)`.
- `resources/install.sh` — repointed for the two directory moves, **11
  substitutions, `bash -n` clean**: `source_of()`'s `%s/skills/%s.md` ->
  `%s/references/skills/%s.md`, the skill loop's `"$ROOT"/skills/*.md`,
  `want_gate` and its two messages, the agents loop's `"$ROOT"/agents/*.md`,
  the `pwd -P` comparison against `"$ROOT/agents"`, its `did` line, and two
  header comments.
- `.pearde/prds/every-document-names-the-path-the-board-is-on/prd.md` — body
  extended with the `agents/` and `skills/` mappings and every stale anchor
  they leave behind.
- `.pearde/prds/the-other-boards-move-once-and-the-script-goes/prd.md` —
  `needs:` on the three layout PRDs, written as a YAML list (a flow list
  `[a, b, c]` is **not** parsed; `scan` said "names no PRD on this board").
- Last round's `plan.py` / `render.py` / `transitions.py` / `guard.py` /
  `knowledge.py` / `init.py` / `serve.py` edits are untouched and still
  uncommitted.

## owed

1. **Push everything. This is the whole of the next session's first step, and
   it is what the user last asked for.** Nothing is committed. The working tree
   holds the entire `.pearde` relayout, the serve.log cap from last round, the
   two directory moves, the install repoint and the board's removal from the
   index. Before committing, run `git remote -v`, `git status -sb` and
   `git status --short` — **none of that was ever read**, so whether this repo
   has a remote at all, and whether the recent `merge PR N:` commit subjects
   mean a branch-and-PR flow rather than a direct push to `main`, is still
   unknown and must be looked at rather than assumed. Expect roughly 245 staged
   deletions (the old `prds/*` paths leaving the index) plus around 40 modified
   files. Sensible shape is more than one commit: the relayout, the install
   repoint, the board leaving the index.
2. **The manifest still names the old paths** — `references/files.md`'s
   `agents/` dispatch section and its two `@agents/...` rows, `index.md`'s
   `@@workers` row, `references/parts/workers.md` in prose, and nothing at all
   registering `references/skills/`. `pearde index` is loud until the docs-sweep
   PRD runs. Expected, not a regression — the PRD's body already names all of it.
3. **Run the loop.** The user's standing instruction from the round before this
   one was: create PRDs for the open points, **then use subagents**. The PRDs
   exist and eight are ready. The orchestrator dispatches `pearde-analyst` and
   `pearde-implementer` at loop steps 4 and 5 with `pearde brief <prd>` as the
   whole prompt — never by hand.
4. **The guard resolves the board wrongly, and this bit this round.** A `Write`
   to `.pearde/.state/round.md` from a cwd of `/Users/feb/dev/infra/pearde` was
   refused with "this session's board is /Users/feb/dev/infra/prds" — the guard
   walked up past this repo's own `.pearde/` and found the outer `infra` board's
   `prds/`. `plan.py`'s `find_board()` resolves it correctly; the guard does
   not. It is a real relayout miss in `resources/guard.py`, not a stale message,
   and it makes the skill's own tree unwritable through the guarded tools. Worth
   its own PRD.
5. **The guard's message names a path that no longer exists** — it tells the
   session to write `prds/.round.md`; the file is `.pearde/.state/round.md`,
   which is what `guard.py`'s `ROUND_FILE` already says. Prose the relayout
   missed. Belongs in the docs-sweep PRD.
6. The workflow finding on `.history.jsonl` vs `.transitions.jsonl` is still
   unread. It lives in the PRD `the-sweep-leaves-nothing-unregistered`, whose
   body carries the path to the output file.

## decided by the user, at the end of this round — the shape the next one builds

**The board is an orphan branch checked out at `.pearde/`.** Plan and code are
versioned in the same repository and pushed to the same remote, but never in
the same history: `main` holds the source tree and ignores `.pearde/`, while a
branch named `pearde` holds nothing but the board and is checked out *as* that
directory through a git worktree. Board work is written locally and pushed on
its own branch. That is what separates plan from code, and it replaces the
plain "ignore it and lose the history" reading of the previous instruction —
the `.gitignore` line stays exactly as it is, and it is what makes the nested
worktree invisible to `main`.

`.pearde/` already exists and holds the board, and `git worktree add` refuses a
directory that is not empty, so the move is: put the board aside, make the
worktree, put the board back.

    cd /Users/feb/dev/infra/pearde
    mv .pearde ../pearde-board-tmp
    git worktree add --orphan -b pearde .pearde     # git >= 2.42
    # older git: git worktree add --detach .pearde && cd .pearde
    #            && git checkout --orphan pearde && git rm -rf --cached .
    cp -R ../pearde-board-tmp/. .pearde/
    rm -rf ../pearde-board-tmp

Then, inside `.pearde/`, decide what that branch itself ignores before the
first commit. The board's regenerable parts are `.state/plan.json`,
`.state/view.html` and `wiki/` (graphify writes it); `.state/round.md`,
`.state/history.jsonl` and `.state/transitions.jsonl` are the board's own
record and are worth keeping. `.claims/` is live worker state and should go.

Two things to verify once it stands, because both are what would make this idea
fail quietly:

- `python3 resources/board/plan.py scan` from the repo root still finds the
  board. It should — the worktree changes nothing about the paths, only what
  `.pearde/.git` is — but the scan is the gate, as it was for the migration.
- `git status` on `main` still shows `.pearde/` as nothing at all. The
  `.gitignore` line covers it, and the `.pearde/.git` file the worktree writes
  sits inside the ignored directory.

The push in owed point 1 now has two halves: `main` for the source tree, and
`pearde` for the board. Do `main` first — the board branch is worthless if the
code that reads it is not on the remote.

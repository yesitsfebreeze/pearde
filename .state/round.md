# round — the board is finished. 53/53, 100%, nothing open

The user's instruction was **finish the board, then push.** It is finished:
`done 53/53 · 100% · derived 19/19 · open 0/74 · blocked 0`, every band of the
scan empty, `doctor` exit 0 with every row it owns `ok`, and `index`, `memos`,
`workflows` and `questions` all silent. The next round starts from a clean
board, not from here.

## What the round did

It began on wreckage that was not wreckage: the previous session died at its
budget with both repos dirty, two claims held by dead workers, and one PRD
analysed but with no `specs/` written. Every dirty hunk belonged to a PRD still
on the list, so all of it was finished rather than reverted. Nine PRDs closed.

| PRD | boxes | what it cost beyond pass one |
|---|---|---|
| the-collect-and-brief-harnesses-are-carried-across-the-layou | 6/6 | nothing — the unit was a proof: 101/101, 133/133, 104/104 |
| an-acceptance-box-that-cannot-fail-is-refused | 9/9 | its specs (the analyst wrote none); 4000-script differential, 0 false refusals |
| collect-commits-only-the-prd-s-own-edits-not-the-footprint-s | 7/7 | its fixture could never fail — 10 → 21 real assertions, plus a mutation proof |
| …/list-the-collects-the-repo-bug-orphaned | 5/5 | `orphans.py` landed; live run says branch-only residue is **0** |
| the-board-asks-for-itself/two-questions-start-a-drill | 13/13 | `spec-fixture.sh` built (30 checks); loop.md broke two pins, fixed |
| the-view-row-names-a-variable-that-exists | 4/4 | pinned why `--harnesses` never returns (below) |
| the-other-boards-move-once-and-the-script-goes | 11/11 | seven live boards migrated; the retirement question below |
| collect-commits-the-code-repo-not-the-board-repo-twice | container | closed on its children |
| the-board-asks-for-itself | container | closed on its children |

## Three orchestrator acts a later round should know about

1. **Board commit `c15b234`, made by hand.** spec03 deleted `probe/migrate.py`
   on the premise that board history held it. It did not — `probe/` was
   untracked — so the deletion would have destroyed the only copy. The probe
   was committed first; the deletion is a retirement. The worker verified the
   blob before removing anything.
2. **Three spec footprints rewritten** on
   `the-other-boards-move-once-and-the-script-goes`, because `collect` refused
   them and was right to. spec01 and spec03 named the retired probe (probe code
   is never a footprint); spec02 named seven absolute board roots in *other*
   repositories, which this board must never commit. All three now say
   `footprint:` with a comment explaining what replaced it. The seven roots and
   their staged-rename counts live in that PRD's `report.md`.
3. **`context-budget` was raised 160k → 700k** for this run, on the user's
   instruction, and **restored to 160k** at the end of it.

## The migration, as it stands on disk

Seven boards moved from `prds/` to `.pearde/`, counts matching exactly:
mitosys 135, model 82, realm 19, shared 17, manola 49, racer/.mi 48, infra 20
own / 273 merged; dotfiles 196 untouched. 8/8 gates green, all four `@member/`
sigils present, 9/9 registry rows live. **Six of those repos hold uncommitted
staged renames** (mitosys 303, manola 253, model 173, infra 118, shared 70,
realm 64; racer's board is untracked). That is deliberate — nothing was
committed or pushed outside pearde — and each repo's owner decides. Until
tonight seven of the nine boards in `serve.json` read as **zero PRDs** under
`plan._scan_one`; that blindness is what the move closed.

## Defects found, recorded, deliberately not taken

The round was told to finish the board, not grow it. Each of these is real:

1. **`collect` hangs forever** on a verify block whose child leaves a process
   holding the captured stdout pipe — `run()` is
   `subprocess.run(capture_output=True)`, so `communicate()` waits on EOF, not
   on exit. Diagnosed with `faulthandler.dump_traceback_later` on a `collect
   --dry` sitting at 0% CPU: `collect.py:930 → :243`. It is also why
   `doctor.sh --harnesses` never returns — the graph PRD's probe runs
   `graphify extract` unbounded and blocks the row's `wait`, which had been
   wrongly blamed on a dirty `doctor.sh`. Wants a per-block timeout and a
   `start_new_session` process group `collect` kills on the way out. **This is
   the one to fix first.**
2. **`collect --dry` does not refuse a footprint of board paths.** It routes
   them to the code repo, which `.gitignore:17` ignores, so an edit to such a
   file is committed by neither repo — silently — while the dry run prints
   `would add: (clean)`. Acts 2 above is the same hole seen from the other side.
3. `the-board-runs-itself/transitions-are-commands/probe/verify.sh` is 66/74:
   its fixture board carries 4 unput questions, so the new drill gate correctly
   refuses its `claim next impl-1`. One line in that fixture.
4. `references/parts/order.md` still says the scan prints "five sections" and
   names no drill band. `references/parts/handles.md` has no `orphans` row.
5. `migrate.py --serve` alone is a silent no-op (exits 2 with usage);
   collisions are named but never warned; dotfiles has a leftover empty `prds/`.
6. Two unrelated PRDs both named a probe `migrate.py`, which made spec03's
   name-based `find` print `LEFTOVER migrate.py FOUND` against a `done`
   sibling's file. The box was ticked on the check it means, with the raw
   output and the collision written into the report.
7. dotfiles `06-help/06-manual-markdown` — two footprint files on disk, never
   committed. The one flag the orphan scan raised that a person should look at.

## Hazards that outlive this round

- The shell is **zsh**: unquoted `$var` does NOT word-split, and `set -- $pair`
  silently does nothing. `timeout` does not exist on this machine.
- Every board command needs `--as engineer`. `scan` takes none; `settings`
  refuses it. `brief` needs `--worker <the claim's holder>`, not `--force`.
- The guard refuses a **glob** over `.pearde/prds/` but allows a named path.
  Walk the board with `scan`, read one file by name.
- Verify blocks run `bash -e -o pipefail` from the code repo on stdin, and
  `specced` now refuses a block that cannot redden. Probe code never goes in
  `footprint:`.
- `.pearde` is a git WORKTREE of the same repository (branch `pearde`); the
  code worktree is on `main`. One store, two branches — any "does repo X hold
  sha Y" check must be per-branch, never `git log --all`.

## Asked

- **Do I run the migration over the seven other repositories?** — put with
  every repo named, the `git mv`, the registry rewrite and the two boards
  holding live claims. **Answered: run all seven now.** Acted on and closed.

Nothing is out to the user.

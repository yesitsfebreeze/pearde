# Report — example-writes-a-board-on-the-pearde-layout

**Verdict: DONE** — 1 spec, boxes 6/6, all six re-run by the implementer
against what is on disk now. Nothing unticked.

## What is on disk

The fix is in both footprint files and is correct:

- `resources/board/plan.py` `cmd_example` — `board = os.path.join(dest,
  BOARD_DIR)` (:2427), `shutil.copytree(EXAMPLE, board, …)` (:2428), and the
  reported line is `os.path.join(board, PRDS_DIR)` (:2434).
- `resources/board/viewtest.js` (:47, :50-56) — copies into
  `path.join(scratch, ".pearde")`, then takes the path off the last
  `gantt: <path>` line `plan.py gantt` actually printed rather than guessing
  `<scratch>/prds/.view.html`.

## Re-verification, box by box

Every box below was run by me in this session; the analyst had pre-ticked all
six. All six held.

1. **board lands at `<dir>/.pearde/`** — `plan.py example /tmp/b1` exit 0,
   printed `example: /tmp/b1/.pearde/prds`. `ls -a /tmp/b1` → `.pearde` and
   nothing else; `.pearde/` holds `settings.md`, `prds`, `memos`,
   `workflows`, `README.md`. Nothing of the board at the dest root.
2. **both printed lines name real things** — the reported path resolves
   (`test -d` ok); the follow-up it prints, `plan.py scan /tmp/b1`, exits 0
   and prints `board: /tmp/b1/.pearde · 8 PRDs · workers=1` with the example
   PRDs by their own names (`finished`, `asking`, `building`, `big`,
   `big/second`, `next`). `pearde.py example /tmp/b4` — the real dispatcher —
   routes through the same code, exit 0, `.pearde/prds` present.
3. **`node viewtest.js --example`** — exit 0, `45/45 passed`, zero `FAIL`
   lines. Checked it renders the *copy*, not this repo's board: `plan.py
   gantt` on a hand-made copy prints `gantt: /tmp/gtest/.pearde/.state/
   view.html`, inside the copy, and the run's own assertions read the
   example's single ask card (`no ask card failed to read its PRD (0 of 1)`).
4. **`doctor.sh --harnesses` `jstests` row** — `jstests ok  viewtest.js
   --example · 45/45 passed`. (`doctor` exits 1 overall on the unrelated
   `skills` row; the row this box names is `ok`.) Confirmed the concurrent
   uncommitted edits to `resources/doctor.sh` from another PRD do not touch
   the `jstests` block — `git diff resources/doctor.sh` has no `jstests` hit.
5. **`init.py` unchanged, `init --example` still correct** — `git status
   --short` and `git diff --stat` on `resources/board/init.py` are both
   empty. `init.py init /tmp/b5 --example` exit 0, `/tmp/b5/.pearde/prds`
   holds the example PRDs; its own trailing doctor reports `board ok`.
6. **no writer left putting `prds/` at a dest root; `example/` untouched** —
   the three copy sites are `plan.py:2428` → `dest/.pearde`,
   `viewtest.js:47` → `scratch/.pearde`, `init.py:125` → `dest/.pearde`. All
   three write into a `.pearde`. `git status --porcelain
   --untracked-files=all resources/board/example/` is empty (checked with
   untracked files included, not only `git diff --quiet` as the spec's block
   does); 16 files tracked, 16 on disk.

Ran the spec's `## Verify and Proof` block verbatim, twice: bare, exit 0; and
with `playwright-core` reachable so the node half executes, exit 0 with
`45/45 passed` and the block's own `grep -Eq "jstests +ok"` satisfied under
`set -e`. The block ends on an explicit `echo`, so `collect` reads 0.

## For the orchestrator — the plan.py half is already committed, under another PRD

`resources/board/plan.py` is **not** in the working tree's diff. Its
`cmd_example` fix — this PRD's work — was swept into commit `2c8cb84`
("state-dir-belongs-to-the-board"):

    git show 2c8cb84 -- resources/board/plan.py
    +    board = os.path.join(dest, BOARD_DIR)
    -        shutil.copytree(EXAMPLE, dest, dirs_exist_ok=True)
    +        shutil.copytree(EXAMPLE, board, dirs_exist_ok=True)
    -    print(f"example: {os.path.join(dest, 'prds')}")
    +    print(f"example: {os.path.join(board, PRDS_DIR)}")

So `collect` will find only `resources/board/viewtest.js` uncommitted for
this PRD. The contract is met on disk either way, but half of it is in
history under a neighbouring PRD's message.

## Weakness in this spec's own verify block

The block's boxes 3 and 4 sit behind
`node -e "require.resolve('playwright-core')"`. `playwright-core` is
installed nowhere on this machine — not in `resources/`, not in any
`node_modules`, not global — so on a bare run the block takes the `else`
branch, prints its skip line and exits 0 having exercised **4 of 6 boxes**.
A green from `collect` here is not evidence for boxes 3 and 4.

I ran them anyway rather than leaving them on the analyst's word: installed
`playwright-core` into the session scratchpad and ran both with `NODE_PATH`
pointed at it. Nothing was added to the repo — no `node_modules`, no
`package.json`, no change to `.gitignore`. Both boxes genuinely pass. Left
the block as written, since the optional-dev-dependency skip is deliberate
and matches `doctor`'s own `off` row; flagging it so the board does not read
a bare-run green as covering all six.

## Finding, outside scope, not fixed

Carried forward from the spec round and re-confirmed: `plan.py`'s docstring
(:6, `render the view to prds/.view.html`) and `render.py`'s module docstring
(:4) both name a path the code has not used since the state dir moved — the
real constant is `.state/view.html` (`render.py:40`), and `gantt` prints
`<board>/.pearde/.state/view.html`. Pre-existing drift about `gantt`, not
about `example`; `viewtest.js` sidesteps it by reading the printed path.
`plan.py`'s docstring lines 13-15 and `example/README.md` line 5, which
document *this* command, are both still accurate and needed no edit.

## Scores

complexity: 8
blast-radius: mid
workflow: none fit

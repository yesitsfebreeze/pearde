# a-collect-does-not-stage-a-tracked-but-ignored-probe-file — implementer

Verdict: DONE

specs 1/1 · boxes 2/2 · files 1 · lane lane/a-collect-does-not-stage-a-tracked-but-ignored-probe-file

## spec01 — collect's own `git add` no longer refuses a tracked-but-ignored path

Both boxes ticked, both run.

- [x] `git_out(root, "add", "-f", "--", *p["add"])` at the PRD-folder staging
      step in `cmd_collect` — the only change.

  ```
  $ grep -n 'git_out(root, "add", "-f", "--", \*p\["add"\])' resources/board/collect.py
  2337:            git_out(root, "add", "-f", "--", *p["add"])
  ```

  `git diff --stat` on the lane: `resources/board/collect.py | 12 +++++++++++-`
  — one changed line plus the comment naming why `-f` is scoped-safe. The
  three other `git_out(..., "add", ...)` sites and `land_lane`'s add are
  untouched, as the spec requires.

- [x] `probe/reproduce.py` exits 0 against the patched file.

  ```
  $ python3 prds/.../probe/reproduce.py
  dirty_paths() sees it: 'tracked'
  no `-f`: collect.git_out(..., "add", ...) raised: git add failed in
    /var/folders/.../repro-tracked-ignored-xgqdo0z1: The following paths are
    ignored by one of your .gitignore files:
  prds/foo/probe
  hint: Use -f if you really want to add them.
  staged after the fixed call (`-f`): True
  PASS: `git_out(root, "add", "-f", "--", *p["add"])` — collect.py:2337 —
    stages the tracked-but-ignored probe file that the unpatched call refused
  exit 0
  ```

## Why `-f` cannot widen the sweep

Checked at the source rather than taken from the spec. `p["add"]` comes off
`dirty_paths()`, which reads `git status --porcelain -uall -z` (collect.py
:1243) with no `--ignored`. Git never lists an untracked-ignored file in that
output, so no fresh ignored file can reach the call site; `-f` only unblocks
paths git already reported as dirty. Root cause and symptom are the same
line — there is no sibling caller of this shape to fix.

## Gate

- Two collect harnesses run from the lane, both green:
  `collect-stages-a-shared-file-whole` — `32 passed, 0 failed`, exit 0;
  `collect-must-not-reset-the-checkout-it-did-not-write` — `31 checks · 31
  pass · 0 fail`.
- `bash resources/doctor.sh` from the lane: every row that reads code is
  `ok` (skills, plugins, workflows, grammar, health, briefs, board, view,
  plan). The red rows are board state, not this diff — see below.

## Defects outside scope (not fixed, reported)

Pre-existing doctor reds, none in the footprint and none touched by this
change: `index` (5 problems), `claims` (16 drifted names), `vault` (the
board is a dot-segment path Obsidian skips), `origin` (8 derived PRDs with
no `from:`), `memos` (43 of 44 missing generated `tags:` — `memos.py retag`
writes them), `knowledge` (graph.json behind the files — `knowledge.py
relink`), `questions` (3 PRDs with `## Answers` and no `## Questions`).

Layout oddity worth an orchestrator's eye: the lane worktree carries its own
untracked copy of the PRD folder at `prds/<prd>/` while the board's copy is
at `.pearde/prds/<prd>/`. They were byte-identical; both acceptance boxes
were ticked in both so neither view is stale whichever one `collect` reads.

## Health floor

Brief listed nothing under the floor in the footprint. `collect.py` was
edited by one line inside the spec's scope; nothing moved.

## Knowledge

`knowledge.py query` had no note on the git behaviour (107 notes, nothing
on the ignored-pathspec refusal). Written back as `[[260903-eb7e]]` —
"git add refuses an explicit pathspec under an ignored directory even when
the file is tracked", with the status/`--ignored` asymmetry that makes `-f`
safe there.

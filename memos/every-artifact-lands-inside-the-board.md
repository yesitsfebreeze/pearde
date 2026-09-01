---
memo: every-artifact-lands-inside-the-board
kind: invariant    # decision | note | invariant
status: decided    # open | decided | superseded
subject: every file the tool writes into a project lands under that project's .pearde/
date: 2026-09-01
verify: bash resources/invariants/every-artifact-lands-inside-the-board.sh
# updated:         # only on a substantive revision; never for a path fix
# prds:            # board-relative PRD dirs this memo governs
#   - <prd-dir>
# supersedes:      # the slug this replaces
# superseded_by:   # the slug that replaced this
---
<!-- Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a
     typo and @resources/doctor.sh fails on it. @references/memo.md is the
     format. -->

# every-artifact-lands-inside-the-board — the board is the only place the tool writes

## Decision

Every file pearde creates in a project lands under that project's `.pearde/`.
The board holds `prds/`, `memos/`, `workflows/`, `wiki/`, `settings.md`,
`vision.md` and `report.md`; `.pearde/.state/` holds the machine-local corner —
`plan.json`, `parse-cache.json`, `view.html`, `history.jsonl`,
`transitions.jsonl`, `round.md` and any `round.<what-you-are-on>.md`. Nothing
of ours is written beside the board.

Two things make it hold rather than being asked for:

- **One spelling.** Every writer goes through `plan.py state_dir(board)`,
  which returns `<board>/.state` and makes it. `.state/…` written on its own
  is a relative path and resolves against the working directory — the repo
  root, one level above the board — so it is never written on its own.
- **One guard.** `guard.py board_artifact_astray()` refuses an `Edit|Write`
  of a board file (`round*.md`, `ask.md`, `plan.json`, `parse-cache.json`,
  `history.jsonl`, `transitions.jsonl`, `view.html`) into a `.state/` that is
  not the board's, and names the path it belongs at. A round writing its own
  memory by hand is the only actor `state_dir` cannot reach.

One exception, named because it is not board content: `init` appends the
machine-local names to the **parent repo's** `.gitignore`. An ignore rule has
to sit in a file git reads, and git reads the repo root's.

## Why

An untracked `<repo>/.state/round.md` appeared here on 2026-09-01: a session
wrote its round memory to the path the guard's own refusal messages and half
the manual spelled — `.state/round.md`, relative — from a working directory
one level above the board. Nothing reads that path. The next session finds no
round file, the file is in no `.gitignore`, and it shows up as untracked noise
in a `git status` that four other sessions are reading.

The failure is cheap to make and silent to have. A relative `.state/` is
correct-looking in every sentence that names it and wrong in every process
whose cwd is the repo root — which is all of them, the daemon included: a
`state_dir` broken to be cwd-rooted for three seconds during this memo's own
testing had the daemon writing `<repo>/.state/plan.json` before the edit was
undone.

So the rule is not a sentence. `state_dir(board)` is where the code cannot
spell it wrong, the guard is where a round cannot, and `verify:` drives the
whole command surface against a throwaway project and diffs the tree — a new
writer that gets it wrong is named by path on the next run.

## Alternatives considered

**Fixing the one path the report named** (`doctor.sh` reading
`$BOARD/.plan.json`) — it turned out already correct and board-rooted, and
patching it would have left the class untouched. The board has a PRD family
about checks that cannot fail; a fix aimed at a symptom is the same mistake in
another key.

**A `.gitignore` entry for `/.state/`** — hides the break instead of stopping
it. The file would still be written, still be read by nothing, and the next
session would still lose its handover. Ignoring an artifact is not the same as
not making one.

**Auditing every `open(…, "w")` by eye and calling it done** — was done, and
found every code writer already board-rooted. It proves the tree at one
instant and nothing about the next writer somebody adds. The driven-project
check in `verify:` is the same audit, repeatable.

**Widening the guard to any path with a `.state` component** — refuses a
project that keeps a `.state/` of its own for unrelated reasons. The rule
matches the board's own basenames only: the guard refuses what it can prove.

## Consequences

- A new writer must take a `board` argument and route through `state_dir`.
  Convenience functions that write from an ambient cwd are not available.
- `verify:` runs the real command surface against a real temp project — about
  3 seconds and a `git init`, so it is a `memo verify` cost, not a per-call
  one. It registers a board with the daemon and calls `serve.py forget` after;
  a machine with no daemon runs it just the same.
- It does **not** settle machine-local install state. `plan.py MACHINE_DIR`
  (`resources/board/state/` — `serve.json`, `serve.log`, `calibration.json`,
  the guard's session cache) is pearde-created and lives inside the install,
  outside every `.pearde/`, because one daemon watches many boards. Whether
  that is exempt or moves to `~/.pearde/` is open with the user as of
  2026-09-01, and the check above deliberately says nothing about it.
- It does not cover what a *worker* writes while building a feature. This is
  about the tool's own artifacts.

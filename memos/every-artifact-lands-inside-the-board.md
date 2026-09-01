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
`transitions.jsonl`, `round.md` and any `round.<what-you-are-on>.md` — and,
since the install stopped being writable, `serve.json` (this board's own
registration with the daemon), `serve.log`, `run-<prd>.log`,
`calibration.json` and `guard/<session>.json`. Nothing of ours is written
beside the board, and nothing of ours is written into the install.

Two things make it hold rather than being asked for:

- **One spelling.** Every writer goes through `plan.py state_dir(board)`,
  which returns `<board>/.state` and makes it. `.state/…` written on its own
  is a relative path and resolves against the working directory — the repo
  root, one level above the board — so it is never written on its own.
- **One root.** There is no path pearde writes that is not relative to a
  board. The install directory used to be the exception and is not any more —
  `resources/board/state/` is deleted, and `verify:` fails if it comes back or
  if any command puts a byte into `resources/`.
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

## What the install's four files became

`resources/board/state/` held four things, and each one had to go somewhere
that is a board.

| was | is | cost |
| --- | --- | --- |
| `calibration.json` — one fit pooled over every registered board | `<board>/.state/calibration.json`, fitted from that board's own done PRDs and its members' | the sample is smaller. It is also honest: a board's own record is the better predictor of that board, and the pooled fit needed a machine-wide list of boards to read, which is the thing being removed |
| the guard's session cache | `<board>/.state/guard/<session>.json` | a session that works two boards writes a file in each. `plan.py guard_sessions(board)` reads one board's, so "the newest session" now means the newest session *on this board* — which is what every caller meant |
| `serve.log` | `<board>/.state/serve.log` of the board whose `ensure` started the daemon, named to the child through `PEARDE_SERVE_LOG` | the daemon watches many boards and logs into one of them. Arbitrary, but inside a `.pearde/` and owned by the board that asked for it |
| `serve.json` — the registry of every board the daemon watches | nothing global. Each board writes its own `<board>/.state/serve.json` saying it is watched; the daemon holds the union in memory only | below |

**The registry is the one that needed a design, not a path swap.** The daemon
is a singleton — one per machine, by port bind — so a list of every board it
watches belongs to no board. There is now no such list. A board records only
its own registration, and the daemon's watch set lives in memory.

Two things keep that from being a regression:

- **`ensure` is safe on every session start**, and is what `pearde view`,
  `pearde init` and every doctor fix already run. A board re-announces itself
  whenever a session opens on it, so the set rebuilds from the sessions that
  actually care about it.
- **A hot reload hands the set forward.** `restart()` re-execs the daemon
  whenever its source moves — several times an hour while pearde itself is
  being worked on — and that used to be safe because `run` reloaded the
  registry file. It now execs `run <board>…` with the paths it is watching. A
  process passing its own state to itself needs no file outside a board, and
  the set survives every reload.

**The honest cost:** a daemon that is *stopped and started* — not reloaded —
watches nothing until each board is `ensure`d again. A board nobody opens a
view on stops being mirrored, silently. That is accepted: the daemon exists to
serve the view, `ensure` is the first thing the view does, and so the set
self-heals at exactly the moment it matters. The failure is a board that is
watched for a background reason nobody is looking at — history rows and plan
reconciliation — going unwatched between a daemon restart and the next
session. It is real, and it is smaller than a file outside every board.

## Alternatives considered for the registry

**Keeping `MACHINE_DIR` as a named exemption** — the shape the memo had until
this revision, with the question left open. It beats nothing: an invariant
with a hole in it does not fail on the writer that widens the hole, and the
next machine-local thing would have landed in the same directory by
precedent.

**Moving the list to `~/.pearde/`** — a different absolute path is the same
mistake with a better address. It is still a root that is not the board, still
a place a writer can reach without a `board` argument, and it makes the tool
own state a person cannot find by looking at their project.

**Rediscovering boards at daemon boot by walking the filesystem** — a scan for
`.pearde/` directories under the home dir. Expensive, wrong (it finds boards
nobody asked to watch), and it still needs somewhere to remember the roots to
scan.

## Consequences

- A new writer must take a `board` argument and route through `state_dir`.
  Convenience functions that write from an ambient cwd are not available.
- `verify:` runs the real command surface against a real temp project — about
  3 seconds and a `git init`, so it is a `memo verify` cost, not a per-call
  one. It registers a board with the daemon and calls `serve.py forget` after;
  a machine with no daemon runs it just the same.
- **The install is not exempt.** `plan.py MACHINE_DIR`
  (`resources/board/state/` — `serve.json`, `serve.log`, `calibration.json`,
  the guard's session cache) was the one place pearde wrote outside every
  `.pearde/`. It is deleted. The user settled it on 2026-09-01: *"We don't
  need constants or absolute. We just need the `.pearde` folder and
  everything we write, we write into it."* Each of the four moved to
  `<board>/.state/`, `verify:` now has two checks that fail if anything lands
  in the install again, and an older install's directory is moved into the
  boards it was holding state for and deleted on the next run.
- It does not cover what a *worker* writes while building a feature. This is
  about the tool's own artifacts.

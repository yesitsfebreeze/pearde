---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 85        # higher first
complexity: 18      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.11h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
commit: fe4340c 2c8cb84
---
<!-- Ordering reads three axes and no clock: dependency (needs + footprint),
     vision importance (priority), and complexity/blast-radius. Add your own
     keys freely, at any nesting. Nothing outside state, origin, from,
     priority, complexity, blast-radius, claim, repo, workflow, needs and
     footprint is read, and nothing you add is ever dropped.
       needs:     — PRD dir names this one depends on. A hard gate in `plan`
       footprint: — paths this PRD touches. The overlap check
       workflow:  — the route a worker is handed, expanded into its brief

     One sitting is the limit: specs summing `complexity` above `split-above`
     or counting above `specs-above` (both in prds/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# state dir belongs to the board

When this is done, one rule holds everywhere: state that belongs to a board is
written under that board's `.state/`, and state that belongs to the machine is
written once, outside any board, through a name that says so. Today neither
half of that is true. `resources/board/plan.py:61` declares
`STATE_DIR = ".state"` and `state_dir(board)` (lines 65-69) joins the board root
with it — but line 1296 rebinds the same module global to
`os.path.join(os.path.dirname(os.path.abspath(__file__)), "state")`, the code
repo's own `resources/board/state`. `state_dir()` reads that global at call
time, so after import it returns the code-repo path for every board it is ever
handed. Importing the module and calling it proves the point: `state_dir(<any
tmp dir>)` returns `/Users/feb/dev/infra/pearde/resources/board/state` and
creates nothing under the board. This matters because it silently merges every
board's plan into one file — a per-project tool quietly turned global.

The measured evidence is a divergence you can read off disk. `load_map` and
`save_map` (plan.py:987 and 995) are the only users of `state_dir()`, so the
schedule lands in the wrong repo: `resources/board/state/plan.json` currently
holds the test fixture's PRD names (`asking`, `big`, `big/second`, `building`,
`finished`, `next`) and was written most recently, while
`.pearde/.state/plan.json` still holds the real board's PRDs and is hours older.
The constants bound *before* the rebinding escaped it and are correct:
`ROUND_FILE` (plan.py:640), `HISTORY_FILE` (1144) and `TRANSITIONS_FILE` (1166)
are all relative `.state/...` paths, joined against the board at each use, which
is why `.pearde/.state/` really does hold `history.jsonl`, `transitions.jsonl`,
`round.md` and `view.html` today. `resources/board/init.py:138-142` already
carries a comment naming this reassignment and working around it by hardcoding
the literal `".state"` at line 143 — the workaround is the bug report.

The second location is deliberate and mostly correct. `resources/guard.py:37-38`
defaults `STATE` to `ROOT/board/state/guard` with a `PEARDE_GUARD_STATE`
override; `git show HEAD:resources/guard.py` returns the same lines, so this is
the committed default and not a rename left behind. `resources/board/plan.py:1195`
duplicates that default as `GUARD_DIR` and only reads from it (`guard_sessions`,
1204-1208), as does `resources/board/transitions.py:482`.
`resources/board/serve.py:115-117` points `APP_DIR` at the same directory for
`serve.json`, `serve.log` and `run-<name>.log`, and `cmd_calibrate`
(plan.py:1373-1374) writes `calibration.json` there. Every one of those is
genuinely machine-scoped: the guard cache is per session, the serve registry
lists every board the daemon serves, and plan.py's own comment at 1290-1294
states the calibration constant is "one constant per machine, not per board".
`resources/board/state/` is gitignored and `git ls-files` returns nothing for
it, so nothing here is a tracked-file move.

The non-goals are therefore sharp. `calibration.json`, `serve.json`,
`serve.log`, `run-*.log` and the `guard/` session cache must NOT move into any
board — a board-scoped calibration would refit per project and a board-scoped
registry could not name its siblings. `PEARDE_GUARD_STATE` must keep working
exactly as it does, because `resources/doctor.sh:260-263` sets it to a
`mktemp -d` so the guard probe does not litter the repo it is checking. Do not
change what `.state/round.md` contains or who writes it; do not rename the
`.state` files; do not un-ignore either directory. The one thing that must move
is `plan.json` — back under the board, where `state_dir()`'s own docstring
already says every writer goes. Whether the machine-scoped corner should also
leave the code repo is a separate contract, not this one.

Pointers: `resources/board/plan.py` (lines 55-69, 640, 987-995, 1144, 1166,
1190-1208, 1290-1300, 1373-1384), `resources/guard.py` (35-45, 217-219, 627,
653), `resources/board/serve.py` (108-117, 386, 1053-1055, 1134),
`resources/board/render.py:40`, `resources/board/transitions.py` (70, 414-425,
482, 798), `resources/board/init.py` (63, 118, 138-143), `resources/doctor.sh`
(255-263), and the repo `.gitignore`. Two locations, six files writing state,
eight distinct writing call sites between them.

## Acceptance sketch, for the analyst

- `resources/board/plan.py` binds the name `STATE_DIR` exactly once, and the
  machine-scoped directory used by `CALIB_PATH`, `GUARD_DIR` and `serve.json`
  is reached through a differently named constant.
- Importing `resources/board/plan.py` and calling `state_dir(d)` for a fresh
  temporary directory `d` returns a path under `d` and creates it there.
- `pearde plan` on a board writes that board's `plan.json` under its own
  `.state/`, and running it on two different boards leaves two separate
  `plan.json` files with no shared content.
- `resources/board/init.py:143` no longer needs its literal `".state"`
  workaround: it can name the planner's constant and the comment at 138-142
  goes with the fix.
- `calibration.json`, `serve.json`, `serve.log` and `guard/` are still written
  to the same machine-scoped directory as before, `PEARDE_GUARD_STATE` still
  redirects the guard, and `resources/doctor.sh` still reports the guard row ok.

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one round in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     one `(recommended)`. Only real forks the user must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such round never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a round that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the round above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

## Report

spec01: exit 0
61:STATE_DIR = ".state"
state_dir/MACHINE_DIR OK
STATE_DIR joins are board files only: ['history.jsonl', 'round.md', 'transitions.jsonl']
serve.json/serve.log machine-scoped OK
machine dir still gitignored
PEARDE_GUARD_STATE still overrides both
verify-ok

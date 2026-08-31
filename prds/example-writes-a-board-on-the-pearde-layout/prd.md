---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 55        # higher first
complexity: 8      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.08h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
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

# example writes a board on the pearde layout

Every command that hands a person a copy of the example board hands them a
board on the `.pearde/` layout — one that the very next command printed
alongside it actually reads. Today `pearde example <dir>` writes a board the
tool cannot open, and prints a follow-up command that exits 2. This is the
quickstart's second door: a first-time reader who takes it is told, by the
tool itself, that the board it just wrote does not exist.

The premise this PRD was filed on is stale and must not be re-fixed. `init` is
already correct: `write_board()` in `resources/board/init.py` (the `if
"example" in args.flags` branch, around line 121) copies `EXAMPLE` into
`board`, and `cmd_init` sets `board = os.path.join(d, ".pearde")` (line 279).
Measured — `python3 resources/board/init.py init /tmp/ex2 --example` wrote
`/tmp/ex2/.pearde/settings.md`, `.pearde/vision.md` and `.pearde/prds/`, and
the `doctor` run it ends with reported `board ok /tmp/ex2/.pearde/prds · 8
PRDs · language English`. The sibling PRD `init-writes-a-board-on-the-pearde-
layout` is landed; do not touch that code path.

The remaining offender is the `example` path in `resources/board/plan.py`.
`EXAMPLE` is defined at line 2387 and `cmd_example` at line 2390; line 2415 is
`shutil.copytree(EXAMPLE, dest, dirs_exist_ok=True)` — straight into `dest`,
with no `.pearde/` between them — and lines 2420–2421 then print
`example: <dest>/prds` and `python3 …/plan.py scan <dest>`. Since
`resources/board/example/` is itself a board root (`settings.md`, `prds/`,
`memos/`, `workflows/`), the copy lands one level too high: the board's own
`prds/` becomes `<dest>/prds`, and `find_board` (line 78, against
`BOARD_DIR = ".pearde"` at line 60) accepts only a path named `.pearde` or a
directory holding one. Measured — `plan.py example /tmp/ex1` printed
`example: /tmp/ex1/prds`, and the command it printed on the next line,
`plan.py scan /tmp/ex1`, answered `pearde: no .pearde/ board at /tmp/ex1` and
exited 2. This is a live user-facing command, not dead code: `COMMANDS`
registers it at line 2429, `main()` special-cases it at line 2436, and
`resources/pearde.py`'s `discover()` (line 103) routes `pearde example`
through it — verified by running `pearde.py example /tmp/ex4`, same result.

One other place copies the example tree and reads it back with the same
mistake, and it is in scope because it is the same contract: `resources/board/
viewtest.js` lines 45–56 copies `resources/board/example` into a mkdtemp root,
runs `plan.py gantt <scratch>`, and expects `<scratch>/prds/.view.html`.
Reproduced by hand — copying the tree to `/tmp/ex3` and running `plan.py gantt
/tmp/ex3` gives `no .pearde/ board at /tmp/ex3`, exit 2. `resources/doctor.sh`
lines 725–730 runs `node viewtest.js --example` for its `jstests` row, so that
row cannot pass today; it is only opt-in behind `--harnesses`, which is why the
breakage has stayed quiet.

Constraints and non-goals. Do not restructure `resources/board/example/` on
disk — it is a board root by design, which is exactly the shape `init` copies
into `.pearde/`, and moving it would break the landed `init` path. Do not add
dual-layout or old-`prds/`-root fallback anywhere; the decision on record is a
single layout. Do not touch `init.py`. Do not widen this into the probe
harnesses that live under a PRD folder — that is the neighbouring PRD
`every-probe-harness-is-re-aimed-at-the-pearde-layout`. Whether `README.md`
should be filtered out of the copy the way `init` filters it
(`ignore_patterns("README.md")`) is not this contract's business either way.
Pointers: `resources/board/plan.py` (`cmd_example`, `EXAMPLE`, `find_board`,
`BOARD_DIR`, `PRDS_DIR`), `resources/board/viewtest.js`, `resources/doctor.sh`
(the `jstests` row), `resources/board/example/README.md` line 5 and
`plan.py`'s own docstring lines 13–15, both of which document the command.

## Acceptance sketch, for the analyst

- `python3 resources/board/plan.py example <empty dir>` leaves a board at
  `<dir>/.pearde/` — `settings.md` and `prds/` inside it, nothing of the board
  at `<dir>/` itself.
- The two lines that command prints name real things: the board path it
  reports resolves on disk, and the follow-up command it prints exits 0 and
  lists the example PRDs by their own names.
- `node resources/board/viewtest.js --example` exits 0 and renders the copied
  example board, and `bash resources/doctor.sh --harnesses <dir>` reports the
  `jstests` row `ok` rather than `broken`.
- `resources/board/init.py` is unchanged by this PRD, and `init <dir>
  --example` still produces `<dir>/.pearde/prds` with the example PRDs in it.
- `grep -rn "example" resources/` turns up no remaining writer of an example
  board that puts `prds/` at the destination root, and `resources/board/
  example/` is byte-identical to what it is today.

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
example: /tmp/spec01-ex1/.pearde/prds
      python3 /Users/feb/dev/infra/pearde/resources/board/plan.py scan /tmp/spec01-ex1
example: /tmp/spec01-ex4/.pearde/prds
      python3 /Users/feb/dev/infra/pearde/resources/board/plan.py scan /tmp/spec01-ex4
spec01: node/playwright-core unavailable here — viewtest.js/doctor jstests row not exercised in this run
board example · language English — pearde settings language=<l> changes it
init: wrote /tmp/spec01-init/.pearde/settings.md and vision.md from the example board
init: board/ -> .pearde/ — Obsidian hides a dot-directory, and this is the name it will show
init: obsidian vault at .obsidian/ — plugins: dataview, obsidian-local-rest-api · dataview serves the live views from the first open, local-rest-api (local-rest-api with MCP) answers on 127.0.0.1:27124 (key: .pearde/wiki/.obsidian-api-key) after Obsidian loads the vault once
serve: watching example · /tmp/spec01-init/.pearde · live view http://127.0.0.1:8443/board/example
pearde doctor — /tmp/spec01-init

  skills      broken  skills/ holds no .md file — there is nothing to install
                      fix: one file per skill, frontmatter name: matching the file name, and description:
  plugins     ok      4 suggested · all installed on this machine
  index       ok      118 files · 31 keywords · every anchor resolves
  statusline  ok      /tmp/spec01-init
                      wire it where your setup runs a command for one — @references/install.md
  board       ok      /tmp/spec01-init/.pearde/prds · 8 PRDs · language English
  vision      ok      vision declared · no terminals — no axis
  origin      ok      8 requested · nothing derived
  memos       ok      1 memos · frontmatter checks out
  workflows   ok      1 workflow · 2 atomics · the library checks out
  briefs      ok      5 blocks in references/parts/workers.md · every placeholder named
  questions   ok      1 PRD carries a round · each asks and offers an answer
  view        ok      watching · http://127.0.0.1:8443/board/example
  plan        off     no plan on record — the view has no bars until there is one
                      fix: python3 /Users/feb/dev/infra/pearde/resources/board/plan.py plan /tmp/spec01-init/.pearde
  harnesses   off     no verify.sh under /tmp/spec01-init/.pearde — a PRD gets one when it is specced
  jstests     off     not run — opt in: bash /Users/feb/dev/infra/pearde/resources/doctor.sh --harnesses /tmp/spec01-init

pearde: something is installed and not working — the fixes are above.
pearde guard on — optional, refuses the waste the loop's rules name
http://127.0.0.1:8443/board/example
pearde add "<title>"
pearde
spec01 verify: all checks passed

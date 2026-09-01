---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 10        # higher first
complexity: 22      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.25h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
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
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# `scan` parses the board once and caches it by mtime

Measured on this board on 2026-09-01, 75 PRDs: `pearde scan` takes 142–173 ms,
of which the python3 interpreter start is 10 ms. The remaining ~140 ms is
re-reading and re-parsing every `prd.md` and every spec's frontmatter, on every
call — and `scan` is step 1 of every round, plus the status line, plus the view
daemon.

This PRD exists because it is the honest answer to "would a compiled binary be
faster". It would be, by roughly the amount this cache is worth, and at the
price of a build step between an edit and its effect — which the install cannot
afford, since it is file-by-file symlinks into this repo and a round on any
board on the machine edits this tree live (memo `the-install-is-live-symlinks`).
Cache the parse and the language question is answered in Python.

What exists when this is done: `scan` keeps a parse cache under
`.pearde/.state/`, keyed on each file's path, mtime and size, and re-parses
only what moved. A cold call is no slower than today; a warm call on an
unchanged board is materially faster. The number to beat, measured the same
way: warm `scan` under 40 ms on this board.

Constraints. The cache is machine-local and git-ignored, exactly like
`.pearde/.state/plan.json`, and is never a source of truth: a missing, corrupt,
unreadable or version-mismatched cache falls back to a full parse silently and
never fails a call. It must never serve a stale answer — an edit made outside
pearde, by a person in an editor or by `git checkout`, is seen on the next
call. Stdlib only, as the whole tree is; no new dependency.

Pointers: `resources/board/plan.py` (`spec_data`, `compute_plan`, `cmd_scan`),
`.pearde/.state/plan.json` for the precedent, and `resources/statusline.sh`
and `resources/board/serve.py` as the other hot callers.

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
board: /Users/feb/dev/infra/pearde/.pearde · 85 PRDs · workers=6 · axis: 0 on · 8 off
vision: One command moves the states, the board organises itself toward a declared destination, and a person reads one live page — nothing is done by hand on the board that a tool can do.
counts: done 75 · open 4 · claimed 2 · superseded 2 · analyzing 2
walk+parse cold 6.2 ms -> warm 4.3 ms (? files)
parse-cache verify: pass

spec02: exit 0
board: /Users/feb/dev/infra/pearde/.pearde · 85 PRDs · workers=6 · axis: 0 on · 8 off
vision: One command moves the states, the board organises itself toward a declared destination, and a person reads one live page — nothing is done by hand on the board that a tool can do.
counts: done 75 · open 4 · claimed 2 · superseded 2 · analyzing 2
walk+parse cold 6.7 ms -> warm 4.6 ms (? files)
parse-cache verify: pass

---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 50        # higher first
complexity: 23      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
needs:
  - init-writes-a-board-on-the-pearde-layout
  - every-document-names-the-path-the-board-is-on
  - the-doctor-checks-the-path-a-board-is-on
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 7.05h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
commit: c8f7817
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

# the other boards move once and the script goes

The eight other boards on this machine are on the `.pearde/` layout, moved by
a script that is then deleted.

This repository was migrated by hand. The others were not, and they will break
the moment they are scanned by the moved code, which looks for `.pearde/` and
no longer knows `prds/`. The decision on record is explicit: no dual-path
support, and no permanent migration command — a throwaway `migrate.py`, run
once per board, then removed from the tree.

The boards are registered in `resources/board/state/serve.json`; read their
paths from there rather than guessing. At the time of writing they were:
dotfiles, mitosys, model, infra, realm, shared, manola, racer/.mi.

Per board, the move is the same one this repository had done to it:

    prds/ -> .pearde/
    inside it: mkdir prds/ and .state/
    every PRD directory -> prds/
    knowledge/ -> wiki/
    memos/ and workflows/ stay where they land, now siblings of prds/
    settings.md and vision.md stay at the board root
    the five state dotfiles -> .state/<name>, leading dot dropped
    each board's .gitignore rewritten for the new paths

Use `git mv` where a path is tracked and a plain move where it is not; some
boards will have untracked PRDs. The gate for each board is the same gate this
one had: `python3 resources/board/plan.py scan` run against it must succeed
and must report the PRDs under the names they already had, not prefixed.

Done when every board in `serve.json` scans clean, and `migrate.py` is no
longer in the tree.

Not in scope: touching the content of any PRD, memo or workflow in those
boards; anything that would make the migration re-runnable or permanent.

Depends on the layout being settled everywhere it is read — run this after the
init, docs and doctor work, not before.

Pointers: `resources/board/state/serve.json`, `resources/board/plan.py`.

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
pre-gate ok
MIGRATE FAILED
GATE: FAILED
LAYOUT: FAILED
STATE: WRONG COPY
spec01 probe: 4/4 gate lines above must read ok
spec01 fixture gate done
/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python: can't open file '/Users/feb/dev/infra/pearde/probe/migrate.py': [Errno 2] No such file or directory
cat: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.WXdlnyE2qg/b/.pearde/.state/history.jsonl: No such file or directory

spec02: exit 0
GATE ok: /Users/feb/dev/dotfiles
GATE ok: /Users/feb/dev/infra/mitosys
GATE ok: /Users/feb/dev/infra/model
GATE ok: /Users/feb/dev/infra
GATE ok: /Users/feb/dev/infra/realm
GATE ok: /Users/feb/dev/infra/shared
GATE ok: /Users/feb/dev/manola
GATE ok: /Users/feb/dev/racer/.mi
SERVE REGISTRY: ok — every row is a live board dir
51
MEMBER SIGILS: present
spec02 gate: 8 GATE ok lines, SERVE REGISTRY ok, MEMBER SIGILS present

spec03: exit 0
/Users/feb/dev/infra/pearde/.pearde/prds/every-document-names-the-path-the-board-is-on/probe/migrate.py
LEFTOVER migrate.py FOUND
GATE ok: /Users/feb/dev/dotfiles
GATE ok: /Users/feb/dev/infra/mitosys
GATE ok: /Users/feb/dev/infra/model
GATE ok: /Users/feb/dev/infra
GATE ok: /Users/feb/dev/infra/realm
GATE ok: /Users/feb/dev/infra/shared
GATE ok: /Users/feb/dev/manola
GATE ok: /Users/feb/dev/racer/.mi
spec03 gate: TREE CLEAN plus 8 GATE ok lines

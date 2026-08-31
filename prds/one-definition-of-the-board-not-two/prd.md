---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 88        # higher first
complexity: 16      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.1h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
commit: 93ba3c4 21641b5
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

# one definition of the board, not two

One tool, one answer to "where is the board". When this PRD is done, every
module that takes a board argument resolves it the same way `find_board` in
@resources/board/plan.py does — to `<x>/.pearde` — and the four commands that
are silently blind today (`memo list`, `memo check`, `workflow list`,
`questions list`) see the files that are actually on disk. It matters because
the failure mode is not an error: every one of them exits 0 while reading an
empty directory, so `doctor` reports the board healthy while looking at
nothing.

There are two definitions in the tree. @resources/board/plan.py:60 sets
`BOARD_DIR = ".pearde"` and `find_board` at plan.py:78 returns
`<x>/.pearde`. @resources/memos.py:238 `find_board` is a near-copy that
returns `<x>/prds` instead — `os.path.basename(p) == "prds"` at memos.py:241,
`os.path.join(p, "prds")` at memos.py:243 and again at memos.py:248/249.
@resources/questions.py:391 is a third copy of the same wrong body
(questions.py:393-405). @resources/workflows.py:88 has no body of its own: it
calls `memos.find_board(arg)` at workflows.py:92 and only rewrites the error
prefix, so it inherits the defect. The second definition names a directory
*inside* the first, which is why nothing raises — `.pearde/prds` exists, so
the resolver succeeds and hands back the PRD tree as if it were the board.

Measured on this repo, at the repo root: `python3 resources/memos.py list
.pearde` prints nothing and exits 0 while `ls .pearde/memos` counts 16 files;
`python3 resources/memos.py check .pearde` opens no file and exits 0;
`python3 resources/workflows.py list .pearde` prints nothing and exits 0 while
`ls .pearde/workflows` counts 18 atomics; `python3 resources/questions.py list
.pearde` prints nothing and exits 0 while three PRDs on the board carry a `##
Questions` heading. @resources/doctor.sh:428 runs `memos.py check "$BOARD"`
for the `memos` row and @resources/doctor.sh:458/462 run `workflows.py
list`/`check` for the `workflows` row, so both rows report ok off a reader
that opened no file.

The callers to re-aim are exactly these: `memos.main` at memos.py:262 and
memos.py:265; `workflows.main` at workflows.py:393 and workflows.py:402;
`questions.main` at questions.py:411. @resources/pearde.py routes `memo`,
`workflow` and `questions` to those scripts at pearde.py:79-81, so fixing the
resolver fixes the whole surface. Note `memos_dir()` and `workflows_dir()`
(workflows.py:98) already join onto the board they are handed and take a
`settings.md` override — they are correct once the board they are handed is
correct, and must not be rewritten.

Non-goals. `find_board` in plan.py is the definition and does not change.
The `settings.md` `memos:`/`workflows:` external-location overrides keep
working exactly as they do now. No file moves on disk, no frontmatter key is
added, and the four scripts keep their own error prefixes (`memos:`,
`workflows:`, `questions:`) so a failure still names the command that was
run. Whether the three copies collapse into one shared import or stay as
three bodies is the analyst's call; what is fixed is the answer, not the
number of copies. `doctor.sh` still has old-layout `prds/` assumptions of its
own (doctor.sh:250, 282, 290-296, 309-311) — those belong to
`the-doctor-checks-the-path-a-board-is-on`, not here.

## Acceptance sketch, for the analyst

- `python3 resources/memos.py list .pearde` from the repo root lists 16 memos and exits 0; `check` opens them and reports on their frontmatter rather than exiting 0 silently.
- `python3 resources/workflows.py list .pearde` lists the 18 atomics in `.pearde/workflows/`; `python3 resources/questions.py list .pearde` reports the PRDs carrying a `## Questions` round.
- All four commands give the same answer with no argument (walking up from a cwd inside the repo), with `.pearde` given, and with the repo root given — and each still errors with its own `memos:`/`workflows:`/`questions:` prefix when no board exists.
- `resources/doctor.sh`'s `memos`, `workflows` and `questions` rows report counts that match what is on disk, rather than ok-over-nothing.
- No remaining occurrence of a board resolved to `<x>/prds` in `resources/memos.py`, `resources/questions.py` or `resources/workflows.py`; a `settings.md` `memos:`/`workflows:` override still redirects the directory as before.

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
== A: memos — list count matches disk, check opens real files ==
  ok   memos list (17) == memos on disk (17)
  ok   memos.py find_board no longer resolves to <x>/prds
== B: workflows — list count matches disk, refs carry no prds/ prefix ==
  ok   workflows list (18) == atomics+workflows on disk (18)
  ok   no workflow ref label carries a stray prds/ prefix
== C: questions — prds() walks board/prds, not board ==
  ok   no questions.prds() label carries a stray prds/ prefix
  ok   questions.prds() count (71) == prd.md files on disk (71)
== D: all four commands agree — no-arg walk, .pearde, repo root ==
  ok   memos.py list agrees across no-arg / .pearde / repo-root
  ok   questions.py list agrees across no-arg / .pearde / repo-root
  ok   workflows.py list agrees across no-arg / .pearde / repo-root
== E: error path still names the command that was run ==
  ok   memos.py: own error prefix, cwd walk
  ok   memos.py: exit 1 with no board
  ok   questions.py: own error prefix, cwd walk
  ok   questions.py: exit 1 with no board
  ok   workflows.py: own error prefix, cwd walk
  ok   workflows.py: exit 1 with no board
== F: doctor.sh rows report counts that match disk ==
  ok   doctor memos row: 17 memos, ok
  ok   doctor workflows row: ok
  ok   doctor questions row: ok
== G: knowledge.py board — no PRD note nested under a stray board/prds/ ==
  ok   knowledge.py board writes no board/prds/ subtree
  ok   knowledge.py board wrote 71 PRD note(s), matching disk (71)

20 checks · 20 pass · 0 fail
verify.sh done, fail=0
resources/memos.py parses
resources/questions.py parses
resources/workflows.py parses
resources/knowledge.py parses
resources/memos.py:22:OPTIONAL = ("updated", "prds", "supersedes", "superseded_by")
resources/memos.py:125:    root = os.path.join(board, "prds")
resources/memos.py:188:        for name in _listed(fm.get("prds")):
resources/questions.py:167:    root_dir = os.path.join(board, "prds")
resources/questions.py:205:              "skeptic", "verdict", "dispatch", "dispatched", "prd", "prds",
resources/workflows.py:206:    prds_root = os.path.join(board, "prds")
verify block complete

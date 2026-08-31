# report — two-questions-start-a-drill · analyst · as engineer

verdict: **SPECCED**

workflow: probe-then-spec — no `## Route`: every step of the run is a library
row already (`read-the-contract`, `attempt-the-build`, `write-the-specs`,
`run-the-scoped-verify`); no atomic the run took is missing.

## What the build stood up (all uncommitted, pass one)

- `resources/questions.py` — `unanswered(board)`: `[(rel, qid, title)]`, the
  one reader. A `### Qn:` under `## Questions` with no matching `**Qn**` under
  `## Answers`, on any PRD outside `CLOSED` — `superseded` joined the terminal
  set beside `done`/`deferred`/`out-of-scope`. `rows()` yields it as `list`'s
  `open` column (`asked` renamed, since the column now means un-put questions).
- `resources/board/plan.py` — `drill_questions(board)` wraps the count with the
  round file: `.pearde/.state/round.md` `## Asked`, matched by normalized
  title, lenient toward `out` (a question already carried is never re-put —
  drill.md's own bias). `cmd_scan` prints `asking N over M PRDs` in the header
  line; over one, a **drill** section stands first, above *collect*, one line
  per question by PRD, id, title, `· out` beside the listed ones. Zero prints
  nothing; one question prints the count and no section.
- `resources/board/transitions.py` — the drill gate in `gate_claim` after the
  `dispatchable` gates: two or more unanswered questions not yet in `## Asked`
  → Refused `asking N — drill first; the unanswered questions go to the user
  before anything is dispatched`. One outstanding is not a gate. `--force` and
  the view's forced `/edit` pass; `brief --worker` refuses the same way
  (nothing is dispatched while it is open).
- Docs: `references/parts/loop.md` step 1 names the count and the drill-first
  cut; step 2 carries the trigger table (0 / 1 / ≥ 2, the PRD's rows) plus the
  nothing-dispatched sentence; step 8 says it is the same drill. drill.md §
  The board's own frontier gained the scan-count entry point. round.md's
  `## Asked` bullet says the gate reads it, by title. guard.md § What it
  counts says the drill refusal lands in the transition window's `refused`.

## Specs

- `specs/spec01.md` — the count: `unanswered` + the scan's drill section
  (complexity 10; footprint `resources/questions.py`, `resources/board/plan.py`).
  5 boxes; boxes 1-2 verified green.
- `specs/spec02.md` — the claim gate (complexity 8; footprint
  `resources/board/transitions.py`). 3 boxes; verified via probe legs 2-3.
- `specs/spec03.md` — the manual says where the drill starts (complexity 5;
  footprint the four reference files). 5 boxes; greps ran green.
- Every box was re-run against the tree as it stands on disk (probe exit 0,
  11 OK / 0 FAIL; direct module calls agree). None pre-ticked.

## Verify block mechanics

Verify blocks end on an explicit echo (`spec01 verify done` / `spec02 verify
done` / `spec03 verify done`), never on a bare grep; fixture boards are built
at run time under tmp paths, never under the board.

## Knowledge step

`python3 resources/knowledge.py query "two questions start a drill"` — 7 hits,
1 strong (scout-conclusions), none answering the PRD's question. The gap
auto-enqueued into `.pearde/wiki/pending/`; noted here, it is not a question
of mine. No fact from outside this repo was learned, so nothing to `remember`.

## Findings (report-only)

- The PRD's loop.md row says "step 7 says it is the same drill" — it predates
  the knowledge step landing today, which made the drill step 8. Landed the
  sentence on step 8, where the loop actually puts the drill.
- `questions.py list` narrowed on purpose: its `asked` column counted every
  question ever asked (answered included); it now prints `open` and counts the
  frontier. Its `answered` column still counts `## Answers` sections, not
  answers — pre-existing, left as it was, recorded here.
- `superseded` joining `CLOSED` also means `check()` reads a superseded PRD's
  `## Answers` as history — consistent with `done`, arguably overdue.
- The view's asks inbox reads states, not the count — untouched, in no
  footprint. A scan-count card in the view would be a separate PRD.
- Real-board effect right now: `.pearde` counts zero unanswered questions, so
  the gate changes nothing on this board until questions stand.

## Scores

complexity: 23
blast-radius: mid
workflow: probe-then-spec

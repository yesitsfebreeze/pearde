---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 90        # higher first
complexity: 18      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.12h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
commit: aa94262 86c9753
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

# the budget ceiling counts the session it stops

When this is done the `context-budget` ceiling is measured against the round it
was written for. The orchestrator session is still bounded and still told to end
at the ceiling; a dispatched analyst or implementer is not refused for a window
the orchestrator's ceiling never described. And no refused party is ever left
with `.pearde/.state/round.md` as one of its few writable paths unless that party
is the session whose round file it is. This matters because the protection is
not merely wrong today, it is off: `.pearde/settings.md:8` reads
`context-budget: off`, set by hand to get work moving again, so the round has no
ceiling at all and the note at 70% never fires.

The measurement is per-session, not per-round. `pre()` at `resources/guard.py:536`
takes `session_id`, `cwd` and (through `context_now()`) `transcript_path` straight
off the hook payload; `context_now()` at `resources/guard.py:463` opens whatever
transcript that payload names and sums `input_tokens + cache_read_input_tokens +
cache_creation_input_tokens` off its last assistant line. `budget_of()` at
`resources/guard.py:443` reads one board-wide `context-budget:` key, defaulting to
`BUDGET_DEFAULT = 100_000` at `resources/guard.py:52`. Nothing in `guard.py`
distinguishes an orchestrator session from a dispatched one — the only mention of
the orchestrator in the whole file is the prose comment at
`resources/guard.py:49`. The guard is wired in `.claude/settings.json` as a
`PreToolUse` hook on `Bash|Read` and on `Edit|Write`, and a `PreToolUse` hook
fires in every agent session, subagents included. So each worker is measured
against the round's number as if it were the round.

Measured, in this session, at the 100k default: three separate freshly-dispatched
analysts were refused every tool call — `Read`, `Write`, `Edit`, and plain `cat`
and `echo` through `Bash` — at 102k, 80k and 72k tokens, each after no more than
reading its own PRD and four or five reference documents. None had made a single
edit. The refusal text at `resources/guard.py:524` then tells the refused party to
write `.state/round.md` whole and let the next session resume from it, which is an
instruction only the orchestrator can act on, and `ESCAPE` at
`resources/guard.py:56` (`\.round\.md$|/(loop|round)\.md$`, honoured for
`Edit|Write|Read` at `resources/guard.py:518`) leaves exactly that path open. One
of the three did as it was told: it wrote its own state into
`.pearde/.state/round.md` and destroyed the orchestrator's round. There is one
round file per board and it is the session's own memory, per
`references/parts/round.md`, so a worker writing it is not a second copy — it is an
overwrite.

Two defects, and the fix must name both: a worker's window is counted against a
ceiling written for the round, and the escape hatch that makes the refusal
survivable for the orchestrator is actively destructive when the refused party is
a worker. Constraints: the token accounting in `context_now()` is correct and does
not change; the key's name, its `100k` default and its `off`/`160k` parsing in
`budget_of()` do not change, because `references/settings.md:44` and
`references/parts/loop.md` document them; the orchestrator's own behaviour — the
one-shot notes at 70% and 85%, the refusal at the ceiling, and the set of paths
that stay open to it — must come out unchanged. Non-goals: this is not a job to
make workers cheaper, to give workers a budget of their own, or to touch any
other refusal in the guard (the hand-walked board, `state:` by hand, repeat
reads). Turning `context-budget` off is the workaround under repair, not an
outcome — the PRD is done when that line can hold a number again.

Pointers: `resources/guard.py` (`budget_of` 443, `context_now` 463, `budget` 494,
`pre` 536, `ESCAPE` 56, `BUDGET_DEFAULT` 52, `state_path`/`load`/`save` 216-234 for
the per-session state the warn band is stored in), `.claude/settings.json` for the
hook wiring, the `context-budget` row in `references/settings.md`, the ceiling
paragraph in `references/parts/loop.md`, and `references/parts/round.md` for what
the round file is and whose it is. Whether the hook payload carries anything that
separates a dispatched session from the round's own is the first thing to
establish; the contract is the outcome, not a particular signal.

## Acceptance sketch, for the analyst

- With `context-budget` set to a number, a dispatched analyst or implementer
  session that reads well past that number is not refused `Read`, `Write`, `Edit`
  or `Bash` by the ceiling.
- With the same setting, an orchestrator session over the ceiling is still
  refused, still gets the 70% and 85% notes exactly once each, and still keeps the
  round file, `references/parts/loop.md`, `references/parts/round.md` and the
  board's own commands open.
- No session that is not the round's own can write `.pearde/.state/round.md`
  through the escape hatch at the ceiling.
- `.pearde/settings.md` no longer needs `context-budget: off`; it carries a number
  and a full round with dispatched workers completes without a worker being
  refused.
- `budget_of()` still parses `off`, a bare number and a `k` suffix as
  `references/settings.md` documents, and `context_now()`'s token sum is unchanged.

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
PASS orchestrator over cap is denied
PASS dispatched worker over cap is not denied
PASS dispatched worker's Bash over cap is not denied
PASS dispatched worker writing round.md over cap raises no ceiling deny
PASS orchestrator's own round.md write at the ceiling stays open
PASS orchestrator at 75% gets the warn note
PASS dispatched worker at 75% gets no note
PASS live orchestrator payload shape is not dispatched
PASS live worker payload shape is dispatched
PASS the two live shapes share one session_id, so it cannot be the signal
PASS budget_of parses off as 0
PASS budget_of parses a bare number
PASS budget_of parses a k suffix

13 of 13 checks pass
---
guard: /Users/feb/dev/infra/pearde/.pearde
  stamp 1788194578.096
  state /Users/feb/dev/infra/pearde/resources/board/state/guard
  scan  python3 /Users/feb/dev/infra/pearde/resources/board/plan.py scan
done

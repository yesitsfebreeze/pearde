---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived  # requested = the user asked | derived = the board found it
from: nothing-left-open/the-line-tells-the-truth
priority: 60        # higher first
complexity: 8      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.04h
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
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# an analyst workflow does not survive into specced

When this is done, a route an analyst has already written down survives the
`analyzing → specced` transition without a person retyping it. `pearde specced
<prd>` reads every `specs/*.md` anyway; when one of them carries a `workflow:`
in its frontmatter and the PRD does not, the command writes that slug into the
PRD's own frontmatter, the same way `refine` already hands a parent's
`workflow` down to each child it creates. An explicit `--workflow <slug>` still
wins over anything derived, and `--workflow none` still deletes the key. This
matters because the PRD-level key is the only thing anything downstream reads:
lose it and the next worker is dispatched with no route where a route existed.

The premise as filed is half wrong, and the correction is the finding. There is
no allowlist and no frontmatter rewrite on this transition: nothing in this repo
parses a `## Scores` block at all. The only two occurrences are
`references/parts/workers.md:153`, where the analyst is told to end its report
with the block verbatim, and `references/parts/workers.md:229`, where the
orchestrator is told to read the values *off* it by eye and retype them as
flags. So no parser drops `workflow:` — there is no parser. The real loss is one
level down, in `resources/board/specs.py`: line 248 reads
`blast, workflow = args.opt.get("blast"), args.opt.get("workflow")`, and that
CLI flag is the key's only source. A spec file's own `workflow:` is read and
*validated* at `resources/board/specs.py:173-181` — it is refused by name if the
slug is an atomic or is in no library — and then discarded: `read_specs`
(`resources/board/specs.py:185`) returns only the sum, the count, the refusals,
the warnings and the footprints, never the slug. The write at
`resources/board/specs.py:292-298` therefore fires only when a human typed the
flag. Contrast `resources/board/specs.py:343-344`, where `refine` does inherit
`workflow` into every child it writes — the same value, propagated on the other
transition out of `analyzing`.

Reproduced on a scratch copy of `resources/board/example`: a PRD in `analyzing`
whose only spec carried `workflow: fix-a-line` (a real workflow in that board's
library), run as `specs.py specced next --blast low`. Exit 0, the progress line
printed `analyzing → specced`, and the PRD came back with `state: specced` and
`complexity: 5` and still no `workflow:` key. Two things compound it, and
together they explain the round in which an analyst reported a workflow edit
that could not be applied and no flag worked around it. First, the spelling the
analyst is told to report is `workflow: <slug> | none fit`
(`references/parts/workers.md:157`) while the command accepts only the bare word
`none`, so `--workflow "none fit"` is refused at
`resources/board/specs.py:254-257`. Second, three of the four places the command
is documented — `README.md:50`, `references/parts/states.md:11`,
`references/parts/solo.md:11` — spell it `specced <prd> --blast <x>` with no
`--workflow` at all; only `references/parts/workers.md:228` mentions it.

What the loss costs is narrower than "the worker gets nothing", and the contract
should be honest about it. `slugs_of` in `resources/board/brief.py` takes the
PRD's `workflow:` for every role, and each spec's `workflow:` **only** for an
implementer. So an implementer still gets its per-spec routes inlined; but the
PRD line carries no mark in `workflow_marks` (`resources/board/plan.py`), the
brief's head line reads `wf none`, no route block is inlined for any other role,
and a later `refine` has nothing to hand its children at
`resources/board/specs.py:343-344`. An analyst or consultant re-dispatched on
that PRD gets no route at all.

Constraints. Do not add a `## Scores` parser — the orchestrator reads that block
and the flag stays the explicit override; the flag must keep winning over any
derived value, and `--workflow none` must keep deleting the key. Do not change
the validation at `resources/board/specs.py:173-181` or its refusal wording, and
do not touch `refine`'s inheritance. `--check` must still write nothing, and
`--dry` (`resources/board/specs.py:277-289`) must show the derived slug in the
same shape the real write would take. Non-goals: no change to
`resources/board/brief.py`, `resources/board/plan.py` or
`resources/workflows.py`; no change to how the library is scanned
(`resources/board/specs.py:227`); no new frontmatter key, no new flag, no
state-machine change; and nothing that would overwrite a `workflow:` the PRD
already carries. One case must be decided and written down rather than guessed:
two specs naming different slugs — leaving the PRD key unset is the safe answer,
but say so in the spec, with the operator told which.

Pointers. `resources/board/specs.py` (`specced` 246-300, the spec check 173-181,
`read_specs` 185, child inheritance 338-348, `FLAGS` 435-439);
`resources/board/edit.py` (`set_key` 35, `del_key` 53 — how a key is appended to
a frontmatter block that only has it commented out);
`resources/board/brief.py` (`slugs_of`, and the `wf ...` head line);
`resources/board/plan.py` (`workflow_marks`); `references/parts/workers.md`
128-232 for the analyst's report contract; `references/workflow.md` and
`references/templates/spec.md` for what the key means.

## Acceptance sketch, for the analyst

- With a PRD in `analyzing` carrying no `workflow:` and one `specs/*.md` whose
  frontmatter names a real workflow, `pearde specced <prd> --blast low` (no
  `--workflow`) exits 0 and the PRD's frontmatter afterwards holds that slug.
- The same run with `--workflow <other-slug>` writes `<other-slug>`, and with
  `--workflow none` the PRD ends with no `workflow:` key — the flag beats the
  spec in both directions.
- A PRD that already carries a `workflow:` keeps its own value when a spec names
  a different one; a spec naming an atomic or an unknown slug is still refused by
  file and line, exactly as it is today, and the PRD is not written.
- `pearde specced <prd> --dry` prints the slug it would write and changes no
  file; `--check` still writes nothing.
- `pearde brief <prd>` on the resulting PRD has the slug in its `wf ...` head
  line and the route inlined, for an analyst brief as well as an implementer's.

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

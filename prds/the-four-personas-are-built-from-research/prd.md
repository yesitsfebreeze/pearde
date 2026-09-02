---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 60        # higher first
complexity: 20      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: low
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.48h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
commit: 144f3e8 695bbda
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

# The four personas are built from research

The four roster personas — `engineer`, `designer`, `mentor`, `skeptic` in
`@references/personas/` — are research-backed composites, built the way
`persona create` builds a new one (@references/personas/INDEX.md, steps 1-4),
instead of written from intuition.

## What exists when this is done

- Each of the four files carries `## Built from`: one bullet per researched
  practitioner of that field — who, known for, the one trait taken, the
  source. At least three practitioners per persona.
  The check that backs this is a shape check — it reads the bullet's form and
  its internal consistency, never whether the artefact named exists. The
  research itself is recorded in `.pearde/wiki/sources/`, not enforced by any
  gate.
- Each bullet under `## How you work` traces to a named trait in `## Built
  from`. A bullet that traces to nobody is cut or re-sourced.
- The opening paragraph of each file says it is a composite, first line.
- The roster in `@references/personas/INDEX.md` no longer says "The four below
  were written, not researched, and carry no **Built from**".

## Why

The four were written on 2026-08-25 from intuition. The rewrite on 2026-09-02
made each precise — what gets noticed first, what gets pushed back on, what
counts as done — but every bullet still traces to nobody, so a reader cannot
tell a measured behaviour from a preference.

## Constraints

- File format unchanged: three frontmatter keys, one paragraph, `## How you
  work` with 3-6 bold-led bullets, `## Voice` in 2-3 sentences, `## Built
  from`.
- Ids, names and professions unchanged. The signals table in
  `@references/parts/personas.md` and the worker table in
  `@references/parts/workers.md` unchanged.
- Second person throughout. No real person quoted. No pronoun for the persona.
- Research is dispatched to workers per INDEX.md step 2 — names are facts, not
  questions for the user.

## Non-goals

- No fifth persona.
- No change to how a persona is chosen, worn, or consulted.
- No in-tree proof that a practitioner or a source is real. Nothing in this
  repo can tell a researched trace from a fabricated one, and this PRD does
  not add it.

## Pointers

- `@references/personas/INDEX.md` — the build steps and the file format
- `@references/personas/{engineer,designer,mentor,skeptic}.md` — the four
- `@references/parts/personas.md` — what a persona is
- `@references/language.md` — the body's rules

## Acceptance

- [x] `grep -c '^## Built from' references/personas/{engineer,designer,mentor,skeptic}.md` prints 1 for each
- [x] each `## Built from` has at least three bullets, each naming a person, a trait and a source
- [x] each `## How you work` bullet names the trait it comes from
- [x] the INDEX.md sentence about "written, not researched" is gone
- [x] `python3 resources/index.py check` silent

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one pass in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     the best one first and marked `(recommended)`. Only real forks the user
     must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such pass never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a pass that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the pass above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

## Report

spec01: exit 0
ok   references/personas/designer.md — one '## Built from', 7 sourced practitioners, all dated, first line says composite
ok   references/personas/mentor.md — one '## Built from', 6 sourced practitioners, all dated, first line says composite
ok   references/personas/skeptic.md — one '## Built from', 7 sourced practitioners, all dated, first line says composite
index.py check said: (silent)
ok   index.py check names no footprint file
134 checks, 134 pass, 0 fail — designer, mentor, skeptic
ok   the three footprint personas are green
ok   designer — the probe goes red on a trace naming nobody (was [Alan Cooper: …])
ok   mentor — the probe goes red on a trace naming nobody (was [Peter Naur: …])
ok   skeptic — the probe goes red on a trace naming nobody (was [Elisabeth Hendrickson: …])

spec02: exit 0
ok   probe reads every trace on a bullet
ok   engineer green
ok   probe goes red on a second trace naming nobody (engineer.md:19)
ok   probe goes red on a source naming no year (designer.md:46)
ok   persona grammar — 190 checks, 190 pass, 0 fail

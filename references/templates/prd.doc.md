# prd.md — how to fill it, and why each line is there

The template is @references/templates/prd.md. `pearde add` copies it whole,
sets `state`, `origin`, `priority` and the title, and puts the body in place of
the placeholder; `pearde refine` writes one child per row from it the same way.
Every line in the template lands in every PRD, so the template carries nothing
a PRD does not need. This file carries the rest.

## Frontmatter

| key | who writes it | why it is in the template |
|---|---|---|
| `state` | the transition commands only, never by hand — @references/parts/guard.md refuses a hand edit | the one key the loop cannot run without. Values: `open` `analyzing` `refine` `question` `specced` `claimed` `blocked` `done` `failed` |
| `origin` | whoever creates the PRD | `requested` = the user asked · `derived` = the board found it. The split in the progress line, the tripwire in @references/parts/derived.md |
| `priority` | user | vision importance — dispatch order, higher first |
| `complexity` | analyst, at spec time | THE WEIGHT the board schedules by, 1-100. Summed from the specs |
| `blast-radius` | analyst, at spec time | `high` \| `mid` \| `low` — what breaks if this is wrong. Breaks ties, decides what a pass leads with |

Keys the template does not carry, all optional, all read when present:

| key | is |
|---|---|
| `from` | derived only — the PRD whose work surfaced this one |
| `repo` | the sub-repo the code lands in; the worker brief reads it |
| `workflow` | a slug in `.pearde/workflows/` — how this kind of job is done. @references/workflow.md. Absent = the brief alone |
| `needs` | PRD dir names this one depends on. A hard gate in `plan` |
| `footprint` | paths this PRD touches. The overlap check |
| `time.est` | the weight, only when `complexity` is absent. Not a duration |
| `time.actual` | a record. Nothing schedules by it |
| `claim` | orchestrator-only, present while a worker holds this PRD |

Match is by name at any nesting, so `time:` holding `est` reads as `est`.
Add your own keys freely; nothing outside the set above is read, and nothing
you add is ever dropped. @references/parts/contract.md is the contract and the
defaults for a missing key.

## Ordering

Three axes and no clock: dependency (`needs` + `footprint`), vision importance
(`priority`), and `complexity` / `blast-radius`. @references/parts/order.md.

## The body

The title says what exists when the PRD is done. The body is the request, for
an analyst who knows the codebase but not the conversation: what exists and why
it matters, constraints and non-goals, pointers to files, docs and prior PRDs.

One contract per PRD. "And also…" is a second PRD — write it separately, or
let the analyst split it. One sitting is the limit: specs summing `complexity`
above `split-above` or counting above `specs-above` (both in
`.pearde/settings.md`, default 40 and 6) make the analyst's verdict REFINE,
and `pearde refine` lands the split under `## Children` — the contract above
it stays as written.

A derived PRD states, in the body, which requested PRD it would otherwise get
wrong. If it cannot, it is filed `state: deferred`; if fixing it would change
only how loudly the board notices, it is a memo, not a PRD.

## The three headings the template does not ship

Each is a claim about the state of this PRD, so an empty copy is a false one:
an empty `## Questions` stops the board on nothing, an empty `## Answers` reads
as answered, an empty `## Failure` reads as a failed attempt. Write the heading
when it has content. @resources/questions.py reports the empty ones, and
`doctor`'s `questions` row runs it.

| heading | who | what |
|---|---|---|
| `## Questions` | analyst, when blocked on the user | one pass in the format of @references/drill.md — `### Q1: <title>`, the fork in two sentences ending in `?`, then exactly three prepared answers, each a complete decision, the best first and marked `(recommended)`. Only forks the user must settle — never facts a worker could look up. Plain words for the person who asked: no backtick, no path, no PRD name, 60 words in the fork, 25 in an answer |
| `## Answers` | orchestrator, or the view | `**Q1** — <the picked answer verbatim, or the user's own words>`, numbers matching the pass. Analysts read these before speccing. An `## Answers` with no `## Questions` above it answers nothing |
| `## Failure` | implementer, after FAILED | what broke, what was tried. `retry` moves it into the body as history and reopens the PRD |

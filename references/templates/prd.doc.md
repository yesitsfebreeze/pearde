# prd.md — how to fill it, and why each line is there

The template is @references/templates/prd.md. `pearde add` copies it whole,
sets `state`, `origin`, `priority` and the title, and replaces the placeholder
with the body; `pearde refine` writes one child per row the same way. Every
template line lands in every PRD, so it carries only what every PRD needs;
the rest is here.

## Frontmatter

| key | who writes it | why it is in the template |
|---|---|---|
| `state` | the transition commands only — @references/parts/guard.md refuses a hand edit | the loop's one required key. Values: `open` `analyzing` `refine` `question` `specced` `claimed` `blocked` `done` `failed` |
| `origin` | whoever creates the PRD | `requested` = the user asked · `derived` = the board found it. The split in the progress line, the tripwire in @references/parts/derived.md |
| `priority` | user | vision importance — dispatch order, higher first |
| `complexity` | analyst, at spec time | THE WEIGHT the board schedules by, 1-100. Summed from the specs |
| `blast-radius` | analyst, at spec time | `high` \| `mid` \| `low` — what breaks if this is wrong. Breaks ties, decides what a pass leads with |

Not in the template; optional, read when present:

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

Match is by name at any nesting, so `time:` holding `est` reads as `est`. Add
your own keys freely: nothing outside the set is read, nothing added is
dropped. @references/parts/contract.md holds the contract and a missing
key's default.

## Ordering

Three axes and no clock: dependency (`needs` + `footprint`), vision importance
(`priority`), and `complexity` / `blast-radius`. @references/parts/order.md.

## The body

The title says what exists when the PRD is done. The body is the request, for
an analyst who knows the codebase but not the conversation: what exists and why
it matters, constraints and non-goals, pointers to files, docs and prior PRDs.

One contract per PRD. "And also…" is a second PRD — write it separately, or let
the analyst split it. One sitting is the limit: specs summing `complexity` over
`split-above` or counting over `specs-above` (both in `.pearde/settings.md`,
default 40 and 6) make the verdict REFINE, and `pearde refine` lands the split
under `## Children`, leaving the contract as written.

A derived PRD names, in the body, the requested PRD that goes wrong without it.
One naming none is filed `state: deferred`; where the fix changes only how
loudly the board notices, write a memo, not a PRD.

## The three headings the template does not ship

Each claims something about this PRD's state, so an empty copy is a false
claim: an empty `## Questions` stops the board on nothing, an empty
`## Answers` reads as answered, an empty `## Failure` as a failed attempt.
Write a heading when it has content. @resources/questions.py reports the empty
ones; `doctor`'s `questions` row runs it.

| heading | who | what |
|---|---|---|
| `## Questions` | analyst, when blocked on the user | one pass in @references/drill.md's format — `### Q1: <title>`, the fork in two sentences ending in `?`, then exactly three prepared answers, each a complete decision, best first, one marked `(recommended)`. Only forks the user must settle, never a lookup. Plain words for the person who asked: no backtick, no path, no PRD name, 60 words in the fork, 25 in an answer |
| `## Answers` | orchestrator, or the view | `**Q1** — <the picked answer verbatim, or the user's own words>`, numbers matching the pass. Analysts read these before speccing. An `## Answers` with no `## Questions` above answers nothing |
| `## Failure` | implementer, after FAILED | what broke, what was tried. `retry` moves it into the body as history and reopens the PRD |

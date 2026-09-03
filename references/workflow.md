# Workflows

A **workflow** says how a kind of job is done, and gets better every run.
Without the folder every worker re-derives the *how*, and the last lesson dies
with its context.

```
.pearde/workflows/<slug>.md
```

| kind         | file says          | is                                                                    |
|--------------|--------------------|-----------------------------------------------------------------------|
| **atomic**   | `atomic: <slug>`   | one unit of work — what to do, how to tell it worked, how it fails    |
| **workflow** | `workflow: <slug>` | ordered atomics — why each is there, and where a failure returns to |

Exactly one slug key: it says the kind, the filename equals the slug.

- No `state`. Never claimed, specced, or dispatched.
- `workflows/` holds no `prd.md`: scan walks past as past `memos/`, and the
  progress line counts none.
- One flat directory, no nesting — a file is found by its slug.
- `workflows:` in `.pearde/settings.md` points elsewhere, default `workflows/`
  — several boards share one library.

A PRD or a spec routes with `workflow: <slug>`, one scalar slug naming one
library file. Any other shape is a **break, not an absence**, reported as a
dangling slug is. An absent key is silence.

The library does **not** merge; only the refs do. A master board's check
crosses every board in `members:`, a slug resolving against its own library
first and the master's second, as `needs:` does —
@references/parts/workers.md.

## Atomic

Frontmatter, a **closed** set:

```
---
atomic: reproduce-the-failure
subject: turn a reported break into a command that fails on this tree
date: 2026-08-28
updated: 2026-09-02
runs: 4
tags:
  - atomic
---
```

| key       | required  | is                                                          |
|-----------|-----------|---------------------------------------------------------------|
| `atomic`  | yes       | the slug — the filename without `.md`                       |
| `subject` | yes       | one line: the unit of work                                  |
| `date`    | yes       | the day written, ISO 8601 — written, never stamped          |
| `updated` | no        | the day the text last changed from a run                    |
| `runs`    | no        | runs the file was in — one collect, one count. Integer ≥ 0, default 0 |
| `tags`    | generated | the slug key's kind, derived and never typed — the graph colours by tag. `workflows add` writes it, `workflows retag` rewrites the lot |

Body, per `@references/templates/atomic.md`:

| section                             | holds                                                       |
|-------------------------------------|---------------------------------------------------------------|
| `# <slug> — <the unit in a phrase>` | the title                                                   |
| `## Do`                             | numbered imperative steps naming commands and files, each closable in one sitting |
| `## Done when`                      | bullets, each a check that can fail                         |
| `## Fails when`                     | table `\| seen \| means \| do \|`, grown from runs — what a run hit, what it meant, what closed it. Empty at `runs: 0` |

One unit. An atomic that needs "and then" is two.

## Workflow

The same closed set with `workflow` as the slug key:

```
---
workflow: fix-a-reported-break
subject: a reported break, from the report to the verified fix
date: 2026-08-28
runs: 0
tags:
  - workflow
---
```

Body, per `@references/templates/workflow.md`:

| section                            | holds                                                      |
|------------------------------------|---------------------------------------------------------------|
| `# <slug> — <the job in a phrase>` | the title                                                  |
| `## Use when`                      | bullets: the jobs this fits, and the near-miss it does not |
| `## Steps`                         | table `\| # \| atomic \| why \| on failure \|`             |

### Steps grammar

- `#` counts from 1, contiguous.
- `atomic` is a slug in the same directory, written `` `<slug>` ``.
- `why` is one clause — what the step buys the job, never its `subject`
  restated.
- `on failure` is `→ N` with N < `#`, or `stop`. No forward jump: a skippable
  step is not a step.
- A back-edge is taken at most twice per run; a third failure at one step is
  `stop`.
- `stop` reports BLOCKED or FAILED per the brief, naming the step.

## The report section

One fixed shape, never per workflow, carried in the worker's report:

```
## Workflow <slug>

| # | atomic            | outcome              | note                                      |
|---|-------------------|----------------------|--------------------------------------------|
| 1 | read-the-contract | passed               |                                            |
| 2 | reproduce         | failed → 1 · passed  | the fixture named in ## Do does not exist  |

### Edits

**<slug>** — `## <section>` — <the replacement text, paste-ready>
```

`outcome` is `passed`, `failed → N`, or `stopped`. A step run twice lists both,
`·` separated.

An edit names file, section and replacement text — the orchestrator pastes or
refuses it, never rewrites it. Edits come from runs, never from reading.

## The check

@resources/workflows.py alone reads this format; the `doctor` row `workflows`
runs it. Failures:

- no `---` fence, or one unterminated
- neither or both of `atomic:` and `workflow:`
- a slug disagreeing with its filename
- a required key missing, or a key nobody declared
- a date outside ISO 8601, an `updated` before its `date`, or a `runs` below
  zero or not an integer
- a `tags:` the file's own slug key does not derive — repaired by `python3
  @resources/workflows.py retag [board]`, never by hand
- an atomic with no `## Do` or no `## Done when`
- an atomic whose `## Do` routes to another atomic **by slug** — "run `<slug>`" is an ordered pair written by hand, so it is refused: route it (a workflow with two atomics) or inline it (prose, one unit again). A slug named with no routing verb ("compare with the `<slug>` atomic") is prose, and passes
- a workflow with no `## Steps` table
- a step row whose `#` breaks the count from 1, whose `atomic` names no file in
  the directory, or whose `on failure` is neither `stop` nor `→ N` with N < `#`
- `workflow:` on a `prd.md` or a spec naming no **workflow** in the library,
  an atomic included — a file is not a route
- `workflow:` on a `prd.md` or a spec holding anything but one slug
- on a master board, either of those on a **member's** PRD or spec, addressed
  `@<member>/<rel>`
- a board in `members:` that is not on disk
- a workflow whose `## Workflow <slug>` report sections on disk right now
  outnumber its own `runs:` — never the other way: a report is overwritten
  by its PRD's next pass, so `runs:` outliving the reports that earned it is
  not a fault
- a `## Workflow` report-section heading naming no slug

Checked against the real library, never a fixture.

## How the text changes

- **No log.** A lesson folds into `## Do` or `## Fails when` and `updated`
  moves; git holds what it replaced.
- **No agent, tool, hook or vendor name.** Commands and files.
- **The board language**, per @references/language.md.
- `runs` counts runs, not the traversals inside one — a step a back-edge
  returns to counts once, as does its atomic. `updated` moves only on a text change.

## Why the board, and the shapes rejected

`.pearde/workflows/` is one directory deeper on a path the session already
walks — the argument @references/memo.md makes for `memos/`, and a `workflow:`
then names a sibling the check can verify.

Rejected:

- **A `kind:` key beside one slug key** — two fields that must agree are one
  field able to disagree.
- **`atomics/` as a subfolder** — one flat directory is one check, and a step
  names a slug, not a path.
- **A dated log section** — git holds history, and a file logging its own
  outgrows the page a worker reads.

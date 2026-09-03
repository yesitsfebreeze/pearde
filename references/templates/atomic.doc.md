# atomic.md — how to fill it, and why each line is there

The template is @references/templates/atomic.md. `pearde workflow add atomic
<subject>` checks it exists, writes the frontmatter — slug key, `subject`,
`date`, `runs: 0`, `tags:` from the slug key — and takes the body on stdin.
@references/workflow.md is the format; @resources/workflows.py checks it.

## Frontmatter

A CLOSED set with exactly one slug key: `atomic` here, `workflow` in
@references/templates/workflow.md. An undeclared key fails the check.

| key | is |
|---|---|
| `atomic` | the slug — the filename without `.md` |
| `subject` | one line — the unit of work |
| `date` | the day it was written, never stamped |
| `updated` | optional — the day a run last changed the text |
| `runs` | runs this file was in — one collect, one count. Integer >= 0 |

## Sections

**`## Do`** — numbered imperative steps, each naming a command and a file:
`python3 resources/index.py check`, not "verify the index". ONE unit of work,
closable in one sitting; one needing "and then" is two atomics and a workflow
ordering them. Name commands and files, never an agent, tool, hook or vendor.
A step that says "run `<slug>`" of another atomic has already written that
pair by hand, and the check refuses it: **route it** — promote both into a
workflow whose steps table orders them — or **inline it**, if the second is a
detail of the first and belongs here as prose. Both land on one file shape.
A slug named without a routing verb ("compare with the `<slug>` atomic") is
prose about a sibling, and passes.

**`## Done when`** — checks that can FAIL: an output, a file, an exit code.
"The check is silent", not "the index is tidy".

**`## Fails when`** — a `seen | means | do` table: the line, exit code or state
the run hit, what it meant, what closed it. EMPTY at `runs: 0`, filled from a
run, never from reading the code. No log section — a lesson folds into `## Do`
or this table, `updated` moves, and git holds what it replaced.

# atomic.md — how to fill it, and why each line is there

The template is @references/templates/atomic.md. `pearde workflow add atomic
<subject>` writes the frontmatter itself — slug key, `subject`, `date`,
`runs: 0`, and a `tags:` derived from the slug key — and takes the body
from the template's shape. @references/workflow.md
is the format; @resources/workflows.py checks it.

## Frontmatter

The keys are a CLOSED set, and exactly one slug key: `atomic` here, `workflow`
in @references/templates/workflow.md. An undeclared key is a typo and the check
fails on it.

| key | is |
|---|---|
| `atomic` | the slug — equals the filename without `.md` |
| `subject` | one line — the unit of work |
| `date` | the day it was written. Written, never stamped |
| `updated` | optional — the day the text last changed from a run |
| `runs` | runs this file was in — one collect, one count. Integer >= 0 |

## Sections

**`## Do`** — numbered imperative steps, each naming the command and the file:
`python3 resources/index.py check`, not "verify the index". ONE unit of work,
small enough to close in one sitting. An atomic that needs "and then" is two
atomics and a workflow ordering them. Name commands and files — never an
agent, a tool, a hook or a vendor.

**`## Done when`** — checks that can FAIL: an output, a file, an exit code.
"The check is silent", not "the index is tidy".

**`## Fails when`** — a `seen | means | do` table: the line, exit code or state
the run actually hit; what it meant; what closed it. EMPTY at `runs: 0`, and
filled only from a run — never from reading the code and guessing. No log
section: a lesson is folded into `## Do` or into this table, and `updated`
moves. Git holds what it replaced.

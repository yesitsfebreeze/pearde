# workflow.md — how to fill it, and why each line is there

The template is @references/templates/workflow.md. `pearde workflow add
<subject>` writes the frontmatter itself — slug key, `subject`, `date`,
`runs: 0`, and a `tags:` derived from the slug key — and takes the body
from the template's shape. Every atomic a step
names exists first, or the step sends a worker nowhere. @references/workflow.md
is the format; @resources/workflows.py checks it.

## Frontmatter

The keys are a CLOSED set, and exactly one slug key: `workflow` here, `atomic`
in @references/templates/atomic.md. An undeclared key is a typo and the check
fails on it.

| key | is |
|---|---|
| `workflow` | the slug — equals the filename without `.md` |
| `subject` | one line — the job this routes |
| `date` | the day it was written. Written, never stamped |
| `updated` | optional — the day the text last changed from a run |
| `runs` | runs this file was in — one collect, one count. Integer >= 0 |

## Sections

**`## Use when`** — the jobs this fits, named the way a request arrives, and
the near-miss it does NOT fit with the slug that does. This is the lookup, so
the boundary earns its bullet.

**`## Steps`** — a `# | atomic | why | on failure` table.

- `#` counts from 1, contiguous.
- `atomic` is a slug in this directory.
- `why` is what the step buys the job — NEVER the atomic's `subject` restated.
- `on failure` is `→ N` with N earlier than this row, or `stop`. No forward
  jump: a step that may be skipped is not a step. A back-edge is taken at most
  twice per run; the third failure at one step is a stop. `→ 1` on every row
  is a list, not a workflow.

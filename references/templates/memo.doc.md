# memo.md — how to fill it, and why each line is there

The template is @references/templates/memo.md. `pearde memo add <subject>`
copies it, filling `memo`, `kind`, `subject`, `date` and the title; an
invariant also gets a bare `verify:` line, which fails `check` until the command
is written and run — an invariant is filed proven, never on faith.
@references/memo.md is the format; @resources/memos.py checks it.

## Frontmatter

Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a typo
`doctor` fails on.

| key | is |
|---|---|
| `memo` | the slug — the filename without `.md` |
| `kind` | `decision` \| `note` \| `invariant` |
| `status` | `open` \| `decided` \| `superseded` |
| `subject` | one line — what this memo settles |
| `date` | the day the call was recorded, never stamped |

Optional:

| key | is |
|---|---|
| `verify` | invariant only, and required there — a command exiting 0 while the invariant holds, run from the repo root |
| `updated` | only on a substantive revision, never for a path fix |
| `prds` | list — board-relative PRD dirs this memo governs |
| `supersedes` | the slug this replaces |
| `superseded_by` | the slug that replaced this |
| `tags` | generated, never typed — `memo`, `kind/<kind>`, `status/<status>`, so the graph view can colour a memo. `memo add` writes it, `memo retag` rewrites it |

## Sections

**`## Decision`** — what was settled, in the present tense: the rule as it
stands, never the story of arriving at it. Short enough to quote.

**`## Why`** — the argument, and the part that must survive: a reader six
months out reconstructs it without you. Name the forces — what was breaking,
what constraint bit, what the cheap option cost.

**`## Alternatives considered`** — one bold entry per road, with what it was
and the count it lost on. Be specific: "slower" is no reason; "it re-reads the
whole board on every state change, which the progress line calls" is. NEVER
empty — a memo with no alternatives is a claim, not a decision, and no later
reader can tell a road rejected from one never seen. Where nothing else was
considered, say so and why.

**`## Consequences`** — what this costs in work or in freedom given up, and
what it deliberately does NOT fix: the next memo's problem, named.

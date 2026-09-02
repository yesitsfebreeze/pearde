# memo.md — how to fill it, and why each line is there

The template is @references/templates/memo.md. `pearde memo add <subject>`
copies it, filling `memo`, `kind`, `subject`, `date` and the title; an
invariant also gets a bare `verify:` line, which fails `check` until the
command is written and run — an invariant is filed proven, never on faith.
@references/memo.md is the format; @resources/memos.py checks it.

## Frontmatter

Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a typo
and `doctor` fails on it.

| key | is |
|---|---|
| `memo` | the slug — equals the filename without `.md` |
| `kind` | `decision` \| `note` \| `invariant` |
| `status` | `open` \| `decided` \| `superseded` |
| `subject` | one line — what this memo settles |
| `date` | the day the call was recorded. Written, never stamped |

Optional:

| key | is |
|---|---|
| `verify` | invariant only, and required there — a command that exits 0 while the invariant holds, run from the repo root |
| `updated` | only on a substantive revision; never for a path fix |
| `prds` | list — board-relative PRD dirs this memo governs |
| `supersedes` | the slug this replaces |
| `superseded_by` | the slug that replaced this |
| `tags` | generated, never typed — `memo`, `kind/<kind>`, `status/<status>`, so the graph view can colour a memo. `memo add` writes it and `memo retag` rewrites it |

## Sections

**`## Decision`** — what was settled, in the present tense. The rule as it now
stands, not the story of arriving at it. Short enough to quote.

**`## Why`** — the argument. This is the part that has to survive: a reader
six months out should reconstruct the reasoning without you in the room. Name
the forces — what was breaking, what constraint bit, what the cheap option
cost.

**`## Alternatives considered`** — one bold entry per road, with what it was
and the count it lost on. Be specific: "slower" is not a reason; "it re-reads
the whole board on every state change, which is the thing the progress line
is called from" is. NEVER empty. A memo with no alternatives is a claim, not a
decision, and nobody can later tell whether the other road was walked and
rejected or never seen. If nothing else was considered, that is the finding:
say so, and say why the choice was forced.

**`## Consequences`** — what this now costs, in work or in freedom given up;
and what it deliberately does NOT fix — the next memo's problem, named.

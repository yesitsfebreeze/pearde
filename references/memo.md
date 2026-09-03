# Memos

A PRD says what to build; a memo, what was decided and what it beat. The PRD
stops mattering at `done`; the memo outlives the work.

```
.pearde/memos/<slug>.md
```

- No `state`. Never claimed, specced, or dispatched.
- `memos/` holds no `prd.md`: scan walks past, the progress line counts none.
- One flat directory, no nesting. A memo is found by its slug.
- On the board anyway: a decision off the next session's path is one nobody
  has.

## Frontmatter — a closed set

```
---
memo: one-writer
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: why the orchestrator is the only writer of PRD state
date: 2026-08-23
prds:
  - p2-parallel-dispatch
---
```

| key             | required | is                                                            |
|-----------------|----------|----------------------------------------------------------------|
| `memo`          | yes      | the slug — the filename without `.md`                          |
| `kind`          | yes      | `decision`, a call made; `note`, source folded in and arguing nothing of ours; `invariant`, a rule that must hold, proved by its `verify:` |
| `status`        | yes      | `open`, `decided`, `superseded`. One word; a status needing a sentence belongs in the body |
| `subject`       | yes      | one line: what this memo settles                               |
| `date`          | yes      | the day the call was recorded, ISO 8601 only. **Written, never stamped**: a generated date moves on every sweep, mtime sorts by last touch, padded spelling makes string comparison date comparison |
| `verify`        | invariant only | the command exiting 0 while the invariant holds. Required here, forbidden on every other kind |
| `updated`       | no       | set only on a *substantive* revision                           |
| `prds`          | no       | board-relative PRD dirs this memo governs. A list              |
| `supersedes`    | no       | the slug this replaces                                         |
| `superseded_by` | no       | the slug that replaced this                                    |
| `tags`          | generated | `memo`, `kind/<kind>`, `status/<status>`, derived from the two keys above and never typed — the graph colours by tag and cannot query a key. `memo add` writes them, `memo retag` rewrites the lot |

A misspelled key reads as present, so anything outside the set fails.

Dialect: a `---` fence, one `key: value` per line, `-` items for lists,
matched by name at any indentation — as `prd.md` and a spec do, one parser
reading all three.

## Body

Per `@references/templates/memo.md`:

| section                     | holds                                              |
|-----------------------------|-----------------------------------------------------|
| `## Decision`               | what was settled, present tense                    |
| `## Why`                    | the argument — the part that has to survive. On recorded knowledge, wikilinks the conclusion `[[<slug>]]` under `.pearde/wiki/conclusions/`: the memo cites, the KB holds the provenance, the body argues |
| `## Alternatives considered`| what lost, and on what count. Never empty — a memo with no alternatives is a claim, not a decision |
| `## Consequences`           | what this costs, including what it does not fix    |

`Why` and `Alternatives considered` are the board's one place for paragraphs,
per @references/language.md. Compress them.

## Invariants

`kind: invariant` is the one testable memo — a rule the board must not break,
filed with `verify:`, a shell command run from the repo root. A rule nobody
can run is a claim.

```sh
python3 @resources/memos.py verify [board]         # run every binding invariant
python3 @resources/memos.py verify <slug> [board]  # just this one
```

Filed **proven, never on faith**: write the command and run `verify <slug>`
before the memo is done. `memo add --kind invariant` leaves `verify:` bare,
failing the check until written. Re-run `verify` whenever a change might bend
one. A broken invariant stops the pass — either the change is wrong, or the
invariant is dead and goes `superseded` with a memo saying why, no longer
binding.

The check refuses an invariant without a command but never runs one — fast and
side-effect free. Executing is `verify`'s job.

## The index

`memos/README.md` indexes by kind — invariants first, because they bind now,
then decisions, then notes, newest first within each. **Generated**: `memo
index` writes it, `memo add` rewrites it after every new file, the check
failing on a stale one. `scan` skips it, the index being no memo; an external
`memos:` dir gets none, read-only.

## An external source

A repo whose decisions live elsewhere does not move them — one fact, one
home. Point `memos:` in `.pearde/settings.md` at that dir:

```yaml
memos: ../.mi/docs/memos
```

Read-only, every scalar frontmatter key rendered as-is. The check verifies
only the universal, that the file parses and the required five are present.
The closed set binds the board's own `memos/`.

## The check

`doctor.sh` reports `memos`; `python3 @resources/memos.py check [board]` is
that check, run against the real board and never a fixture. Failures:

- a `kind` or `status` word outside the closed set
- a slug that disagrees with its filename
- a required key missing, or a key nobody declared
- a date not ISO 8601, or an `updated` preceding its `date`
- `status: superseded` naming no `superseded_by`, or naming a missing memo
- `prds:` naming what is not a PRD on this board
- an invariant without a `verify:` command, or a `verify:` on any other kind
- a `tags:` disagreeing with this memo's kind and status — repaired by
  `python3 @resources/memos.py retag [board]`, never by hand
- a `README.md` index no regeneration from the tree would produce

## Why the board, not a docs folder

`memos/` is one directory deeper on a path the session already walks.
Rejected:

- **`docs/` at the repo root** — reads fine for a human, invisible to the
  loop. Memos beside the PRDs let `prds:` name a sibling the check verifies.
- **Status as the folder** (`open/`, `decided/`, …) — moving a file to change
  a status rots every inbound link.

# Grammar

A **grammar** says what the words mean — every term this repo gives a meaning
of its own, so session, worker and person name one thing one way.

```
.pearde/grammar.md
```

- One file, not a directory. A term is one row; a vocabulary read a term at a
  time goes unread.
- No `state`. Never claimed, specced, or dispatched — invisible to `scan` and
  the progress line, yet where the next session looks.
- Every board has one, written by `pearde init` from
  @references/templates/grammar.md with the board vocabulary in it; a board
  adds its **own** words.
- `grammar:` in `.pearde/settings.md` points elsewhere, default `grammar.md` —
  several boards over one codebase share one vocabulary.

## Frontmatter — a closed set, like a memo's

```
---
grammar: pearde
subject: the words this repo gives a meaning of its own
date: 2026-09-02
updated: 2026-09-02
---
```

| key       | required | is                                                        |
|-----------|----------|------------------------------------------------------------|
| `grammar` | yes      | whose vocabulary this is — the board's `name:` where it has one |
| `subject` | yes      | one line: what this file settles                           |
| `date`    | yes      | the day it was started. ISO 8601, written never stamped    |
| `updated` | no       | the day a term was last added or changed                   |

A misspelled key reads as present.

## Body

`## <group>` headings, each holding one table. A group is a subject, not a
letter — a reader knows a word's kind long before its spelling, alphabetical
order seating a term beside an unrelated one. Under the heading go that
group's rule files, `@<path>` addresses per @index.md. The row is the meaning,
the rule stays there.

```markdown
## States, and what moves them

@references/parts/states.md

| term | is |
|---|---|
| `open` | claimable for analysis |
| **parked** | any `state` outside the nine. Never dispatched, never scheduled |
```

- **Backticked where the term is literal text on disk** — a key, a state, a
  command, a filename — and **bold where the term is a concept**. The
  spelling is the lookup, matching the tree.
- **One line, present tense, no hedging** — @references/language.md, as
  everywhere else on the board.
- **A definition names the thing it is about.** "The relevant setting" is not a
  definition; `claim-ttl` is.

## The collision table

A word with two meanings gets a three-column row beside its existing
definitions — not what the word means but which meaning is in play:

```markdown
| the word | here | and here |
|---|---|---|
| **sweep** | the pass over silent claims | a scout run that snapshots every bucket |
```

The checker tells the two tables apart by column count, never by heading — a
board writes its headings in its own `language`.

## What never enters a grammar

- **A word meaning everywhere what it means here.** A glossary defining
  "file" teaches nobody.
- **A former name.** Rename a thing and the row moves with it; git holds what
  it replaced, a stale row reading as current — @references/language.md.
- **A rule.** A row says what a word means; what the thing must do is in the
  file the group heading names — two homes for one rule can disagree.

## Who writes it

The orchestrator, on the transition introducing the word — when a memo is
written, and for the same reason: an unwritten word is re-derived next session
under a different spelling. A worker never writes here; a word it missed goes
in its report, the orchestrator adding the row with the collect.

```sh
python3 @resources/grammar.py list  [board]           # term · group · meaning
python3 @resources/grammar.py show  <term> [board]    # one term, and its collision row
python3 @resources/grammar.py brief [board]           # the vocabulary as one page
python3 @resources/grammar.py add   <term> <meaning> [board] [--group <g>]
python3 @resources/grammar.py check [board]           # what doctor reports for `grammar`
python3 @resources/grammar.py stale [board]           # rows whose term is nowhere in the repo
python3 @resources/grammar.py undefined [board]       # words the board uses that no row defines
python3 @resources/grammar.py init  [board]           # write the file from the template
```

`brief` is what a worker is handed — `term — meaning`, one per line, no table
syntax or group prose. `show` is the mid-job one-term lookup: a vocabulary
read whole sits in the window all session.

## The check

@resources/grammar.py alone reads this format; the `doctor` row `grammar` runs
it. Failures:

- no `---` fence, or one unterminated
- a required key missing, or a key nobody declared
- a date not ISO 8601, or an `updated` preceding its `date`
- a table row that is neither two columns nor three
- an empty term, or a term with no meaning
- one term defined twice — the lookup is the spelling, so two meanings belong
  in the collision table, not in two rows

`stale` and `undefined` are judgements, not defects — no part of the check,
never failing `doctor`. `stale` lists terms found nowhere else in the repo,
candidates for deletion: a word said in passes and never typed is what this
file exists for. `undefined` names every word the board uses that no row
defines, and only what enumerates without prose:

- every `@@<keyword>` under the board and in @index.md
- every frontmatter key in `.pearde/prds/**/prd.md` and their `specs/*.md`
- every key in `.pearde/settings.md`

One line per word — `<word> — <where it is used, first hit>`, sorted. Keys and
scopes are the limit, so a word only in prose escapes.

## Why one file, and the shapes rejected

- **A directory of one file per term**, the shape `memos/` uses — a memo
  carries an argument and is read alone; a term is one line, read beside its
  neighbours. Two hundred files is two hundred reads.
- **A `## Glossary` section in the README** — the README has a human reader
  and one shape, quickstart then rings. A vocabulary is read cold and mid-job
  by an agent, and grows as words are coined.
- **Generating it from the tree** — a definition is a judgement; what extracts
  is the spelling, the half nobody was missing.

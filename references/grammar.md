# Grammar

A PRD says what to build, a memo says what was decided, a workflow says how a
job is done. A **grammar** says what the words mean — every term this repo
gives a meaning of its own, so a session, a worker and a person name the same
thing the same way.

```
.pearde/grammar.md
```

- One file, not a directory. A term is one row, and a vocabulary read a term at
  a time is a vocabulary nobody reads.
- No `state`. Never claimed, specced, or dispatched — invisible to `scan` and
  to the progress line, yet on the board, where the next session looks.
- Every board has one. `pearde init` writes it from
  @references/templates/grammar.md, already holding the board vocabulary; what
  a board adds is its **own** repo's words.
- `grammar:` in `.pearde/settings.md` points elsewhere, default `grammar.md` —
  several boards over one codebase share one vocabulary.

## Frontmatter

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

The set is **closed**, like a memo's — a misspelled key reads as present.

## Body

`## <group>` headings, each holding one table. A group is a subject, not a
letter: a reader looking for a word knows what kind of thing it is long before
they know how it is spelled, and an alphabetical list is the one ordering that
guarantees a term sits beside a term it has nothing to do with.

Under the heading, the files that hold the rules for that group — `@<path>`
addresses, per @index.md. The row is the meaning; the rule stays there.

```markdown
## States, and what moves them

@references/parts/states.md

| term | is |
|---|---|
| `open` | claimable for analysis |
| **parked** | any `state` outside the nine. Never dispatched, never scheduled |
```

- **The term is backticked where it is literal text on disk** — a key, a
  state, a command, a filename — and **bold where it is a concept**. The
  spelling is the lookup, so it matches the tree exactly.
- **One line, present tense, no hedging** — @references/language.md, the same
  rules as everything else on the board.
- **A definition names the thing it is about.** "The relevant setting" is not a
  definition; `claim-ttl` is.

## The collision table

A word with two meanings gets a row in a three-column table, beside whatever
definitions it already has — the reader's question there is not "what does this
mean", it is "which of the two is this":

```markdown
| the word | here | and here |
|---|---|---|
| **sweep** | the pass over silent claims | a scout run that snapshots every bucket |
```

The checker tells the two tables apart by their column count, never by the
heading — a board writes its headings in its own `language`.

## What never enters a grammar

- **A word that means everywhere what it means here.** A glossary that defines
  "file" teaches nobody the one word they were missing.
- **A former name.** Rename a thing and the row moves with it; git holds what
  it replaced. A stale row reads as current — @references/language.md.
- **A rule.** A row says what a word means. What the thing must do is the file
  the group heading names, and two homes for one rule is one rule that can
  disagree with itself.

## Who writes it

The orchestrator, on the transition that introduces the word — the same moment
a memo is written, and for the same reason: the call is fresh, and a word
nobody wrote down is re-derived by the next session under a different spelling.

A worker never writes here. A word it needed and did not find goes in its
report, and the orchestrator adds the row with the collect.

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
syntax and no group prose. `show` is the one-term lookup a worker makes
mid-job, and it is the call to reach for: a vocabulary read whole is in the
window for the rest of the session.

## The check

@resources/grammar.py is the only reader of this format, and the `doctor` row
`grammar` is that check. It fails on:

- no `---` fence, or one unterminated
- a required key missing, or a key nobody declared
- a date that is not ISO 8601, or an `updated` preceding its `date`
- a table row that is neither two columns nor three
- an empty term, or a term with no meaning
- one term defined twice — the lookup is the spelling, so two meanings under
  one spelling belong in the collision table, not in two rows

`stale` is not part of the check and never fails `doctor`: it lists every term
that appears nowhere else in the repo, which is a candidate for deletion and a
judgement, not a defect. A term can be real and unwritten — a word said in
passes and never typed is exactly the word this file exists for.

`undefined` runs the other direction, and has the same standing: never part of
the check, never a `doctor` failure — what a word should mean is the author's
to say. It lists every word the board uses that no row defines, and it reads
only what can be enumerated without reading prose:

- every `@@<keyword>` under the board and in @index.md
- every frontmatter key in `.pearde/prds/**/prd.md` and their `specs/*.md`
- every key in `.pearde/settings.md`

One line per word — `<word> — <where it is used, first hit>`, sorted. That
scope is the limit: it reads keys and scopes, so a word reintroduced in prose
alone is used by nobody it reads and is not caught by it.

## Why one file, and the shapes rejected

- **A directory of one file per term**, the shape `memos/` uses — a memo
  carries an argument and is read alone; a term is one line and is read beside
  the terms around it. Two hundred files is two hundred reads to answer "what
  do we call this".
- **A `## Glossary` section in the README** — the README has a human reader
  and one shape (quickstart, then rings). A vocabulary is read by an agent,
  cold, mid-job, and it is the one document that grows every time a word is
  coined.
- **Generating it from the tree** — a definition is a judgement. What can be
  extracted is the spelling, which is the half nobody was missing.

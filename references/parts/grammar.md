# Grammar

What the words mean, kept where the next session looks.

A PRD says what to build, a memo what was decided, a workflow how a job is
done. A **grammar** says what a word means on this board.
@references/grammar.md is the format, the closed frontmatter set, the collision
table and the check.

```
.pearde/grammar.md
```

- No `state`. Never claimed, specced or dispatched — invisible to `scan` and to
  the progress line, yet on the board.
- One file, one table per group, one row per term. `grammar:` in
  `.pearde/settings.md` points elsewhere, default `grammar.md`.
- `pearde init` writes it from @references/templates/grammar.md, already
  holding the board vocabulary. What a board adds is its own repo's words.
- Frontmatter is a **closed set**: `grammar`, `subject`, `date`, `updated`.

## When a row is written

| moment                              | what happens                                          |
|-------------------------------------|--------------------------------------------------------|
| a word is coined in a pass          | the orchestrator adds the row on the transition that introduced it |
| a worker did not find a word it needed | it says so in its report; the row lands with the collect |
| a word turns out to have two meanings | the two rows become one row in the collision table    |
| a thing is renamed                  | the row is rewritten. Never a second row, never a former name |

An entry is from use, never from reading. A word nobody has said yet is not a
term; a word said twice under two spellings already cost more than the row.

## Handed to a worker

The brief names the file and the one-term lookup, never the vocabulary itself:

```sh
python3 @resources/grammar.py show <term>   # one term, and its collision row
python3 @resources/grammar.py brief         # the whole vocabulary, one line per term
```

`show` is the call a worker makes mid-job. `brief` is for a worker whose
contract is written in the board's own words end to end — a vocabulary read
whole stays in the window for the rest of the session, the cost
@references/parts/loop.md's second rule is about.

## What it is not

- **A style guide.** How a document is written is @references/language.md; a
  row says what the thing is called.
- **A rule book.** A row says what a word means. What the thing must do stays
  in the file the group heading names.
- **A search index.** No ranking, no tags. `list`, `show` and the group
  headings are the whole lookup.

```sh
python3 @resources/grammar.py list  [board]        # term · group · meaning
python3 @resources/grammar.py add   <term> <meaning> [board] [--group <g>]
python3 @resources/grammar.py check [board]        # what doctor reports for `grammar`
python3 @resources/grammar.py stale [board]        # terms that appear nowhere in the repo
python3 @resources/grammar.py undefined [board]    # words the board uses that no row defines
```

---
name: pearde-grammar
description: What the words mean on this board — one file holding every term this repo gives a meaning of its own, so a session, a worker and a person name the same thing the same way. Read the vocabulary, look one term up mid-job, add a row when a word is coined, check the file. Use for "/grammar", "what do we call this", "what does <term> mean here", "define this term", "add a word to the vocabulary", "check the grammar", "is that the right word for it", "what is the word for this", "which of the two meanings is this". A row is written from use, never from reading.
---

Read @references/parts/grammar.md for when a row is written and what is handed
to a worker, @references/grammar.md for the format — the closed frontmatter
set, the group tables, the collision table, the check, and what never earns a
row. @references/templates/grammar.md is the file a board starts from. The
scope is `@@grammar`.

```sh
python3 @resources/pearde.py grammar list [board]         # term · group · meaning
python3 @resources/pearde.py grammar show <term> [board]  # one term, and its collision row
python3 @resources/pearde.py grammar add <term> <meaning> [board] [--group <g>]
python3 @resources/pearde.py grammar check [board]        # what doctor reports for `grammar`
```

`grammar` forwards to @resources/grammar.py, the only reader of that format.
`show` is the call a worker makes mid-job; `brief` prints the whole vocabulary,
one line per term, for a contract written in the board's own words end to end.

A word earns a row when it means something here that it does not mean in
ordinary English, or when it stands beside a word it is not. A word with two
meanings gets one row in the collision table, never two rows — the lookup is
the spelling.

`stale` lists every term that appears nowhere else in the repo; `undefined`
runs the other direction, over the `@@` scopes and the frontmatter and
settings keys the board uses. Both are judgements, never defects, so neither
fails a check.

The grammar lives at `.pearde/grammar.md`, so a board is needed to read one.
With none in scope, say where the file would be; adding a row is an
orchestrator write, and it does not happen uninvited.

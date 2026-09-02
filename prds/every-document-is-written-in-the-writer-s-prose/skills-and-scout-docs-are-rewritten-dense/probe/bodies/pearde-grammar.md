
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
`show` is the call a worker makes mid-job; `brief` prints the whole
vocabulary, one line per term, for a contract written end to end in the
board's own words.

A word earns a row where the board's meaning parts from the ordinary English
one, or where the word sits beside a look-alike of another meaning. A word with two
meanings gets one row in the collision table, never two — the lookup is the
spelling.

`stale` lists every term appearing nowhere else in the repo; `undefined` runs
the other direction, over the `@@` scopes and the frontmatter and settings
keys the board uses. Both are judgements, never defects, so neither fails a
check.

The grammar lives at `.pearde/grammar.md`, so reading one needs a board. With
none in scope, say where the file would be; adding a row is an orchestrator
write and does not happen uninvited.

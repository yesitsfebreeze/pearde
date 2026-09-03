---
name: pearde-memo
description: Record a decision the code will not explain, and check the ones on record — one file per call holding what was decided, what it beat and why; a checker enforces the keys, invariants carry a verify command, an index by kind is generated. Use for "/memo", "memo <subject>", "record this decision", "why did we choose X", "check the memos", "record an invariant", "verify the invariants", "adr".
---

Read @references/parts/memos.md for when a memo is owed, @references/memo.md
for the format and the closed frontmatter set, @references/templates/memo.md
for the file. The scope is `@@memos`.

```bash
python3 @resources/pearde.py memo list [board]    # slug · kind · status · date · subject
python3 @resources/pearde.py memo add <subject> [--kind <kind>]  # a new memo, slugged from the subject
python3 @resources/pearde.py memo check [board]   # what doctor reports for `memos`
python3 @resources/pearde.py memo verify [slug] [board]  # run every invariant's `verify:` command
python3 @resources/pearde.py memo index [board]   # regenerate memos/README.md, the index by kind
python3 @resources/pearde.py memo retag [board]   # rewrite every `tags:` from its own kind and status
```

`memo` forwards to @resources/memos.py, the only reader of that format.

Write one at the moment the call is made, not when the work lands: a memo
exists because a future reader asks "why is it like this" and the code will
not answer.

An **invariant** (`--kind invariant`) is the one testable memo — a rule
required to keep holding, carrying a `verify:` command that exits 0 while it does.
File it proven: write the command, then run `memo verify <slug>`. Re-run `memo
verify` whenever a change might bend one. A broken invariant is a stop, not a
warning.

Memos live at `.pearde/memos/`, so filing one needs a board. With none in
scope, write the memo and say where it goes.

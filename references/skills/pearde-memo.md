---
name: pearde-memo
description: Record a decision the code will not explain, and check the ones on record — one file per call, holding what was decided, what it beat, and why, never buried in a PRD. Slugged from the subject, with a closed set of frontmatter keys that a checker enforces; invariants carry a verify command and an index by kind is generated beside them. Use for "/memo", "memo <subject>", "record this decision", "write this down as a decision", "why did we choose X", "what did we decide about Y", "check the memos", "record an invariant", "is the invariant still true", "verify the invariants", "adr", "decision record", "document this tradeoff". Write it when the call is made, not when the work lands.
---

Read @references/parts/memos.md for when one is owed, @references/memo.md for
the format and the closed frontmatter set, @references/templates/memo.md for
the file. The scope is `@@memos`.

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
exists because a future reader will ask "why is it like this" and the code
will not answer.

An **invariant** (`--kind invariant`) is the one testable memo: a rule that
must keep holding, carrying a `verify:` command that exits 0 while it does.
File it proven — write the command, run `memo verify <slug>` — and re-run
`memo verify` whenever a change might bend one. A broken invariant is a stop,
not a warning.

Memos live at `.pearde/memos/`, so a board is needed to file one. With none in
scope, write the memo and say where it should go.

# Memos

What was decided, and what it beat.

A PRD says what to build. A **memo** says what was decided and what it beat,
and outlives the work it governed. @references/memo.md is the format, the
closed frontmatter set, and the argument for putting it on the board.

```
.pearde/memos/<slug>.md
```

- No `state`. Never claimed, specced, or dispatched — invisible to scan and to
  the progress line, yet on the board, where the next session looks.
- Frontmatter is a **closed set**. Anything else fails `doctor` — the one
  inversion of the frontmatter contract, because the memo table is a fold over
  declared keys.
- `## Alternatives considered` is never empty — a memo with no alternatives is
  a claim.
- `kind: invariant` is the testable memo: a rule that must keep holding,
  carrying a `verify:` command that exits 0 while it does. Filed proven,
  re-run by `verify` whenever a change might bend it.
- `memos/README.md` is the index by kind — generated, never maintained;
  `check` fails when it is stale.

```sh
python3 @resources/memos.py list [board]    # slug · kind · status · date · subject
python3 @resources/memos.py check [board]   # what doctor reports for `memos`
python3 @resources/memos.py verify [board]  # run every invariant's command
python3 @resources/memos.py index [board]   # regenerate the kind index
```

Write one when a call is made that the code will not explain: a rule the board
follows, a road not taken, a constraint that looks arbitrary. Not for what a
commit message covers.

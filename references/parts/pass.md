# The pass file

`.pearde/.state/pass.md` — the session's own memory, fifteen lines, rewritten at every
transition. Machine-local and git-ignored, like `.pearde/.state/plan.json`: one
session's holding, never the board's.

A context window ends without warning, and everything the pass worked out —
which PRD is being collected, what a check returned, what the user answered,
what is owed — goes with it. The cheapest thing the session can do next is
then the most expensive: re-read the specs, re-run the sweeps, re-derive the
conclusion it already had. The alternative costs one write per transition.

## What goes in it

Only what `@resources/board/plan.py scan` cannot print. The scan already has
every state, weight, gate, claim and box count, and a copy of those goes wrong
the moment a worker moves.

```markdown
# Pass — <what this pass is doing>

## Established
- <fact> — <how it was checked> · <time>

## Decided
- <decision> — <what it beat, in a clause>

## Asked
- <question put to the user> · <answered | out>

## Edits
- <slug> `## <section>` — applied | refused · <whose fault the failure was>

## Owed
- <the next action, as an action>
```

- **Established** pays for the file: a count, a diff, a command's verdict,
  with the time on it. A fact here is cited, never re-run —
  @references/parts/loop.md. Every command prints the progress line, so quote
  the line rather than computing the sum by hand.
- **Decided** holds the pass's judgment calls. A decision the code will not
  explain graduates to a memo, per @references/parts/memos.md, drafted in this
  scratch.
- **Asked** is the live frontier: what went to the user and whether it came
  back. A question here is never re-asked, and the drill gate reads the
  section — a claim over an unput frontier refuses with
  `asking N — drill first` until the pass lists the questions by title, in the
  words the scan's drill section prints, and a question marked `answered` or
  `out` stops gating.
- **Edits** is every workflow edit this pass applied or refused, per
  @references/parts/loop.md step 6. A refusal is the half that has to be
  written down: the file is unchanged, so nothing on disk records that the run
  proposed the edit or why the run turned it down, and the next pass would
  either re-refuse from scratch or take it. Empty when no worker returned a
  `## Workflow` section — omit the section, never leave a placeholder under it.
- **Owed** is one line, in the imperative, and the first thing the next turn
  does.

## When it is written

At every transition — the same moment the progress line is printed, and the
line says `pass file owed` until this file is newer than the PRD it moved.
Steps 2, 3, 6 and 7 of the loop all move something; each rewrites the file
whole before moving on. Never appended and never sectioned by pass: the file
says what is true now, with nothing to prune later.

## After a compaction

Read this file, run `scan`, act. In that order and nothing else — no spec
re-read, no tree sweep, no re-derivation of a conclusion the file already
carries. A conclusion the file does not carry is the bug: write it down this
time.

If the steps themselves are gone, re-read @references/parts/loop.md — that
one file, not the `@@loop` scope and not the reference tree behind it. A pass
that re-opens the manual after every compaction pays for the manual as many
times as it compacts.

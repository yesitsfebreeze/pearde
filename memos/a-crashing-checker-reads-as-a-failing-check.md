---
memo: a-crashing-checker-reads-as-a-failing-check
kind: decision
status: decided
subject: doctor reports a checker's own traceback as the checked thing's failure, so a broken instrument and a real red are indistinguishable from the report
date: 2026-09-01
---

# a-crashing-checker-reads-as-a-failing-check — the row blames the board for the tool's crash

## Decision

A `doctor` row that reports a failure it did not observe is an instrument
defect, and until the rows separate the two cases the rule is: **before acting
on a red doctor row, run its checker directly and read its exit path.** A red
row is a claim about the board only if the checker completed.

The reds this catches are not rare and not cheap — they send workers at
contracts that are not broken.

## Why

`doctor` printed `vision broken — 5 names in vision.md resolve to no PRD`. All
five names resolve. What actually happened was a `NameError` inside `plan.py`:
the checker died, doctor caught a non-zero exit, and rendered the row's
prepared failure text as though the check had run and disagreed with the board.

The row's text is written at the call site, before the call. It describes what
a failure *would* mean, and it is printed whenever the call does not succeed —
which conflates "I looked and it is wrong" with "I could not look". Those are
opposite findings. The first is work for the board; the second is work on the
tool, and reading it as the first is how a round spends a dispatch chasing a
contract that was never broken.

The same shape is what made this board's `vault` row untrustworthy in a
different direction — a row asserting an answer it had no way to check. A row
that speaks past what it observed is the recurring defect in this instrument,
and it is worth naming once rather than per-row.

Under @references/parts/derived.md rule 2 this is a memo: fixing it changes
nothing about what ships, only how loudly and how honestly the board reports.

## Alternatives considered

**File a derived PRD to separate the two exits** — the real repair: a checker
that exits non-zero after completing reads `broken`, one that dies reads a
third state naming the traceback. It lost at filing time on rule 2, and on the
tripwire — this board's derived count already stands at 19/19 against a
requested tree of 64, and a PRD whose entire consequence is a clearer error
string is the loop feeding on itself.

**Make doctor print the checker's stderr on every red** — cheap, and it would
have made this instance obvious in one line. It lost because it makes the
common case worse: every genuine red would carry a wall of subprocess output,
and a report nobody reads to the end is a report that hides its own findings.
Worth revisiting as "print stderr only when the exit signals a crash", which is
the same discrimination the real repair needs.

**Leave it and rely on the reader** — what the board has been doing, and it
failed here: a round read `vision broken` and believed it. A rule nobody wrote
down is not being relied on, it is being got away with.

## Consequences

- Every red row now costs one extra command before it is acted on. That is a
  real tax on rounds that read a full doctor sweep, and it falls hardest on the
  sweep case where a dozen rows are red at once.
- It deliberately does not fix the row. The discrimination between a crashed
  checker and a completed one still does not exist anywhere in `doctor.sh`, and
  the next reader who skips the extra command will make the same mistake.
- It says nothing about the other direction — a row that reads `ok` because its
  check could not run. That is the same defect mirrored, it has already bitten
  this board once on the `vault` row, and it is more dangerous, because nobody
  runs an extra command against a green row.

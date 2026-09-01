---
memo: one-author-is-not-an-accepted-spec
kind: decision
status: decided
subject: a spec whose code, probe, acceptance boxes and proof block have one author is not accepted evidence; a box is ticked only against a check that has been seen fail
date: 2026-09-01
prds:
  - seven-closed-probes-drifted-red/the-doctor-completes-without-a-home
---

# one-author-is-not-an-accepted-spec — a rubric its own author grades is not a check

## Decision

When one worker writes the code, the probe, the acceptance boxes **and** the
proof block, a later pass that re-runs those four artefacts against each other
is not verification, and the orchestrator does not collect `done` on it.

The rule that follows: **a box is ticked only against a predicate that has been
observed to fail.** Not one that could in principle fail — one that was seen
red, against a deliberately broken variant or the pre-fix tree, with the red
quoted. A box that has never been red is a sentence, not a check.

## Why

`the-doctor-completes-without-a-home` came back DONE at 8/8 boxes. Its box 3
asserted that one sentence — "Obsidian not installed here" — was **absent**
from a row whose text the same author had written. The author had chosen not to
write that sentence. The box could not fail, and it survived a DONE report
untouched.

What it was standing in front of was real. The `elif [ -z "$OBSCFG" ]` arm the
same author added turned a true `broken` into `ok` with exit 0 on the same
fixture board, by unsetting one variable — while doctor's own `plugins` row
resolved that home through `getpwuid` in the same run. The board's own gate
read green over it. The analyst wrote the artefacts; the implementer ran them;
the count was 8/8; nothing in the chain contained an observer.

The two-pass dispatch is not the defect — a second pass over a footprint
another worker built is a legitimate and cheap shape. The defect is that the
second pass inherited the first pass's rubric along with its code. A pass that
takes both has one author with two dispatches, and the second dispatch buys the
board a re-run, not a review.

The failure mode is specific and worth naming: an author writes the check
around the behaviour they built, so the check describes the build instead of
the contract. It cannot be caught by reading the box — the box reads fine. It
is caught only by asking whether anyone has seen it red.

## Alternatives considered

**Require a different worker for the second pass** — the obvious structural
fix, and it addresses authorship directly. It lost because it is expensive and
still insufficient: a fresh worker handed the same probe and the same boxes
re-runs the same tautology, and the board pays a dispatch to learn nothing. The
rubric is the problem, not the name on it.

**Have the orchestrator review every box by reading it** — what happened here,
and it worked once, at the cost of the orchestrator reproducing the central
claim by hand from the repo root. It does not scale past a board with two open
PRDs, and it puts the orchestrator's judgment inside the acceptance evidence,
which is the place the board most needs it to stay out of.

**Call the skeptic on every collect** — @references/parts/consult.md already
prescribes this before `done` on work the session implemented, and it is what
surfaced the port collision here. It lost as the *whole* answer because a
skeptic reads what it is shown: on this PRD one skeptic cleared the build and
concluded "land the collect", missing box 3 entirely. A consult is a second
reader, not a falsifiable predicate.

**Accept it and note the risk** — rejected outright. The board's states are
worth something only because `done` means a check passed. A `done` that means
an author agreed with themselves costs the board every earlier `done` too,
because a reader now has to ask which kind each one was.

## Consequences

- Every acceptance box now owes a demonstration of its own red. That is real
  work at spec-writing time — the analyst must build the broken variant, or
  name the pre-fix commit the box fails against — and it will slow
  `write-the-specs`.
- It gives the orchestrator a refusal it did not have: a DONE report at full
  box count is now declinable on the shape of the evidence alone, without
  disputing a single technical claim in it. The doctor PRD's build was and is
  correct; the collect was still withheld.
- It deliberately does not say who writes the replacement box. Here the
  orchestrator unticked two and named the predicate; the corrective implementer
  wrote it. Whether that is the general rule, or whether a failed rubric should
  go back through REFINE, is unsettled and has not yet cost anything.
- It says nothing about probes that pass by scheduling rather than by
  authorship. This PRD had one of those too — a harness binding hard-coded
  ports with no bind check, green or red depending on what else was running.
  A check that is red half the time is a different disease from a check that
  cannot be red, and it wants its own memo.

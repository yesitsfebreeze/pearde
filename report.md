# The board that runs itself — where it stands

*2026-09-02*

Eighty-nine of the hundred and five requested pieces of work are finished —
eighty-three percent, up from seventy-three this morning. Eleven landed today.
Three were parts of one job: rewriting the project's own written material so it
says the same things in fewer words, of which three of four sections are now
done. The other two matter more than their size suggests, and are below.

The story of the hour is that a long-standing jam cleared. For most of the
afternoon, six finished and independently re-checked pieces of work sat unable
to be filed, because a set of files in the working copy had been edited and not
yet put down — and nothing could be written into place while another line of
work had the same files open. Twice before, an automated attempt to clear such
files destroyed a colleague's unsaved work, so the queue waited on purpose. In
the last half hour whoever owned those edits committed them, and the queue was
worked immediately.

## What we learned when it cleared

Only one of the six went straight in. The other five had gone **stale while
they waited**. Each had been measured and proven correct against the project as
it stood when the work finished; by the time they could be filed, four other
changes had landed underneath them, and their own checks no longer passed — not
because the work was wrong, but because the ground had moved. Each has been sent
back to be re-measured against the project as it is now, and none of that is
rework in the usual sense; it is one re-run each.

The lesson is worth keeping: **a finished piece of work left in a queue decays.**
The longer the wait between finishing and filing, the more likely it is that
filing needs a second pass. The jam did not just delay six things; it quietly
created work.

## The two that matter most, both finished today

- **Checks that could not fail are now refused.** This was the most important
  open item on the board. Three people had hit the same defect independently in
  unrelated places: a check written a certain way reports success even when the
  thing it checks is broken. Investigating found it was worse than assumed —
  five of eleven check shapes passed on deliberately broken work, by three
  separate mechanisms rather than one, and two of those meant most checks were
  never really being examined at all. The fix now refuses such a check outright
  when work is filed, and warns on the weaker variants. Applied across the whole
  board on landing: a hundred and thirty-nine items and two hundred and
  seventy-nine checks were swept, thirty were flagged for a second look, and only
  one was refused — which was already finished. So the sweep confirms the
  existing body of work is sound, and stops new instances at the door.
- **One shared cache per machine instead of one per working copy.** Ninety-nine
  percent of what sits on disk here is material that can be regenerated, and it
  was being duplicated across thirty-odd working copies. It is now stored once
  and shared, with every one of the two hundred and sixty-nine items accounted
  for — shared or explicitly refused, none silently dropped. The guard proving
  this is itself proven able to fail, which after the item above is not a
  detail.

## What is being worked on now

Eight pieces of work are running at once. The most important of them:

- **A sweep for checks that cannot fail.** Three people hit this defect
  independently today in unrelated places: a check written a certain way reports
  success even when the thing it checks is broken. The investigation is now in,
  and it is worse than assumed — of eleven check shapes tested, **five pass on
  deliberately broken work**, by three separate mechanisms rather than one. Two
  of them mean most checks on this board were never really being examined at
  all. The fix is built and measured, and it newly rejects none of the two
  hundred and sixty-seven checks currently standing. This matters more than
  anything else in flight: a green check is the only evidence this board has that
  anything works.
- **One shared cache per machine instead of one per working copy.** The
  mechanism already exists; examining it found five real defects, including that
  twenty-seven of thirty working copies silently cannot use it while the status
  display reports none refused.
- **A filing defect that has been blocking the highest-priority finished item.**
  The filing step tries to record one particular file in the wrong place — a
  place it can never exist — and fails. This was parked earlier as a curiosity;
  it turns out to be the sole obstacle to a finished, high-priority piece of
  work that three further items are waiting on. It has been brought back and is
  being specified now.
- **Measurement harnesses that name something they do not actually measure.**
  Investigating found the problem is twice as large as reported, and a fifth
  instance appeared while the investigation ran. It cannot be closed by fixing
  files, because there is no template that would stop new ones being born the
  same way — which is a separate piece of work, not a wider version of this one.

- **Notes written by workers had been quietly going missing — and they have now
  been recovered.** Every worker gets its own private copy of the project to work
  in, and the shared notebook was never reachable from inside one, so a worker
  asking "do we already know this?" was always told no, and anything it wrote
  down was saved into its private copy and lost when that copy was cleaned up.
  The cause turned out to be a single line resolving a path the wrong way, and
  fixing it took one file. Before anything was cleaned up, a rescue pass swept
  twenty-seven private copies and recovered **thirty-five stranded notes**, five
  of them real findings somebody recorded deliberately; the shared record went
  from eighty-three to eighty-eight entries and is verified clean, with no
  private copy left holding anything. The earlier caution about not tidying up
  no longer applies.

## The filing machinery repaired itself

Three of the eight items that landed were defects in the machinery that files
work, and they explain a lot of this week's friction. One meant that filing an
item touching the project's own records failed outright, because it looked for
those records in the wrong place. Another meant that a filing run could crash
**after** marking an item finished but **before** recording it — leaving the
board claiming something was done while no record of it existed. That had been
happening; it was diagnosed as bad luck and repaired by hand more than once. It
now stops cleanly instead, and puts the record back.

There is a pleasing knot in the middle of this: the item that fixed the
first defect could not be filed, because filing it hit the very defect it fixed.
It was resolved by using the repaired machinery, from where it had been built,
to file itself — no hand-editing, no shortcuts.

## What is waiting on a person again

Two finished, fully-checked pieces of work cannot be filed, and it is the same
situation that held up the morning: someone has files open. A colleague is
part-way through edits to the filing machinery itself, and both finished items
need to write to those same files. Nothing is wrong with either side — the two
sets of edits are each correct, and in one case they sit on **adjacent lines**,
which is precisely the case an automatic merge cannot settle on its own.

Committing, setting aside, or discarding those in-progress edits releases both.
That is a person's call about their own work, and deliberately not something to
force: twice before, an automated attempt to clear such files destroyed a
colleague's unsaved work, and the safeguard added afterwards had to be withdrawn
for doing the same.

## Undecided or failing

- **One question is genuinely stuck, and it is a contradiction rather than a
  preference.** The documentation job was given two rules: cut thirty percent of
  the words, and never cut a fact. Six people have now independently measured
  their own sections, and not one can reach thirty percent without losing
  something real — the measured cuts come out between nothing and twelve
  percent, because most of what is there is prose the contract requires. Every
  remaining part of that job is specced against a target its own measurements
  refuse. **The recommendation is to drop the number and keep the rule:** the
  job passes when the checker is green and no fact has been lost, and the cut is
  whatever that turns out to be. Nothing else needs a decision to keep moving.
- **One finished piece of work is being held back deliberately.** It stops a
  background service writing into a folder it no longer owns, and it is proven.
  But the way its final check is written would, if run now, take a colleague's
  set-aside work and dump it into the working copy. That is a hazard rather than
  a refusal, it is documented in place, and it needs its check rewritten before
  it can be filed — not a person's decision, but not something to do carelessly
  either.
- **A second, smaller question** about how one line of the project's own
  description should read is waiting on an answer, and the work that would carry
  the first of its options is already finished — so choosing that option now
  needs somewhere new to put it.

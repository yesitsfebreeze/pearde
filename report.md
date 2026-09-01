# The board — where it stands

*2026-09-02*

**Your five answers turned into five pieces of work, and all five have already
been worked out in detail — each one was built once as a trial, proven, and
written up ready to finish properly.** Nothing is waiting on you. What decides
how fast the rest goes is simply running those five to completion, and two of
them have to go in order rather than side by side.

## Planned

Five pieces, all worked out and ready to be built. Roughly in the order they
should happen.

- **Make the self-test run trustworthy** — the tests now run a few at a time
  instead of all at once. In the trial this took failures from eight down to
  one, and cost no extra time at all. A worthwhile discovery along the way: the
  fix the code's own note recommended would have broken the health check on
  every Mac, so a different approach was used.
- **Fix the written instructions handed to everyone taking on work** — they now
  mention the one thing the filing tool refuses a write-up without, and the
  duplicated half-sentence has been removed. Following the instructions now
  produces something that is accepted.
- **Re-aim the four out-of-date self-tests** — done and proven, each shown
  failing before and passing after. Two silent ones that had quietly stopped
  checking anything were caught and fixed in the same pass. No working code was
  changed to make a test happy.
- **Make upgrading a board leave it as healthy as creating one** — the missing
  step is added, with a check that builds an old-style board, brings it
  forward, and confirms the result.
- **Make filing refuse rather than lose a file** — naming a file that cannot be
  found now stops the whole filing, instead of quietly dropping it and claiming
  otherwise.

These two must not run at the same time: fixing the written instructions
rewrites a file that one of the re-aimed tests reads. The instructions go
first.

## In work

Nothing is being built right now. All five are worked out and waiting for the
next session to finish them; that is the natural next step and needs no
decision from you.

## Undecided or failing

Nothing needs your answer. Four smaller things surfaced while the five were
being worked out, and none of them blocks anything.

- **Bringing a board forward misses a second thing too** — it also skips
  seeding the board's statement of what it is for. The health check calls this
  "not set up" rather than "broken", so it was deliberately left out of the fix
  you approved. Worth its own small piece of work if you want it.
- **The list of test results is quieter than it looks** — a check meant to
  confirm each test reports a real count only recognises one exact spelling, so
  forty-three of fifty-two are not actually being confirmed. Separate from the
  work above.
- **Three more self-tests are checking nothing** — the same kind of silent
  failure that was just fixed in two others, in three tests nobody had named.
  Left alone deliberately: fixing things the board found rather than things you
  asked for is a trade worth making on purpose, not by drift.
- **A note on file records a problem that no longer exists** — it is the last
  note still marked as needing a decision, and the crash it describes was fixed
  some time ago. It needs closing rather than answering, and will be closed the
  next time that part of the board is opened.

Set aside for now: two older items on where test code lives and how snapshots
are folded together, both untouched.

One piece of housekeeping outside all of this: the note-taking app on this
machine has accumulated seven hundred registered folders, six hundred and sixty
of which no longer exist — every temporary test board ever created registered
itself and never cleaned up. It harms nothing today and grows on every test
run.

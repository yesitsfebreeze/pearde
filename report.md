# The board — where it stands

*2026-09-01*

**Everything you asked for is finished — sixty-four of sixty-four pieces, with
nothing open and nobody working on anything right now.** The health check is
green again after one stale index was rebuilt today. But the board's own
self-tests are not all green, and that is worth a minute of your time: five of
them fail, and four of those five are tests pinned to code that has since moved
on. The fifth was this page.

## Planned

Three repairs that need no decision from you. They are small, and each is
waiting only for the next piece of work that opens the same file.

- **Re-aim four self-tests that no longer match the code** — each was written
  to guard something real, then the thing it guarded was deliberately changed
  and the test was never updated. They now fail for being out of date rather
  than for finding anything, which is the worst state for a test to be in: it
  cries wolf, and the next person learns to ignore it.
- **Delete a duplicated half-sentence from the written instructions** handed to
  everyone who takes on a piece of work. An edit some weeks ago replaced a line
  and left the old one behind, so the instructions now repeat themselves
  mid-thought.
- **Close a note that records a problem already solved.** It is the only note
  on file still marked as needing your decision, and the crash it describes was
  fixed some time ago. Left as it is, it will send someone back to you with a
  question that no longer exists.

## In work

Nothing is being worked on right now. The last two pieces landed earlier today
and the board has been idle since.

## Undecided or failing

Five things need your answer. They are being put to you as a set, so you can
settle them in one sitting.

- **Setting up versus upgrading** — creating a new board leaves it healthy;
  bringing an existing one forward skips a step and leaves it failing a check a
  new board passes. Fix it, leave it parked, or drop it?
- **Filing work can quietly lose a file** — when work is filed away you can
  name extra files to include, and any it cannot find are dropped without a
  word while the record still claims they went in. This has happened twice, and
  once it left a finished piece unfiled. Refuse to file at all in that case,
  warn out loud, or leave it?
- **The instructions omit something the filing tool demands** — a write-up that
  follows the written instructions exactly gets refused, and it only works
  today because whoever hands out the job remembers to add the missing bit
  every time. Fix the instructions, loosen the tool, or leave the reminder?
- **Four self-tests guard code that changed underneath them** — bring each back
  in line with how things work now, retire the ones whose point has passed, or
  leave them failing as a reminder?
- **The self-test run is decided partly by luck** — all forty-eight tests are
  launched at once and several compete for the same network ports, so four of
  today's nine failures were collisions rather than faults. Run them a few at a
  time so the result means something, have each stand aside when its port is
  busy, or accept the noise?

Set aside for now: the upgrade gap above, and two older items on where test
code lives and how snapshots are folded together, both untouched.

One thing outside our control: another session working in this same checkout
has a half-finished browser-testing install, so the two browser tests cannot
run. Nothing here depends on them.

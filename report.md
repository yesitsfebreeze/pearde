# Where things stand

**Everything you asked for is finished.** Sixty-four pieces of requested work,
all done, nothing open, nothing waiting on you. Three things are parked by
choice and described at the bottom; none of them blocks anything.

## What finished today

Two pieces of work landed, and both took longer than they should have for the
same reason, which is worth telling you about because it changed how the board
now works.

The first was a fault in the health check. Run it in a stripped-down shell —
the kind a scheduled job or a container gives you — and it stopped dead
partway through, silently, leaving twelve of its rows unprinted. The cause was
one line reading the user's home directory without checking whether there was
one. That part was diagnosed correctly on the first attempt and the fix was
right.

What took three attempts was proving it. The first report claimed the job was
done against a test that could not fail: the person who wrote the code also
wrote the test, and wrote it to check that a particular sentence was absent
from a message they had themselves chosen not to write. It passed because
nothing could have made it fail. We refused it. The second attempt rewrote the
test properly, but fixed the underlying behaviour by calling out to Python —
and in exactly the stripped-down environments this work exists to serve,
Python often is not there. A reviewer broke it in ten minutes. The third
attempt solved it with a shell builtin that needs nothing installed at all, and
that one held up under everything we could throw at it.

The second piece was setting up a new board so that the health check passes on
it from the first minute. That one went more smoothly, partly because the
lesson above was written down first: the person doing the work was told to
attack the tests rather than re-run them, and found a real fault nobody had
spotted — a failure during setup that was being swallowed, so the command
reported success while leaving the board broken. That is now fixed and proven.

## What changed about how the work gets checked

Four rules came out of the above and are now on the record:

- A test counts as evidence only if someone has watched it fail. Not "could
  fail in principle" — actually seen red, with the failure quoted.
- Work checked only by the person who wrote it is not checked. A second pass
  that re-runs the first pass's own tests proves nothing.
- A test that skips itself says "skipped", and a skip is never counted as a
  pass. We found one quietly counting itself as a pass when it stood aside.
- A check whose result depends on what else happens to be running is not
  evidence. Several tests were fighting over the same network ports and going
  green or red by luck.

These are already paying for themselves — the second piece of work above found
a genuine fault precisely because the person was held to them.

## Two rough edges in the tooling itself

Both are recorded, neither is fixed, and you may want to know about them.

The command that files finished work will accept a list of extra files to
include, quietly ignore any it cannot find, and then write a commit message
that names them anyway. That happened once today: a commit describes ten files
it does not contain. The files were re-filed correctly straight afterwards, but
a record that claims something the archive does not hold is the kind of thing
worth fixing rather than remembering. A related version of the same fault left
one finished file uncommitted; it was caught and filed by hand, with an
explanation attached.

Separately, one of the older test scripts prints a column of zeroes instead of
its real counts, because of a formatting mistake. Three people worked around it
today rather than fixing it, each spending time rediscovering that the zeroes
mean nothing.

## Parked, and why

- **Setup versus upgrade.** Creating a new board now leaves it healthy;
  bringing an *existing* board forward still misses one step and leaves it
  failing the same check. It is a one-line fix and the proof around it is the
  real work. Parked rather than started, because it is beyond what you asked
  for and the choice to spend time on it is yours.
- **Two older items** on where test code lives and how snapshots are folded
  together, both untouched and both still parked from before.

## One thing outside our control

Another session working in the same checkout installed a browser-testing
package this afternoon. Its files are not tracked, which makes one of the
project's own consistency checks report 115 problems and turns three unrelated
status lines red. None of it is caused by the work above, and it was verified
line by line that none of the 115 complaints names any file this work touched.
It will clear when that session finishes or the files are ignored deliberately.

---
state: claimed
origin: derived
from: the-board-is-a-real-directory-at-pearde-never-a-symlink/init-and-upgrade-write-the-dotted-board
priority: 95
complexity: 32
blast-radius:
claim: impl-harness-nodispatch2 2026-09-03 21:03
---


# a harness never dispatches the live board

A probe belonging to a `done` PRD launches real dispatchers against the real
board every time it runs. This is the cause of both fan-out incidents on
2026-09-03, and neither was diagnosed correctly at the time — the 09:16 one was
attributed to the two board aliases, the 11:56 one to four hand-invocations.
Both attributions are wrong. Nobody typed those commands.

## What was measured

At 12:03:37 on 2026-09-03 the process tree of a pass worker on
`the-board-is-a-real-directory-at-pearde-never-a-symlink/init-and-upgrade-write-the-dotted-board`
read, child last:

    81190 bash .../the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
    81193 bash .../the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
    81195 bash .../the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
    81197 bash .../the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
    81200 python3 .../resources/board/run.py all
    88291 claude --print --dangerously-skip-permissions /pearde run <that row>

That is a harness, four frames deep in its own sibling recursion, holding a
live `pearde run` as a descendant. Four such dispatchers were running on that
one row at 12:03, and a fifth on `big/second`. The claims timestamped
`2026-09-03 12:03` and `12:04` across the board — a dozen of them — are that
one harness invocation's work.

`reproduced`, by process tree, at 12:03:37. **Do not re-measure by running the
probe**: running it is the defect firing.

## The cause

`resources/board/run.py` has two entry points. `read_main` is the read.
`main` dispatches, and `main` is what `__main__` calls:

    if kind == "reserved" and value == "all":
        return dispatchlib.main(rest, entries=entries)

`main` strips a leading `run` if one is there and otherwise ignores its
absence, so `run.py all` and `run.py run all` are the same command. The bare
form is not the read path; `read_main` is unreachable from `sys.argv`.

The probe believes otherwise. Its last check is written as

    A="$(... "$(cd / && python3 "$ROOT/resources/board/run.py" all 2>&1)")"

and its own comment above it calls that "the read" — "the read marks the
container `ready`, and `claim` refuses it". Every other command in the file is
correctly `run all --dry`; this one line is not, and it is the one that moves.
The file's header promises "`--dry` moves nothing" and the check named
`--dry opened no run log on this board` passes, all while the line below it
opens four.

## Why it is not free

`doctor.sh --harnesses` runs every harness on the board, and `collect`
re-checks a spec's verify commands. Either fans the machine out. The cost is
measured, not projected:

- **A worker was killed.** `agent-ae6439a54de4db4d6`, the implementer on
  `no-work-is-lost-on-the-board/the-board-locks-by-realpath`, froze at
  12:00:16 — the second its duplicate dispatcher lost the claim race and
  exited — while workers in the surviving window went on ticking to 12:02:27.
- **Every requested PRD in flight is racing.** Duplicate pass workers share
  one claim ledger, and the ledger does not cover two collects merging into
  one branch.
- **`.state/pass.md` is last-writer-wins** across them, over the board's only
  memory, with nothing detecting the loss.
- It ships. A harness that dispatches its user's whole watch set on
  `doctor --harnesses` is a product defect, not an instrument's quiet miss.

## Done means

- The probe's last check reads the frontier without dispatching it, and the
  read it uses is a path a reader can reach from the command line.
- No harness anywhere under `.pearde/prds/` launches a dispatcher. A check
  proves the absence over every `probe/` on the board, not over the one file
  this PRD repaired.
- `run.py`'s bare `all` either reaches `read_main` or refuses, so that the
  next person who writes `run.py all` meaning the read gets a refusal instead
  of a fan-out.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:59 — claim impl-harness-nodispatch 2026-09-03 14:01, silent 6.7h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/a-harness-never-dispatches-the-live-board`, whose worktree this sweep removed — the branch is kept.

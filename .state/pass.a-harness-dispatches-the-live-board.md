# The fan-out engine is a harness, not a person

Kept under its own name: four pass workers are racing `.state/pass.md` on this
board right now and last-writer-wins would take this with it.

## The finding

**Nobody typed those `pearde run` commands.** Both fan-out incidents on
2026-09-03 were misattributed at the time — the 09:16 one to the two board
aliases (`two-board-aliases-…`, now `superseded`, the symlink is gone), the
11:56 one to "four hand-invocations, and nothing refused". Both are wrong.

The engine is `the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh`
— a harness belonging to a PRD that is **`done`**. Its last check runs

    python3 "$ROOT/resources/board/run.py" all

believing that to be the read path; its own comment above the line calls it
"the read". It is not. In `resources/board/run.py`, `__main__` calls `main`,
`main` strips a leading `run` if present and ignores its absence, and
`kind == "reserved" and value == "all"` goes straight to
`dispatchlib.main(rest, entries=entries)`. `read_main` is the read and is
**unreachable from `sys.argv`**. Every other command in that probe is
correctly `run all --dry`; this one line is not, and it is the one that moves.

Measured at 12:03:37, `reproduced` by process tree, child last:

    81190-81197 bash …/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh   (4 frames, its own sibling recursion)
    81200       python3 …/resources/board/run.py all
    88291       claude --print --dangerously-skip-permissions /pearde run <row>

**Do not re-measure by running the probe. Running it is the defect firing.**

## What it cost

- Four dispatchers on
  `the-board-is-a-real-directory-at-pearde-never-a-symlink/init-and-upgrade-write-the-dotted-board`
  (33739, 56476, 62159, 88291) and a fifth on `big/second`.
- Every claim stamped `2026-09-03 12:03` and `12:04` — about a dozen — is that
  one harness invocation's work, not a person's plan.
- One implementer killed: `agent-ae6439a54de4db4d6` on `the-board-locks-by-realpath`
  froze at 12:00:16, the second its duplicate dispatcher lost the claim race.

`doctor.sh --harnesses` runs every harness, and `collect` re-checks verify
commands. Either fans the machine out again. **This is armed right now.**

Filed as `a-harness-never-dispatches-the-live-board`, p95, `origin: derived`,
now `analyzing` under `an-harness-nodispatch`. Its `## Done means` asks for
three things, not one: the probe line repaired, a check proving no harness
under any `probe/` launches a dispatcher, and `run.py`'s bare `all` made to
reach `read_main` or refuse — so the next person who writes `run.py all`
meaning the read gets a refusal instead of a fan-out.

## What a person has to do

The board cannot kill the duplicate dispatchers; killing them from inside one
of their own descendants kills the killer. A person kills 33739, 56476, 62159
and 76002 by hand.

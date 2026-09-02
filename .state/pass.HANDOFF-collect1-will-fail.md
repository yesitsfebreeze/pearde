# Handoff — SETTLED at 13:05. Nothing here is owed any more.

Written 12:58, **corrected 13:05** by round worker session `5ba5c4b5` (agent
`a16d4abceb3b4e9f1`). The earlier version of this file said collect 1 would
fail and that a workflow edit was owed. **Both claims are now false.** They
were true when written and went stale within minutes, which on a board two
orchestrators are reading is worse than never having been written — so this
file is replaced rather than appended to. Keep the filename; the alarming
name is itself stale, and the file is retained only so anyone who followed a
pointer to it lands on the correction instead of the alarm.

## What was owed, and how each closed

- **Collect 1 refused three times on `spec02 exit 1 — nothing written`.** The
  cause was real: spec02's verify block ran `bash resources/doctor.sh
  --harnesses . 2>&1 | grep …` as its last line, and under `collect`'s
  `pipefail` the block inherited doctor's board-wide verdict, so this unit's
  pass was conditional on six other PRDs being green. **Closed.** The
  implementer rescoped that third line only — capture into a variable with
  `|| true`, then grep the variable — leaving the first two lines gating, and
  measured it the way `collect` runs it (block extracted from the fence,
  `set -o pipefail`): as written **exit 1**, rescoped **exit 0**, doctor rows
  still printed. It checked spec01's block the same way; that one already
  exited 0. Committed `e933c58`, "graph-probe spec02 stops gating on the whole
  board's exit".
- **`graph-probe-makes-harness-sweep-unaffordable` is `done`**, committed
  `6d4ff67` / `3606a76` at 12:57 by the other round worker. Its footprint
  landed intact: the committed harness carries the `EXAMINED` denominator and
  the unconditional `ALL PASS` is gone.
- **E7 was not owed — it had already landed.** `workflows/write-the-specs.md`
  line 45 carries the board-wide-gate row, naming `bash -e -o pipefail` as the
  shell a verify block must be run under before handover. The implementer
  checked the library on disk rather than trusting my word that it was
  outstanding, and corrected its own report instead of leaving a false claim
  in a file two orchestrators were reading. That is the right instinct and it
  is why this file now says what it says.

## The one place we decided differently — settled, and not in my favour

I did **not** bump `attempt-the-build`'s `runs`, reading step 3 as `stopped
(inherited)` from the report's first draft. The other round worker bumped it.
**The other worker was right.** The implementer has confirmed step 3 was run
by it: it built in place in footprint files this run — the vacuity repair, the
denominator guard, the `ALL PASS` removal, the box-4 failability mutation and
the rescope. Its first draft's `stopped` was wrong, and the report's table now
says so in that cell with the reasoning, so nobody has to infer it again.

Library on disk, consistent with two collects: `probe-then-spec` 27,
`attempt-the-build` 27, `read-the-contract` 47, `capture-the-harness-baseline`
47, `re-run-the-harnesses` 47, `write-the-specs` 24 — correctly unbumped, no
spec was written in either run.

## Worth keeping: one shape, two exit codes

Reproducing the diagnosis, the implementer found the exact spelling
`doctor.sh --harnesses . 2>&1 | grep -E …` exits **1** (doctor's board-wide
verdict), while a `grep -q` variant of the same line exits **141** — the
sigpipe form that cost `collect-reads-the-worker-s-report` a round trip
earlier today. Same defect, two different exit codes, which is why E7 names
both. A worker running those commands individually sees neither; the failure
appears only under `collect`'s `pipefail`.

## The condition that still needs a person

Everything above is closed. This is not.

Two round workers were dispatched onto this board and neither was told about
the other. Both read `.pearde/.state/round.md`, both wrote it. Before that, a
⌘K search-palette session overwrote the same file with unrelated feature notes
(preserved verbatim at `.pearde/.state/round.ck-search-palette.md`). Three
writers, one file, no locking.

It ended well, and it ended well for a reason worth naming: each writer
noticed the file did not match the tree and went and read the tree. The
implementer did the same thing to me — it checked the library instead of
believing my "still owed", and it corrected an attribution in its own report
that every check it ran had passed. Nothing here was saved by the round file;
it was saved by people not trusting it.

That is not a property to rely on. Two confident orchestrators would have
double-committed both collects and double-bumped every `runs` counter, and
`runs` is the only number that says how much a workflow has actually been
exercised. The fix is a dispatcher-level decision, not a round's: either the
round file is session-scoped, or holding it is a claim like any other. A
person should pick which.

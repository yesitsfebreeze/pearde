---
memo: a-check-decided-by-scheduling
kind: decision
status: decided
subject: a harness whose verdict depends on what else is running is not evidence, and a check that stands down reports skip and is never counted as a pass
date: 2026-09-01
prds:
  - seven-closed-probes-drifted-red/the-doctor-completes-without-a-home
  - the-view-row-names-a-variable-that-exists
---

# a-check-decided-by-scheduling — green because nothing else was running is not green

## Decision

Two rules, and the second is the one that bites.

1. **A harness that binds a fixed machine-wide resource — a port, a path, a
   pidfile — is not evidence until it either claims that resource or fails
   loudly.** A count taken from such a harness is quoted with what else was
   running when it was taken, or it is not quoted.
2. **A check that declines to run reports `skip`, and a skip is never counted
   as a pass.** A probe may stand down from a race — that is the correct move
   when the racing file belongs to another PRD — but the number it prints
   afterwards must not be the number it would have printed had it run.

Sibling to `one-author-is-not-an-accepted-spec.md`: that memo forbids a check
that *cannot* fail. This one forbids a check that fails only sometimes, and a
check that stopped looking while still reporting success.

## Why

`prds/the-view-row-names-a-variable-that-exists/probe/verify.sh` binds ports
8477-8479 with no bind check, and `resources/doctor.sh:722` launches all 47
harnesses at once with no job cap. Two runs on one machine fight for the ports;
the loser's fixture server never comes up and its `view` rows read `broken` and
`off`. Three independent readers reproduced it — `10 pass · 0 fail` and
`9 pass · 1 fail` from the same tree back to back, and `6 checks · 4 pass ·
2 fail` from a deliberate second concurrent run. Nothing in the tree changed
between any pair of those runs.

That harness also never initialises `SRVPID3`. Line 27 sets `SRVPID=""` and
`SRVPID2=""`; `cleanup()` tests `[ -n "$SRVPID3" ]` under `set -u`, so any exit
before line 112 kills the trap **at that line** — `rm -rf "$D"` is never
reached and the first two servers are never killed. Two listeners leak
machine-wide, which makes the port collision permanent rather than transient.
The two defects compound: the leak guarantees the collision, and the collision
is what causes the early exits that trigger the leak.

Rule 2 was earned separately and later. The doctor PRD's probe was fixed to
stand down when `PEARDE_HARNESSES` is set or 8477 is held — the right move —
but the stood-down check counted itself a pass. On an identical tree with a
deliberately broken view-row harness, standalone read `11 checks · 10 pass ·
1 fail` and the same tree under `PEARDE_HARNESSES=1` read `11 checks · 11 pass
· 0 fail`. In the exact mode the acceptance box measured, the check could not
fail, and the count the box quoted as its proof was produced by the fix. The
stand-down also fires on *any* holder of the port — a bare unrelated socket was
enough. Combined with the leak above, one early exit retires that check forever
on that machine, silently, while it goes on reporting a pass.

A red check gets fixed. A flaky check gets re-run until it is green, and that
is worse: the board learns to disbelieve its own gates, and the next real red
is read as scheduling too. A skip counted as a pass is worse again — nobody
even knows to re-run it.

Under @references/parts/derived.md rule 2 the harness defects are a memo, not
PRDs: fixing them changes nothing about what ships, only whether the board can
believe its own instruments. They are recorded here rather than filed, and the
board's derived count already stands at 19/19 against a requested tree of 64.

## Alternatives considered

**File the port fix and the `SRVPID3` fix as derived PRDs against
`the-view-row-names-a-variable-that-exists`** — the honest repair, and both are
one-line changes: bind port 0 and read back what the kernel gave, and
`SRVPID3=""` beside its two siblings on line 27. It lost at filing time on rule
2 and on the tripwire. It should be folded into the next PRD that legitimately
opens that file, and this memo is the note that says so. It is not a decision
to leave them broken.

**Cap the sweep instead — a `-P`-style job limit at doctor.sh:722** — one
change fixing every present and future collision at once, without touching any
harness. It lost as the whole answer because it hides the defect rather than
removing it: the harnesses stay unable to run concurrently, and the first
person to run two by hand meets the same red with no sweep to blame. Worth
doing as well, never instead.

**Declare a "serial" set of harnesses the sweep runs one at a time** — more
precise than a global cap, and it keeps the sweep fast. It lost on bookkeeping:
the set is a list somebody has to maintain, and a harness that acquires a port
after being added to the parallel set is exactly the failure this memo exists
to stop, now with a file asserting it is safe.

**Let a stood-down check count as a pass and note it in the report** — the
cheapest reading of rule 2, and what the code did. Rejected: it makes the
summary count a number nobody can interpret without reading the prose beneath
it, which is the one thing a count is for.

## Consequences

- Every count quoted from a harness that binds a port now owes a statement of
  what else was running. That is real friction on a board whose gate runs 47
  harnesses at once, and it will be skipped unless a reviewer asks for it.
- A probe that stands down now reports three states rather than two, and every
  caller that parses `N checks · N pass · N fail` has to learn a fourth number.
  Nothing on the board parses those counts mechanically yet, so the cost is
  deferred rather than avoided.
- It deliberately does not fix the two harness defects. They stay in
  `the-view-row-names-a-variable-that-exists`, named here with their line
  numbers, waiting for the next writer who legitimately opens that file.
- It says nothing about the eleven harnesses currently red in the full sweep
  (`6 green · 39 unpinned · 66s`). At least one of them —
  `the-gate-runs-the-harnesses`, green standalone at `57/57` and red only
  inside the sweep — is another instance of exactly this defect, and the rest
  have not been read.

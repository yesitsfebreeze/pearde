---
memo: no-harness-under-the-board-dispatches-it
kind: invariant
status: decided
tags:
  - memo
  - kind/invariant
  - status/decided
subject: a harness measures the board and never moves it, and the read it needs is a command a person can type
date: 2026-09-03
verify: bash resources/invariants/no-harness-under-the-board-dispatches-it.sh
prds:
  - a-harness-never-dispatches-the-live-board
---
<!-- Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a
     typo and @resources/doctor.sh fails on it. @references/memo.md is the
     format. -->

# no-harness-under-the-board-dispatches-it — a harness measures, and the read it measures with is a command

## Decision

No file under any `prds/**/probe/` on this board launches something that
**moves** a board. A command whose command word resolves to `run.py`,
`dispatch.py`, `machine.py`, `pearde run` or a `claude … /pearde run`, with no
`--dry` and no read word after it, is a defect wherever written and
whatever the purpose.

One shape is exempt, and only one: a harness that dispatches a board **of its
own making**. Telling a fixture board from the user's is not decidable from
the source, so such a call carries its reason in a line of its own —

    # dispatch-exempt: <why this board is a fixture and not the user's>

— within six lines above it. An empty marker is not an exemption, and a marker
with no dispatcher under it is a stale line the reader reports rather than
honours. @resources/board/collect.py's `_park` exemption already uses the
shape, written down for the same reason: the exemption is the measurement, not
the function name.

The other half of the rule is the mechanism, because the rule alone would not
have prevented the fault. `run.py` run as a script refuses a bare scope, and
the refusal names the read that replaces it — `pearde plan <scope>`, restored
to @resources/board/plan.py, reaching `read_main` in
@resources/board/run.py. Reading and moving are two commands. The invariant
holds both halves: red if a harness dispatches, and red if the read the refusal
points at has been dropped again.

## Why

`doctor.sh --harnesses` runs every harness on the board, and `collect`
re-checks a spec's verify commands. A harness that dispatches turns either one
into a fan-out of the user's whole watch set. That happened twice on
2026-09-03 and was twice diagnosed as somebody having typed the command. At
12:03:37 the process tree of one pass worker held four nested frames of
`the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` with a live
`claude --print … /pearde run <row>` as a descendant. Nobody typed it. The
dozen claims stamped `12:03` and `12:04` across the board are that one harness
invocation's work, an implementer — `agent-ae6439a54de4db4d6` — froze at
12:00:16 the second its duplicate lost the claim race, and `.state/pass.md` is
last-writer-wins across duplicates over the board's only memory.

The rule is about every future harness rather than about the eight lines
repaired here, which is what makes it an invariant with a command instead of a
comment above a function. Nothing in a passing suite notices a new one: every
box stays green, and the cost lands in somebody else's worker.

**Why the mechanism is half the memo.** The line the PRD measured carries a
comment above it calling it "the read", and the comment was true when written.
Before `60f49d1 machine becomes run`, `main` in `machine.py` **was** the read
and the move was the sub-verb `machine dispatch`; that commit made `main` the
dispatcher and left `__main__` calling it, so every `machine.py all` written to
mean "print the frontier" silently became "dispatch every board the daemon
watches" with no harness line changed. And the read those lines should have
moved to was dropped a commit later: `_merged_plan` — the branch routing
`plan all`, `plan <group>` and the four windows to `read_main` — did not
survive the `plan.py` split, leaving `read_main` with no caller in the tree and
`pearde plan all` answering `pearde: no .pearde/ board at all`, while two
shipped skill files documented it as a command. `run.py all` was the only
spelling left on the machine that printed a frontier, and it printed it by
dispatching it. Repairing the harnesses alone would have left the next person
writing the same line for the same good reason.

**Why a reader and not a grep.** `grep -rn run.py` over this board returns 27
lines of which 8 are the defect, and it misses the worst one entirely: that one
is `RUN="${RUN_PY:-$ROOT/resources/board/run.py}"` on line 17 and `"$RUN" all`
on line 29, with the dispatcher's name in neither command position. So shell is
read positionally with the file's own variable assignments resolved, and Python
as an AST with module- and function-level bindings resolved to a fixed point,
so a `subprocess.run(argv)` whose `argv` was built two assignments earlier is
seen and a docstring naming `run.py` is not.

A scanner that has stopped matching passes everything, so two synthetic boards
run before the real one: one holding six spellings of the fault, every one of
which must be seen, and one holding eight near-misses — `--dry`, a read word, a
`grep` argument, a `[ -f … ]`, an `open()`, a comment, a docstring, an
exemption — none of which may be. And no board found is a **refusal**, never a
pass: a check reading green over an absent tree is this memo's own shape of
defect.

## Alternatives considered

**A comment in each harness saying not to.** What the board effectively had —
`the-machine-frontier-is-one-ordered-list/probe/verify.sh` calls itself
"read-only, so the whole harness is" on line 4 and dispatches the machine on
line 29. A sentence a file writes about itself is not a check.

**Leaving `run.py all` alone and repairing only the harnesses.** The PRD's own
`Done means` refuses this, and the history above is why: the fan-out was the
reasonable line to write, being the only spelling left that printed a frontier.

**Making `run.py all` silently mean the read.** Cheapest, and the worst: a
scope that dispatched yesterday and prints today is a command whose meaning
turned over without a refusal, which is exactly the change that caused this.
The script entry refuses instead, and names both commands.

**Asserting a count of dispatching harnesses.** The next legitimate fixture
dispatcher added would fail a check about a number rather than about the rule.
The reader asserts the property of each call site and prints its totals rather
than asserting them.

**Scanning the whole checkout rather than `prds/**/probe/`.** The board's code
dispatches on purpose, being the dispatcher. Only a harness is claiming to
measure while moving, and widening the scan would bury the eight lines under
every honest call site in `resources/board/`.

## Consequences

- A new dispatcher in a harness fails
  `pearde memo verify no-harness-under-the-board-dispatches-it` by file and
  line, with the offending line quoted.
- `run.py` as a script is a **move-only** entry: `python3 run.py all` exits 2.
  In-process `pearde run all` is untouched — the word `run` has already been
  eaten by @resources/pearde.py, so no person types the verb twice.
- It cannot see a command built from a variable **the file does not assign** —
  a shell `$RUN` exported by the caller, or a Python name bound from `argv`, a
  dict or a function's parameter. The reader collapses an unknown shell name to
  a marker rather than to the empty string, so it does not invent a call
  either; it simply does not see one.
- It cannot see a dispatcher reached through a **wrapper not in its table**. A
  harness that shells out to a helper script of its own, or to a `just` recipe,
  or to a `pearde` alias spelled some fourth way, reads green. `MOVERS`,
  `WRAPPERS` and the `claude … /pearde run` case are the whole list, and the
  list is the limit.
- It reads `.sh`, `.bash` and `.py` under `probe/` and nothing else. A harness
  written in another language, or a dispatcher in a spec's own `## Verify and
  Proof` block, is not this check's.
- An exemption is honoured on its marker alone. The reader cannot verify that
  the board named is really a fixture, and can only insist somebody wrote down
  why. `the-board-locks-by-realpath` is the one exemption on the board today,
  and both its spawns carry the line.

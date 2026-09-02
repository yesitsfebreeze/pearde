---
memo: a-harness-that-reads-the-whole-checkout-is-not-a-harness
kind: decision
status: decided
subject: a probe asserts over its own footprint, never over the live working tree, and its flip probe runs every file it claims for
date: 2026-09-02
prds:
  - two-self-tests-fail-on-timing-not-on-code
  - the-board-runs-itself/readme-in-three-rings
---

# a-harness-that-reads-the-whole-checkout-is-not-a-harness — a probe measures its footprint, not the machine

## Decision

A probe's assertions are scoped to files in its own PRD's footprint, or to a
fixture the probe itself built. **A probe never asserts on the state of the
live working tree.** Two corollaries, both learned the expensive way:

- A check that runs a repo-wide command — `index.py check`, `doctor.sh`, a
  bare `git status` — and asserts on its output is measuring whichever
  neighbouring session last saved a file. It reddens on work that is not the
  PRD's and stays green on a real break the neighbour happens to mask.
- **A flip probe must execute every file whose behaviour it certifies.** A
  flip that runs one of two footprint files proves one of two, and the
  report's claim covers both.

And a corollary about acceptance boxes: a box naming a command that cannot
produce a failing output is not an acceptance box. `git status --porcelain
.pearde` is the worked example — `.pearde/` is gitignored in the parent repo,
so that command prints zero bytes whatever the code does.

## Why

`two-self-tests-fail-on-timing-not-on-code` was collected `done` on
2026-09-02 (board commit `758b040`). It replaced two timing assertions with
work-counting ones and built two flip probes, and a skeptic consult
reproduced both flips independently: `flip-scan.sh` and `flip-readme.sh` each
go green on the input they must pass and red on the input they must catch.
The work was real and the DONE was earned.

The same consult found the contract's own sentence — "a red always means
something is actually broken" — **not yet true of one of the two footprint
files**:

- `readme-in-three-rings/probe/verify.sh:110` still runs
  `eq "G index.py check is silent" … "0"` over the whole live checkout. That
  is the exact disease the PRD existed to remove, surviving inside the PRD's
  own footprint. The implementer disclosed it (its finding 9) and correctly
  left it, because it was not one of the four assertions `spec02` named.
- `flip-readme.sh` invokes `quickstart.sh` only. `verify.sh` is never executed
  in any of its four trees, so `verify.sh:95`'s re-aimed install relation has
  no flip behind it, and `verify.sh` section F's relation is not known to be
  able to go red at all — nothing in the tree constructs that input.
- `spec01` box 4 named `git status --porcelain .pearde`. The implementer
  ticked it on the honest form, `git -C .pearde status --porcelain`, and
  recorded the weak spelling rather than editing a box mid-run. That was the
  right call for the running pass and is the wrong permanent state: the box
  as written is a green that cannot go red, and the command appears in no
  `## Verify and Proof` block, so `collect` never runs it in either spelling.

None of the three changes what the board ships — they change how loudly it
would notice. @references/parts/derived.md sends exactly that to a memo
rather than to a PRD, and the derived tripwire was already standing at
`3 derived in flight vs 2 requested`, so a fourth derived PRD would have been
the loop feeding on itself.

## Alternatives considered

**Refuse the DONE and send the implementer back.** It lost on attribution: the
gap is between what `spec02` asked for and what the PRD's contract sentence
promised — an under-spec by the analyst, not a failure by the implementer,
which met every box it was given and proved each against real output. It also
lost on availability: that worker was killed by an account rate limit minutes
after writing its report and cannot be resumed.

**File a derived PRD for the remaining sweep.** It lost on
@references/parts/derived.md's own test — would fixing this change what
ships, or only how loudly the board would have noticed? — and on the
tripwire, which the user has already been asked about once.

**Fold the box correction into the finished spec.** Rejected: `spec01` is
committed and `done`. Editing a closed PRD's acceptance box rewrites the
contract the work was measured against, after the fact.

## Consequences

- Three items are owed to whoever next opens `readme-in-three-rings`, which
  owns `probe/verify.sh` and `probe/quickstart.sh`: scope section G's
  `index.py check` to `git archive HEAD` or to the anchors the README names;
  extend `flip-readme.sh` to run `verify.sh` in all four trees; construct the
  input that makes section F's install relation go red, or delete the
  relation.
- One item is owed to whoever next opens
  `two-self-tests-fail-on-timing-not-on-code`'s `spec01`: correct box 4 to
  `git -C .pearde status --porcelain` and add it to `## Verify and Proof`.
- `README.md` still says "the twelve skills"; the tree builds seventeen. Same
  owner, same visit.
- This does **not** re-open the collected PRD, and does not claim its flips
  are unsound. Both were reproduced.
- It deliberately does not fix the general case: nothing yet stops a new probe
  from asserting over the live tree. This is filed as a `decision`, not an
  `invariant`, precisely because no check proves it today — an invariant whose
  `verify:` is red the day it is written records a wish, not a rule. The
  invariant becomes writable once the three owed items above land.

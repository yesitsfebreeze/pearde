---
state: "analyzing"
origin: requested
priority: 78
repo: "/Users/feb/dev/cartridge/prd.ctg"
footprint:
- "src/lifecycle.ts"
- ".cartridge/tests"
claim: "codex-lifecycle-prerequisite 2026-09-19T18:02:05.938Z"
---

# A done PRD's receipt survives a later PRD editing inside its footprint

## Outcome

A PRD that was verified and collected stays verified when a later, separately
collected PRD changes a path inside its footprint. Only an uncollected change
inside a done PRD's footprint makes its receipt stale.

## Evidence

On 2026-09-19 `completionProblem` in `src/lifecycle.ts` (about line 94)
returned "verified source footprint changed after collection" for
`@root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url`.
That child was collected at superproject `7354034` with footprint `web.ctg`.
Its sibling `the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it` was
then collected at `12a1646` and legitimately added
`web.ctg/.cartridge/.gitignore` and a memo under `web.ctg/.cartridge/memos`. The
check runs `git diff --name-only <commit> -- <footprint>` against HEAD, so any
later commit inside the footprint counts as drift, even one that has its own
verified receipt. As a result the parent rollup
`@root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository`
can never collect. The same refusal appears in older baselines for
`@proxy/improve-proxy-total-usage` and in `boards/gitfs`, so the class is
recurring.

A fix has to keep the check's purpose, which is catching unreviewed edits to
verified code. One candidate is to treat a path as drifted only when the
commits touching it since the receipt are not themselves the `commit:` of a
done PRD whose footprint covers that path.

## Acceptance

- [ ] A done PRD whose footprint is later changed only by commits that are the recorded `commit` of other done, verified PRDs covering those paths reports no completion problem.
- [ ] An uncollected or hand-made commit inside a done PRD's footprint still reports "verified source footprint changed after collection".
- [ ] A parent rollup whose children were collected in sequence over overlapping footprints collects.
- [ ] `bun test ./.cartridge/tests/records.test.ts` and the engine's own suite pass.

## Questions (2026-09-19, after review round 4 of 5)

Round 4 scored 81 and failed with two blocking findings. One of them can be
closed in the single remaining round; the other cannot, and it is a question
about what this PRD is worth rather than about how to write it. So it comes to
you rather than consuming the last round.

**F10, closable in round 5.** The published proof still fails on a correct
implementation, intermittently — one reference run in four, on the same tree
that passed three times, because a fixture test exceeds even the raised
30-second per-test timeout and its `afterEach` then removes the fixture root
while the timed-out `collect` is still running. The engine also kills a Verify
block at 120 seconds and runs each block twice, and block 1 measured 61 to 90
seconds on the reference and 155 on base. The remedy is a spec-only edit:
split block 1 into two blocks selecting disjoint subsets with `bun test -t`,
each with its own report and name gate. Raising the timeout only trades a
per-test failure for a block-timeout failure.

**F11, the question.** The rule's steady-state cost is unmeasured, and the
Design's published bound does not describe it. `vouches` calls `codeRepo(other)`
and `feet(other)` — each spawning a `git rev-parse` — and then a non-memoised
recursive `completionProblem`, all *before* the one memoised call the bound
accounts for. Measured on the live board: `codeRepo` 5.28 ms, `feet` 5.53 ms,
`completionProblem` 28.00 ms, against 390 done leaves and 1232 (commit, file)
pairs across 83 drifted records.

Today every one of those costs is zero, because no receipt carries `base:` yet
and the missing field rejects each candidate before any Git work happens. That
is why no earlier round saw it. As receipts accumulate `base:`, a board sweep
moves from the published 1.6 seconds toward minutes — and `verifiedStatus` runs
that sweep for every record.

**The decision.** Fixing F11 changes the rule's own code, which re-opens the
reference implementation, its seven tests and every measurement rounds 2 to 4
rest on, with no review round left to check the result.

- **Recommended: spend round 5 on F10, correct the steady-state sentence to say
  plainly that the cost is not bounded by `laneRange` and is unmeasured, and
  open F11 as its own PRD against the same function.** The rule is correct and
  this lands the correctness now.
- **Alternative: stop here.** If you would rather not land a rule whose cost
  grows as receipts accumulate `base:`, say so and this PRD waits for the
  performance work rather than preceding it.

One more thing you should weigh, recorded in the Design and confirmed by every
round since: **landing this clears nothing on the day it lands.** Base and
reference produce byte-identical verdicts over all 717 records today, this
PRD's own evidence case included. The conservative legacy choice was taken
deliberately; the remedy for the drifted records is re-collection, not this
rule. So the value of landing it now is that the *next* laundering attempt is
refused, not that anything currently broken becomes fixed.

Director verdict 2026-09-19 (via planner cartridge-e4): decided, defer; do not spend round 5 landing the rule without its cost bound. The rule clears nothing on the day it lands (review round 4: base and reference verdicts are byte-identical over all 717 records), while every collection from that day writes a `base:` that moves `prd plan` and `prd status` sweeps from 1.6 s toward minutes (F11). The follow-up PRD the recommendation relies on would sit on the prd board, which has no coordinator, so the cost would accrue with no owner. That is the premortem that rejects landing now. [[prove-it-works]] and [[subtract-before-you-add]] rule out shipping a known, unmeasured regression for zero present value. This row does not really hold its only dependent. `@root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository` is cleared by re-collecting its search child (`git branch -D lane/<board>-<slug>` first, see Remaining limits), not by this rule, because a legacy receipt vouches for nothing. Its planner should take that route and drop the `needs` edge. Reopen with `release <ref> open` as one fresh spec that lands the rule together with F11's remedy (test `laneRange` before `codeRepo(other)` and `feet(other)`, memoise `completionProblem` per sweep, and measure a sweep with `base:` receipts), plus F10's split Verify block, on a new round budget. Reverse this verdict if a laundering commit is actually observed to pass the current check, or if a coordinator takes the prd board and wants the combined PRD sooner.

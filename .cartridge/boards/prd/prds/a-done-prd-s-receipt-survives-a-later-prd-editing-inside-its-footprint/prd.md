---
state: "open"
origin: requested
priority: 78
repo: "/Users/feb/dev/cartridge/prd.ctg"
footprint:
- "src/lifecycle.ts"
- ".cartridge/tests"
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

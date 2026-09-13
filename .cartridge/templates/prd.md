---
repo: <absolute source repository path>
state: open
origin: requested
priority: 0
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
---

# <One observable resulting behavior>

<Problem, bounded outcome and accountable cartridge in two or three sentences.
Aim for 150–300 words; split independent outcomes before exceeding 400 words.>

## Acceptance

- [ ] <Successful behavior at the real consumer boundary.>
- [ ] <Invalid input, denial or stale revision leaves the right state intact.>
- [ ] <Cancellation, failure or restart has an observable recovery outcome.>

## Proof and recovery

<Exact starting files, disposable fixture, commands with cwd, and expected result.
State what must be probed before specs; proposed checks are not passing evidence.
Name the compatible fallback and durable state to preserve.>

## Dependencies and review

<Resolve hard prerequisites into needs frontmatter and narrow the footprint.
Link review.md, canonical source identity and inherited round count. Require an
attributed agent score >=90 with no blockers, within five rounds.>

<A parent contains only its outcome, child links and integration gate; each
executable leaf owns its acceptance. Do not paste a whole assessment into a PRD.>

---
state: open
origin: requested
priority: 35
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: repo-checks-cartridge
footprint:
  - "checks.ctg"
---

# The repository's own checks run as a post-pass

An agent working in an unfamiliar repository either guesses the verify command or runs the whole suite. Both are wrong: the guess misses the check the repository actually carries, and the full suite is too slow to run after an edit. Port pi's `rigor` as `checks.ctg`: discover the checks a repository already declares, record them, and run the ones a change warrants.

Discovery reads what is already there — package scripts, Makefile and justfile targets, cargo, go and pytest markers, and a repository's own probe script — and writes them to a recorded set that a later session reads instead of rediscovering. The post-pass after a change runs the change's own verify plus the checks around the changed files, never the whole suite: a full run belongs to a deliberate pre-merge gate, which this cartridge also exposes but never triggers on its own.

## Acceptance

- [ ] Discovery run against fixture repositories carrying a justfile, a package.json scripts block, a Makefile, a Cargo manifest and a pytest layout records each declared check with the command that runs it and the source file it was discovered from.
- [ ] A repository declaring no check at all records an empty set and reports that, rather than inventing a command.
- [ ] The post-pass for a change selects only the checks reaching the changed files plus the change's declared verify, and the selection is reported before anything runs.
- [ ] A failing check reports the check name, its command, and its output, and the post-pass stops at the first failure rather than running the remainder.
- [ ] The full gate is reachable as an explicit operation and is never run by the post-pass.
- [ ] Discovery and selection are tested offline against fixture repositories in `just test checks`; no check fixture reaches the network.

## Proof and recovery

Port from `/Users/feb/dev/pi/packages/coding-agent/src/core/rigor/` (542 lines at survey, verified present). Upstream writes its discovered set to a project-local JSON file; here it is recorded through the composition's own record ownership rather than a second store. Upstream couples the post-pass to a sub-agent dispatcher; this port runs the checks directly and leaves dispatch to the composition.

This child is sequenced first in the roll-up: its post-pass is what verifies the later children's own work.

Gates, cwd `/Users/feb/dev/cartridge`: `just test checks`, `just check checks`. Not run for this plan.

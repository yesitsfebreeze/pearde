---
state: open
origin: discovered
priority: 99
repo: "/Users/feb/dev/cartridge"
blast-radius: wide
work-kind: leaf
wave: 1
date: "2026-09-15"
footprint:
- "/Users/feb/dev/cartridge/prd.ctg/src/lifecycle.ts"
---

# Collect checks the footprint, not the whole working tree

## Outcome

A PRD whose every box is green can be collected in a repository where other
work is in progress. `prd collect` refuses on paths outside the footprint, as
it should, but it reads them from the whole working tree rather than from the
change it is about to make.

## Acceptance

- [ ] `prd collect` succeeds for a PRD whose footprint is clean and whose boxes are green, while unrelated paths in the same repository are dirty, including modified submodules and untracked directories.
- [ ] A commit that touches a path outside the footprint is still refused, by the existing `assertFootprint` check on the candidate revision.
- [ ] An unrelated dirty path is never staged, committed or reverted by a collection.
- [ ] The three items this blocked on 2026-09-15 collect without their footprints changing.

## Result

Found 2026-09-15 by the coordinator, after three separate PRDs reached every
box green and none could be landed. All three refuse at the same line:

```
$ just prd collect the-gates-run-from-the-root-justfile --board root
changed path is outside the PRD footprint: agent.ctg
$ just prd collect the-record-has-one-vocabulary-and-no-shadowed-copies --board root
changed path is outside the PRD footprint: agent.ctg
$ just prd collect the-profile-is-the-orchestration-service/the-composition-comes-up-without-memory --board root
changed path is outside the PRD footprint: agent.ctg
```

`agent.ctg` is a submodule holding another session's uncommitted work. Each of
the three PRDs has a clean footprint and a commit that touches nothing else.

`prd.ctg/src/lifecycle.ts` scans `git status --porcelain=v1 -z
--untracked-files=all` over the whole repository and throws on the first entry
outside the footprint. In a composed repository of eighteen submodules worked
by concurrent sessions, that condition is never satisfied. Today the tree shows
fourteen modified submodules and two untracked directories, none of them
related to any PRD on this board.

The check the routine actually wants is already there and already passing:
`assertFootprint` diffs the candidate commit against the base and rejects any
committed path outside the footprint. The working-tree scan exists so that
verification output does not get swept into the commit, which is worth keeping,
but the correct scope for it is the footprint, not the repository. Restricting
the scan to footprint paths preserves what it is for and stops unrelated work
from blocking every collection.

Three ways out were considered. The other sessions committing their work only
lasts until the next concurrent edit. Adding `.obsidian/` and `.yolo-test/` to
`.gitignore` removes two of sixteen blockers. Only narrowing the scan is a
lasting fix, and it is the one this PRD names.

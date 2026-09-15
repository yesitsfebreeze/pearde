---
state: "specced"
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

- [x] `prd collect` succeeds for a PRD whose footprint is clean and whose boxes are green, while unrelated paths in the same repository are dirty, including modified submodules and untracked directories.
- [x] A commit that touches a path outside the footprint is still refused, by the existing `assertFootprint` check on the candidate revision.
- [x] An unrelated dirty path is never staged, committed or reverted by a collection.
- [x] The three items this blocked on 2026-09-15 collect without their footprints changing.

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

### Done, same day

The status call now carries a pathspec built from the footprint. Nothing else
moved: `assertFootprint` still diffs the candidate commit against the base and
rejects any committed path outside the footprint, `cleanIndex` still refuses a
repository with staged changes, and the per-entry footprint check stays as a
second line of defence.

Two of the three blocked collections went through immediately, against a
working tree carrying 23 unrelated dirty and untracked entries:

```
$ just prd collect the-gates-run-from-the-root-justfile --board root
Verified and collected the-gates-run-from-the-root-justfile at 585a7677d6714a9c15d6fe92a2e6db13538c5ae4

$ just prd collect the-composition-comes-up-without-memory --board root
Verified and collected the-profile-is-the-orchestration-service/the-composition-comes-up-without-memory at 585a7677d6714a9c15d6fe92a2e6db13538c5ae4
```

Nothing unrelated was touched. The 23 entries were still there afterwards, and
the collection commit in prd.ctg contains exactly two files, the PRD and its
receipt.

The third, `the-record-has-one-vocabulary-and-no-shadowed-copies`, now refuses
for a reason that is correct rather than incidental:

```
changed path is outside the PRD footprint: .cartridge/memos/principle/no-redundant-comments.md
```

That file is another session's, written while this pass ran, and it is inside
that PRD's own `.cartridge/memos/**` footprint. Uncommitted work inside the
footprint is exactly what this check is for, so the refusal stands and the item
stays specced until its owner commits it.

`just check prd` passes and `just test prd` is unchanged: 69 pass, 6 fail,
the same six cases as before the edit.

---
atomic: merge-blocking-branch
subject: pulls the landed sibling's commits in and turns the abstract "4 files disagree" into concrete diff hunks to read
date: 2026-09-03
runs: 0
tags:
  - atomic
---

## Do

1. From the lane, `git merge --no-commit --no-ff <blocking-branch>` (named in
   the PRD's `## Blocked` note), then `git diff --name-only --diff-filter=U`
   to list the files that actually conflict.

## Done when

- Every conflicted file has been read end to end at least once, with the
  `<<<<<<<`/`|||||||`/`=======`/`>>>>>>>` hunks identified and the commit
  range on the blocking side (`git log <merge-base>..<blocking-branch> --
  <file>`) read to know what changed and why.

## Fails when

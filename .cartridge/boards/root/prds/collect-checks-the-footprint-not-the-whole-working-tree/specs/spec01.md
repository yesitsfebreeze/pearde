---
complexity: small
footprint:
  - /Users/feb/dev/cartridge/prd.ctg/src/lifecycle.ts
---

# spec01 — scope the pre-commit scan to the footprint

`collect` asks git for the status of the whole repository and throws on the
first entry outside the footprint. Give the same question a pathspec, so it
asks only about the paths the collection may touch.

- `git status --porcelain=v1 -z --untracked-files=all` becomes the same
  command with `-- <footprint paths relative to the code root>`.
- The per-entry footprint check stays. It is now a second line of defence
  rather than the only one, and it still catches a pathspec that overlaps more
  than intended.
- Everything else is unchanged: `assertFootprint` still diffs the candidate
  commit against the base and rejects any committed path outside the
  footprint, `cleanIndex` still refuses a repository with staged changes, and
  `git add` and `git commit --only` still name exactly the paths found.

This narrows what the collection looks at; it never widens what it commits.
Only footprint paths were ever staged, so no unrelated path can enter a commit
either before or after. What goes away is a refusal that no repository of
eighteen submodules worked by concurrent sessions can ever avoid.

The one thing given up is incidental: a file written outside the footprint by
a verification command used to be reported here. It was never committed, so
the loss is a diagnostic, not a guard.

## Acceptance

- [x] The status call is scoped by a pathspec built from the PRD footprint, and the per-entry footprint check remains.
- [x] `prd collect` succeeds for a PRD with green boxes and a clean footprint while unrelated submodules and untracked directories in the same repository are dirty.
- [x] Nothing outside the footprint is staged or committed by that collection: the resulting commit touches only footprint paths, and the unrelated dirty paths are still dirty afterwards.
- [x] `just check prd` passes and `just test prd` is unchanged by this edit.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge

# The scan is scoped, and the per-entry check is still there.
grep -q "status', '--porcelain=v1', '-z', '--untracked-files=all', '--', \.\.\.scope" prd.ctg/src/lifecycle.ts
grep -q "changed path is outside the PRD footprint: " prd.ctg/src/lifecycle.ts

# The committed-revision guard is untouched.
grep -q "committed path is outside the PRD footprint: " prd.ctg/src/lifecycle.ts
grep -q "repository has staged changes; preserve them before collection" prd.ctg/src/lifecycle.ts

just check prd | grep -Eq '^check +prd +pass$'

echo 'collect scans the footprint'
```

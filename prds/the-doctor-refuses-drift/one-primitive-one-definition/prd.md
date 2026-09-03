---
state: open
origin: requested
priority: 85
complexity: 15
blast-radius:
needs: every-module-finds-its-siblings-by-one-rule
---

# one primitive one definition

A doctor row `primitives` that reads every `resources/**/*.py` and reports broken when a second definition of `find_board`, `parse_frontmatter`/`split_frontmatter`, `atomic_write`, a git runner (`def git(`), or a `## section` extractor exists outside `resources/common.py`, naming both files.

On 2026-09-03 the tree held 8 frontmatter parsers, 7 board resolvers, 9 section extractors and 6 git runners.

## Done means

Plant a copy of `find_board` in a scratch module → the row is broken naming both files; remove it → ok.

## Needs

`every-module-finds-its-siblings-by-one-rule` — the same gate as the container `the-doctor-refuses-drift`.

## Questions

### Q1: How much this check cleans up

You are choosing whether the new check ships passing or failing. The tree
already holds thirty-seven copies of the five shared helpers it looks for, so a
check that reports every one of them starts out failing, while a check that
draws a line under today starts out passing?

1. **Draw a line under today** — the check ships passing, records today's thirty-seven as known, and fails the moment anyone writes a thirty-eighth. (recommended)
2. **Clean them up now** — the check ships naming all thirty-seven, and the same job folds every copy into the shared file.
3. **Report them and leave them** — the check ships naming all thirty-seven and keeps failing until some later job folds them in.

<!-- for the board: resources/primitives.py problems(); doctor.sh primitives row; answer 2 is a REFINE into a fold-in child over 14 modules -->

### Q2: The two helpers with no home

The check looks for five shared helpers, but the shared file holds only three of
them — nothing there runs git, and nothing there cuts a document at its
headings. So sixteen of the copies have no single version to point at?

1. **Write the two missing ones** — the shared file gains a way to run git and a way to cut a document. (recommended)
2. **Watch only the three that already exist** — the check says nothing about running git or cutting documents until someone writes those two.
3. **Report them as missing** — the check names the two absent helpers as a problem, and keeps failing until they are written.

<!-- for the board: common.py has find_board, split_frontmatter/parse_frontmatter, atomic_write but no git() and no section(); 7 git runners and 9 section extractors depend on this -->

## Answers

**Q1** *(answered 2026-09-03 14:37)* — Clean them up now — the check ships naming all thirty-seven, and the same job folds every copy into the shared file.

**Q2** *(answered 2026-09-03 14:37)* — Write the two missing ones — the shared file gains a way to run git and a way to cut a document.

## Children

| child | contract | needs |
|---|---|---|
| `common-py-gains-a-git-runner-and-a-section-extractor` | resources/common.py` holds one git runner and one section extractor, each shaped (via `check=`/`default=`/`raise_as=`-style parameters) to cover every existing caller's return-or-raise contract, so every module below has one version to point at. | — |
| `the-top-level-resources-modules-delegate-to-common` | resources/guard.py`, `health.py`, `knowledge.py`, `questions.py` and `workflows.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`. | common-py-gains-a-git-runner-and-a-section-extractor |
| `the-core-board-modules-delegate-to-common` | resources/board/boards.py`, `collect.py`, `edit.py`, `prdfile.py` and `specs.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`. | common-py-gains-a-git-runner-and-a-section-extractor |
| `the-lane-and-repo-modules-delegate-to-common` | resources/board/lanes.py`, `orphans.py`, `ramp.py`, `refuse.py`, `repos.py`, `shared.py` and `transitions.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`. | common-py-gains-a-git-runner-and-a-section-extractor |
